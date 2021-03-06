import numpy as np

num_channels=16
N = np.empty((num_channels, 3))
for i in range(N.shape[0]): N[i,] = [1, 0, 0]
electrodeParameters = {
    'sigma' : 0.3,              # Extracellular potential
    'x' : np.zeros(num_channels), # x,y,z-coordinates of electrode contacts
    'y' : np.zeros(num_channels),
    'z' : np.linspace(-1600, -100, num_channels),
    'z_L5': np.linspace(-1600, -100, num_channels),
    'z_L23': np.linspace(-3100, -100, num_channels),
    'z_L6': np.linspace(-1600, -100, num_channels),
    'n' : 20,
    'r' : 10,
    'N' : N,
}

morphology = 'morphologies/L5_Mainen96_LFPy.hoc'

common_parameters = {
    'cell_parameters': {
    'morphology': morphology,
    'cm': 1.0,  # membrane capacitance
    'Ra': 150.,  # axial resistance
    'v_init': -65.,  # initial crossmembrane potential
    'passive': True,  # turn on NEURONs passive mechanism for all sections
    # 'passive': False,  # turn on NEURONs passive mechanism for all sections
    'passive_parameters': {'g_pas': 1. / 30000, 'e_pas': -65},
    'nsegs_method': 'lambda_f',  # spatial discretization method
    'lambda_f': 500.,  # frequency where length constants are computed
    'dt': 2. ** -3,  # simulation time step size
    'tstart': -10.,  # start time of simulation, recorders start at t=0
    'tstop': 50.,  # 50  # stop simulation at 100 ms.

    }
}

L5_parameters={
    'num_cells':100, #wanted 6k but that failed
    'n_syn':200, #JFK: NEED SOME REAL NUMBER HERE 200 is ok
    'heights':{
        'max':1000.,
        'min':-1000.,
        'basal_max':-50,#200,#-50.,
        'apical_min':500,#400,#500.,
        'soma': -1300.,
    },
    'synapse_parameters':{
        'idx': [],
        'e':0.,
        # 'syntype': 'ExpSyn',  # synapse type
        # 'tau':2.**-3,#0.1,
        # 'syntype': 'Exp2Syn',  # synapse type
        # 'tau1': .2, #used 5
        # 'tau2': .3, #used 6
        'syntype': 'ExpSynI',
        'tau':1,#2. ** -3,#.1, #used 1.0 for most long runs
        'weight': .1,#.1001,  # synaptic weight
        'excitatory_weight':.1,
        'inhibitory_weight':-.1,
        'record_current': True,  # record synapse current
    },
}

L23_parameters={
    'num_cells':100,
    'n_syn':200,
    'heights':{
        'max':1000.,
        'min':-1000.,
        'basal_max':-50.,
        'apical_min':500.,
        'soma': -1250.+200., #200 is added to push soma up from the bottom of L3
    },
    'synapse_parameters':{
        'idx': [],
        'e':0.,
        'syntype': 'ExpSynI',
        'tau':1,#2. ** -3,#1.,
        'weight': .1,#.1001,  # synaptic weight
        'excitatory_weight': .1,
        'inhibitory_weight': -.1,
        'record_current': True,  # record synapse current
    },
}

L6_parameters={
    'num_cells':10,
    'n_syn':200,
    'heights':{
        'max':1000.,
        'min':-1000.,
        'basal_max':-50.,
        'apical_min':500.,
        'soma': -1700., #about center of markram L6
    },
    'synapse_parameters':{
        'idx': [],
        'e':0.,
        'syntype': 'ExpSynI',
        'tau':1,#2. ** -3,#1.,
        'weight': .1001,  # synaptic weight
        'excitatory_weight': .1,
        'inhibitory_weight': -.1,
        'record_current': True,  # record synapse current
    },
}

radii = [79000., 80000., 85000., 90000.]
sigmas = [0.3, 1.5, 0.015, 0.3]
rad_tol = 1e-2