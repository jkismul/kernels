import os
import LFPy
import pickle
import numpy as np
from functions import *
from Parameters import *

# <editor-fold desc="make output data directory">
try:
    os.makedirs('data_out')
except OSError:
    pass
# </editor-fold>

populations=['L5','L23']#,'L6']
# populations=['L5','L23','L6']

synapse_positions = ['apic','bas']
pos_names=['a','b']
synapse_types = ['excitatory','inhibitory']
type_names = ['e','i']
params = [L5_parameters,L23_parameters]#,L6_parameters]
# params = [L5_parameters,L23_parameters,L6_parameters]

num_tsteps = 1+len(np.arange(0,
                           common_parameters['cell_parameters']['tstop'],
                           common_parameters['cell_parameters']['dt']))

p = [] #dipole moment
v = [] #vmem
im = []
total_LFP = []

for j in range(len(populations)):
    parameters = params[j]
    electrodeParameters['z']=electrodeParameters['z_{}'.format(populations[j])]
    for l in range(len(synapse_types)):
        if l == 1:
            parameters['synapse_parameters']['weight'] = \
                parameters['synapse_parameters']['{}_weight'.format(synapse_types[l])]
        for k in range(len(synapse_positions)):
            cell_LFP=[]
            EEG = np.zeros(num_tsteps)
            for i in range(parameters['num_cells']):
                #pick a random place in 'markram-cylinder'
                R=210
                r=R*np.sqrt(np.random.uniform())
                theta = np.random.uniform()*2*np.pi
                x_loc = r*np.cos(theta)
                y_loc = r*np.sin(theta)

                #simulate cell
                print('cell {} of {}.'.format(i + 1, parameters['num_cells']), end='\r')
                cell = LFPy.Cell(**common_parameters['cell_parameters'])
                cell.set_rotation(x=4.99, y=-4.33)  # let rotate around z-axis
                cell.set_pos(x=x_loc,y=y_loc,z=np.random.normal(loc=parameters['heights']['soma'],scale=50))
                insert_synapses(parameters['synapse_parameters'], synapse_positions[k], parameters['n_syn']
                                ,parameters['heights'],cell)
                cell.simulate(rec_imem=True, rec_vmem=True, rec_current_dipole_moment=True)

                v.append(cell.vmem[0]) #storing vmem in soma, not used
                im.append(cell.imem) #storing all imem, not used

                #calculate LFP
                elec = LFPy.RecExtElectrode(cell,**electrodeParameters)
                elec.calc_lfp()
                cell_LFP.append(elec.LFP)

                #calculate EEG (using 4-sphere)
                P = cell.current_dipole_moment
                somapos = np.array([cell.xmid[0], cell.ymid[0], radii[0]+cell.zmid[0]])
                r_soma_syns = [cell.get_intersegment_vector(idx0=0, idx1=i) for i in cell.synidx]
                r_mid = np.average(r_soma_syns, axis=0)
                r_mid = somapos + r_mid/2.
                eeg_coords_top = np.array([[0., 0., radii[3] - rad_tol]])
                four_sphere_top = LFPy.FourSphereVolumeConductor(radii, sigmas, eeg_coords_top)
                pot_db_4s_top = four_sphere_top.calc_potential(P, r_mid)
                eeg_top = np.array(pot_db_4s_top) * 1e9
                EEG += np.squeeze(np.array(pot_db_4s_top) * 1e9)

            total_LFP.append(np.sum(cell_LFP,axis=0))
            tot = np.sum(cell_LFP,axis=0)
            population_LFP = np.vstack((tot,EEG))

            pickle.dump(population_LFP,open('data_out/{}{}{}.p'.format(populations[j],pos_names[k],type_names[l]),'wb'))