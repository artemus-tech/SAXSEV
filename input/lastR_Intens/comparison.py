import matplotlib.pyplot as plt
# -*- coding: utf-8 -*-
import numpy as np
import cast as ct
import glob

#data1  =np.loadtxt("vfdf_0.9440608762859226_fi=0.026845068024904602_fiplus=333459.83224689314_sqd=[[1113.63664419]]_Rg[0.2843876326121044,87.47006162457019]@Rg_vfdf_vfdfVal_vfdfPos_vfdfPosVal_vfdfAmbiguity_R_VFDFR_trapzNormaValuate.txt")
#data2  =np.loadtxt("vfdf_1.778279410038923e-05_fi=0.002584366916902624_fiplus=350524.5167125773_sqd=[[1321.47210149]]_Rg[0.2843876326121044,87.47006162457019]@Rg_vfdf_vfdfVal_vfdfPos_vfdfPosVal_vfdfAmbiguity_R_VFDFR_trapzNormaValuate.txt")


def compare(data1,data2):
    xmin = np.amax([np.amin(data1[:,0]),np.amin(data2[:,0])])
    xmax = np.amin([np.amax(data1[:,0]),np.amax(data2[:,0])])

    grid = np.linspace(xmin,xmax,1000)

    f1 = np.interp(grid, data1[:,0], data1[:,1]/np.max(data1[:,1]))
    f2 = np.interp(grid, data2[:,0], data2[:,2]/np.max(data2[:,2]))

    F1= ct.norm_distr(grid, f1)
    F2= ct.norm_distr(grid, f2)

    return ct.norm_distr(grid,f1-f2)/F1





etalonData = np.loadtxt("./VFD_vs_Rg_with_shape=6_scale=2.5_.txt")

res=[]
for f in glob.glob("./vrija*/selec*"):
    print(f)
    data = np.loadtxt(f)   
    res.append(compare(etalonData,data))
print(res)
nc=[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4]

fig,ax = plt.subplots()

labelTitle = "title"
ax.grid(1)
ax.plot(nc, res)
plt.show()
