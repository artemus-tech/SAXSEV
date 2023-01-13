import matplotlib.pyplot as plt
import numpy as np
import glob 
import re
import os

tpa = "./vrija*/"
tp2 = "./intens*.txt"
tp3 = "./selected_Rg_VFDF*.txt"

fig,ax = plt.subplots()

lastPOINT = 10

for dn in glob.glob(tpa):
    print(dn)
    os.chdir(dn)
    fInt = glob.glob(tp2)[0]
    fVFD = glob.glob(tp3)[0]
    m = np.loadtxt(fVFD)
    #row ,col= m.shape

    #lastpointCurrent = m[row-1,1]

    #relmulti = lastPOINT/lastpointCurrent
    

    labelTitle = re.search('NC=(.+?)_shape', fInt)
    MaxF = np.max(m[:,1])
    VFDout = m[:,2]/MaxF
    ax.plot(m[:,0],    VFDout, label=labelTitle.group(1))
    
    os.chdir("../")
       
    np.savetxt("./SAXSEVPrepare/"+"VFDF_vs_RG_for_NC="+str(labelTitle.group(1))+".txt", np.c_[m[:,0],VFDout])

m0 = np.loadtxt("VFD_vs_Rg_with_shape=6_scale=2.5_.txt")
MaxF0 = np.max(m0[:,1])
VFD0 = m0[:,1]/MaxF0
ax.plot(m0[:,0],    VFD0, label="исходная ФР")

ax.set_xlabel('Rg, $nm$')    
ax.set_ylabel('VFDF, arb. u.')    
#ax.set_ylim(np.power(10,7), np.power(10,8))

ax.set_title('Восстановленная Ф. распределения об. долей при разной доли рассеивающего вещества')
ax.legend()
#ax.loglog()
plt.show()



