import LFPy
import numpy as np

def insert_synapses(synparams, section, n,heights,cell):
    soma_h = heights['soma']
    if section == 'dend':
        maxim = heights['basal_max']
        minim = heights['min']
    if section == 'apic':
        maxim = heights['max']
        minim = heights['apical_min']
    if section == 'allsec':
        maxim = heights['max']
        minim = heights['min']
    if section =='soma':
        maxim=0
        minim=0
    '''find n compartments to insert synapses onto'''
    idx = cell.get_rand_idx_area_norm(section=section, nidx=n, z_min=soma_h+minim, z_max=soma_h+maxim)
    # Insert synapses in an iterative fashion
    for i in idx:
        synparams.update({'idx': int(i)})
    #     # Create synapse(s) and setting times using the Synapse class in LFPy
        s = LFPy.Synapse(cell, **synparams)
        s.set_spike_times(np.array([np.random.normal(loc=25,scale=1)]))