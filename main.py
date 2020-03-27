import os
import argparse
import numpy as np
import LFPy
import pickle
import matplotlib.pyplot as plt
import time
import scipy.signal as ss
from matplotlib.collections import PolyCollection

from functions import *
from Parameters import *

fitses = pickle.load(open('data_in/fits_inhibition_off.p', 'rb'))
lines = pickle.load(open('data_in/lines_inhibition_off.p', 'rb'))


populations=['L5','L23']#,'L6']
synapse_positions = ['apic','dend']
pos_names=['a','b']
synapse_types = ['excitatory','inhibitory']
syn_names = ['e','i']
params = [L5_parameters,L23_parameters]
EEG = np.zeros(401)

p = [] #dipole moment
v = [] #vmem
im = []
x_line = np.linspace(0, common_parameters['cell_parameters']['tstop'], len(fitses[0]))

elleffpe = [9]
syni=[]
dipole_moments=[]
dipole_locs=[]
total_LFP = []

for j in range(len(populations)):
    parameters = params[j]
    electrodeParameters['z']=electrodeParameters['z_{}'.format(populations[j])]
    for k in range(len(synapse_positions)):
        for l in range(len(synapse_types)):
            if l==1:
                # parameters['synapse_parameters']['weight'] = parameters['synapse_parameters']['weight']*-1
                parameters['synapse_parameters']['weight'] = parameters['synapse_parameters']['{}_weight'.format(synapse_types[l])]
            cell_LFP=[]
            for i in range(parameters['num_cells']):
                R=210
                r=R*np.sqrt(np.random.uniform())
                theta = np.random.uniform()*2*np.pi
                x_loc = r*np.cos(theta)
                y_loc = r*np.sin(theta)

                print('cell {} of {}.'.format(i + 1, parameters['num_cells']), end='\r')
                cell = LFPy.Cell(**common_parameters['cell_parameters'])#**cell_parameters)
                cell.set_rotation(x=4.99, y=-4.33)  # let rotate around z-axis
                # cell.set_pos(x=np.random.normal(loc=0,scale=100),y=np.random.normal(loc=0,scale=100),z=np.random.normal(loc=parameters['heights']['soma'],scale=10))
                cell.set_pos(x=x_loc,y=y_loc,z=np.random.normal(loc=parameters['heights']['soma'],scale=50))

                insert_synapses(parameters['synapse_parameters'], synapse_positions[k], parameters['n_syn']
                                ,parameters['heights'],cell)


                cell.simulate(rec_imem=True, rec_vmem=True, rec_current_dipole_moment=True)
                P = cell.current_dipole_moment
                p.append(np.asarray(P[:,2]))
                v.append(cell.vmem[0])
                im.append(cell.imem)
                elec = LFPy.RecExtElectrode(cell,**electrodeParameters)
                elec.calc_lfp()
                cell_LFP.append(elec.LFP)
                elleffpe.append(elec.LFP)
                dipole_moments.append(cell.current_dipole_moment)
                somapos = np.array([cell.xmid[0], cell.ymid[0], radii[0]+cell.zmid[0]])
                r_soma_syns = [cell.get_intersegment_vector(idx0=0, idx1=i) for i in cell.synidx]
                r_mid = np.average(r_soma_syns, axis=0)
                r_mid = somapos + r_mid/2.
                dipole_locs.append(somapos[2])

                eeg_coords_top = np.array([[0., 0., radii[3] - rad_tol]])
                four_sphere_top = LFPy.FourSphereVolumeConductor(radii, sigmas, eeg_coords_top)
                pot_db_4s_top = four_sphere_top.calc_potential(P, r_mid)
                eeg_top = np.array(pot_db_4s_top) * 1e9
                EEG += np.squeeze(np.array(pot_db_4s_top) * 1e9)
            total_LFP.append(np.sum(cell_LFP,axis=0))
            tot = np.sum(cell_LFP,axis=0)

# SoME REDUNDANT BITS HERE! FIX
            population_LFP =[]

            population_LFP.append(tot)

            population_LFP = np.squeeze(population_LFP)

            population_LFP = np.vstack((EEG,population_LFP))
            pickle.dump(population_LFP,open('data_out/{}{}{}.p'.format(populations[j],pos_names[k],syn_names[l]),'wb'))
