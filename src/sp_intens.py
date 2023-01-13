import numpy as np
import glob
import os
from scipy import integrate
import scipy.special as sps
import numpy as np

lim_const=np.power(10,3)
Epsrel=1.49e-03

vc = 4/3.0*np.pi

def volume_in_range_integrand(Rg):
    return pdf(Rg)*sp_volume(Rg)

def int_for_valuate():
    func =  NDF*sp_volume(vector_rg)
    return np.trapz(func, vector_rg)
#    return integrate.quad(func, r_min, r_max)[0] 

def sp_factor(x):
    return np.power(3*((np.sin(x) - x*np.cos(x))/(x)**3),2)

"""

def pdf(Rg):
    #y=np.power(Rg,shape-1)*np.exp(-Rg/scale) /(sps.gamma(shape)*np.power(scale,shape))
    #np.savetxt("./rg_fr.txt", np.transpose([Rg,y]))
    return np.power(Rg,shape-1)*np.exp(-Rg/scale) /(sps.gamma(shape)*np.power(scale,shape))
"""
def pdf(Rg):
    #interpolate.CubicSpline(M[:,6], M[:,7], axis=0, bc_type='not-a-knot', extrapolate=None)
    return np.interp(Rg,vector_rg, NDF)
    #return np.power(Rg,shape-1)*np.exp(-Rg/scale) /(sps.gamma(shape)*np.power(scale,shape))


def sp_volume(Rg):
    return vc*np.power(Rg,3)


def full_intens(q):
    integrand_func = NDF * sp_factor(q*vector_rg) * np.power(sp_volume(vector_rg),2)
    #r = np.linspace(r_min,r_max,100)
    #y = pdf(r)
    #np.savetxt("./rg_fr.txt", np.transpose([r,y]))
    return np.trapz(integrand_func, vector_rg)
#    return integrate.quad(integrand_func, r_min, r_max, limit = 100)[0]


def sum_intens(q,rvect):
    s=0
    for r in rvect:
        s+=sp_factor(q * r) * np.power(sp_volume(r),2)
    return s


#A = NC*vc*np.power(r_global,3) / int_for_valuate()
NDF = None
vector_rg = None
RMIN= None
RMAX = None





    



