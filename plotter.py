import pickle
import matplotlib.pyplot as plt
import numpy as np

num_channels = 16+1 #one for EEG/ERP

#Read kernel data
L5ae = pickle.load(open('data_out/L5ae.p','rb'))
L5be = pickle.load(open('data_out/L5be.p','rb'))
L5ai = pickle.load(open('data_out/L5ai.p','rb'))
L5bi = pickle.load(open('data_out/L5bi.p','rb'))
#
L23ae = pickle.load(open('data_out/L23ae.p','rb'))
L23be = pickle.load(open('data_out/L23be.p','rb'))
L23ai = pickle.load(open('data_out/L23ai.p','rb'))
L23bi = pickle.load(open('data_out/L23bi.p','rb'))

# print(np.shape(L5ae))
# plt.figure()
# for i in range(1,17):
#     plt.plot(L5ae[i]/np.max(np.abs(L5ae[i]))+i)
# plt.show()

fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2,sharey='row',gridspec_kw={'wspace':0})

ax1.plot(65 * L5ae[0] / np.max(np.abs(L5ae[0])), 'r', lw=0.5)
ax1.plot(65 * L5be[0] / np.max(np.abs(L5be[0])), 'b', lw=0.5)
ax2.plot(65 * L5ai[0] / np.max(np.abs(L5ai[0])), 'r', lw=0.5)
ax2.plot(65 * L5bi[0] / np.max(np.abs(L5bi[0])), 'b', lw=0.5)

ax3.plot(65 * L23ae[0] / np.max(np.abs(L23ae[0])), 'r', lw=0.5)
ax3.plot(65 * L23be[0] / np.max(np.abs(L23be[0])), 'b', lw=0.5)
ax4.plot(65 * L23ai[0] / np.max(np.abs(L23ai[0])), 'r', lw=0.5)
ax4.plot(65 * L23bi[0] / np.max(np.abs(L23bi[0])), 'b', lw=0.5)
for i in range(1,num_channels):
    ax1.plot(65*L5ae[i]/np.max(np.abs(L5ae[1:]))+(i*100),'r',lw=0.5)
    ax1.plot(65*L5be[i]/np.max(np.abs(L5be[1:]))+(i*100),'b',lw=0.5)
    ax2.plot(65*L5ai[i]/np.max(np.abs(L5ai[1:]))+(i*100),'r',lw=0.5)
    ax2.plot(65*L5bi[i]/np.max(np.abs(L5bi[1:]))+(i*100),'b',lw=0.5)

    ax3.plot(65*L23ae[i]/np.max(np.abs(L23ae[1:]))+(i*100),'r',lw=0.5)
    ax3.plot(65*L23be[i]/np.max(np.abs(L23be[1:]))+(i*100),'b',lw=0.5)
    ax4.plot(65*L23ai[i]/np.max(np.abs(L23ai[1:]))+(i*100),'r',lw=0.5)
    ax4.plot(65*L23bi[i]/np.max(np.abs(L23bi[1:]))+(i*100),'b',lw=0.5)
plt.show()