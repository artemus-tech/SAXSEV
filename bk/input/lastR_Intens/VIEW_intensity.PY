import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import glob 
import re
tpl = "./vrija*/intens*.txt"

fig,ax = plt.subplots()


markers = ['.','p','*','^','+','D','_','x','o','|','s']

lastPOINT = 10

c=0
for f in glob.glob(tpl):
    print(f)
    m = np.loadtxt(f)
    row ,col= m.shape

    lastpointCurrent = m[row-1,1]

    relmulti = lastPOINT/lastpointCurrent

    labelTitle = re.search('NC=(.+?)_shape', f)

    Iout = relmulti *m[:,1]
   
    ax.plot(m[:,0],    Iout, label=labelTitle.group(1),marker=markers[c])

    c+=1
    np.savetxt("./SAXSEVPrepare/"+"Intensity_for_NC="+str(labelTitle.group(1))+".txt", np.c_[m[:,0],Iout, np.sqrt(Iout),np.sqrt(Iout)])

ax.set_xlabel('q, $nm^{-1}$')    
ax.set_ylabel('I(q), arb. u.')    
#ax.set_xlabel(
#ax.set_ylim(np.power(10,7), np.power(10,8))

ax.set_title('Интенсивность рассеяния при разной доли рассеивающего вещества')
ax.legend()
ax.loglog()
plt.show()



