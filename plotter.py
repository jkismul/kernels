import pickle
import argparse
import matplotlib.pyplot as plt
import numpy as np
from Parameters import common_parameters

parser = argparse.ArgumentParser()
parser.add_argument('-L6', help='Include L6? y/n')
args = parser.parse_args()

num_channels = 16
num_tsteps = 1 + len(np.arange(0,
                               common_parameters['cell_parameters']['tstop'],
                               common_parameters['cell_parameters']['dt']))

# Read kernel data
L5ae = pickle.load(open('data_out/L5ae.p', 'rb'))
L5be = pickle.load(open('data_out/L5be.p', 'rb'))
L5ai = pickle.load(open('data_out/L5ai.p', 'rb'))
L5bi = pickle.load(open('data_out/L5bi.p', 'rb'))
#
L23ae = pickle.load(open('data_out/L23ae.p', 'rb'))
L23be = pickle.load(open('data_out/L23be.p', 'rb'))
L23ai = pickle.load(open('data_out/L23ai.p', 'rb'))
L23bi = pickle.load(open('data_out/L23bi.p', 'rb'))
#
L6ae = pickle.load(open('data_out/L6ae.p', 'rb'))
L6be = pickle.load(open('data_out/L6be.p', 'rb'))
L6ai = pickle.load(open('data_out/L6ai.p', 'rb'))
L6bi = pickle.load(open('data_out/L6bi.p', 'rb'))

if args.L6 == 'y':
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = \
        plt.subplots(3, 2,
                     # sharey='row',
                     sharex='col',
                 gridspec_kw={'wspace': .2, 'hspace': 0},
                     subplot_kw={'autoscale_on':False,'adjustable':'datalim','xlim':[2,3],'ylim':[2,3]},
                 figsize=(5, 10)
                     )
    axes = [ax1, ax2, ax3, ax4, ax5, ax6]
else:
    fig, ((ax1, ax2), (ax3, ax4)) = \
        plt.subplots(2, 2, sharey='row', sharex='col',
                     gridspec_kw={'wspace': 0, 'hspace': 0})
    axes = [ax1, ax2, ax3, ax4]
# fig.set_size_inches(10,10)
populations = [
    [L5ae, L5be], [L5ai, L5bi],
    [L23ae, L23be], [L23ai, L23bi],
    [L6ae, L6be], [L6ai, L6bi]
]

names = ['L5e', 'L5i', 'L23e', 'L23i', 'L6e', 'L6i']

for j, ax in enumerate(axes):
    ax.plot(65 * populations[j][0][-1] / np.max(np.abs(populations[j][0][:][-1])) + (17 * 100), 'r', lw=0.5)
    ax.plot(65 * populations[j][1][-1] / np.max(np.abs(populations[j][1][:][-1])) + (17 * 100), 'b', lw=0.5)
    ax.text(60, 700, names[j], c='lime', size=20, zorder=0)

for i in range(num_channels):
    for j, ax in enumerate(axes):
        ax.plot(65 * populations[j][0][i] / np.max(np.abs(populations[j][0][:][:-1])) + (i * 100), 'r', lw=0.5)
        ax.plot(65 * populations[j][1][i] / np.max(np.abs(populations[j][1][:][:-1])) + (i * 100), 'b', lw=0.5)
        ax.set_xticks(np.linspace(0, num_tsteps, 6))
        ax.set_xticklabels(np.linspace(0, 50, 6).astype(int))
        ax.set_xticks([])
        yy=np.linspace(-100,1800,20)
        ax.set_yticks(yy)
        y_labels = np.array(['',*np.linspace(1600,100,16).astype(int),'','S',''])
        ax.set_yticklabels(y_labels)
        y_ticks = ax.yaxis.get_major_ticks()
        for tick in y_ticks:
            tick.label.set_fontsize(5)


ax1.set_ylabel('depth [um]')
ax3.set_ylabel('depth [um]')

if args.L6 == 'y':
    ax5.set_xticks(np.linspace(0, num_tsteps, 6))
    ax5.set_xticklabels(np.linspace(0, 50, 6).astype(int))
    ax6.set_xticks(np.linspace(0, num_tsteps, 6))
    ax6.set_xticklabels(np.linspace(0, 50, 6).astype(int))
    ax5.set_ylabel('depth [um]')
    ax5.set_xlabel('time [ms]')
    ax6.set_xlabel('time [ms]')
else:
    ax3.set_xticks(np.linspace(0, num_tsteps, 6))
    ax3.set_xticklabels(np.linspace(0, 50, 6).astype(int))
    ax4.set_xticks(np.linspace(0, num_tsteps, 6))
    ax4.set_xticklabels(np.linspace(0, 50, 6).astype(int))
    ax3.set_xlabel('time [ms]')
    ax4.set_xlabel('time [ms]')
plt.show()
