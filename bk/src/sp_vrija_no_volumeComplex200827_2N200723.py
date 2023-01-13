import numpy as np
"""to enable color mapping"""
import glob
import os
import fnmatch
from scipy import integrate
import scipy.special as sps

lim_const=np.power(10,4)
Epsrel=1.49e-06

   
def get_Vsp(R):
    return 4.0/3.0*np.pi*np.power(R,3)
    
def get_Vmean():
    Vfunc = lambda r: pdf(r)*get_Vsp(r)    
    all_vol = integrate.quad(Vfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    pdffunc = lambda r: pdf(r)
    norm_pdf = integrate.quad(pdffunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return all_vol/norm_pdf    
    
def get_RGlob(nc):
    meanfunc = lambda r: r**3*pdf(r)
    mean_int = integrate.quad(meanfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   np.sqrt(mean_int/nc)

def ksi(nu):
    meanfunc = lambda r: pdf(r)*np.power(2*r,nu)
    mean_int = integrate.quad(meanfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return c*mean_int
    #return np.pi/(6.0*get_Vsp(Rglob))*np.sum(np.power(2*r,nu))

def Psi(X):
    return np.sinc(X/np.pi)

def Fi(X):
    return (3.0/(X)**3.0*(np.sin(X)-X*np.cos(X)))

def mean_dnu_eiX_Fi(q,nu):
    meanfuncRE = lambda r: pdf(r)*np.power(2*r,nu)*np.cos(q*r)*Fi(q*r)
    mean_intRE = integrate.quad(meanfuncRE, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    meanfuncIM = lambda r: pdf(r)*np.power(2*r,nu)*np.sin(q*r)*Fi(q*r)
    mean_intIM = integrate.quad(meanfuncIM, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   c*(mean_intRE + 1j*mean_intIM)

def mean_dnu_eiX_Psi(q,nu):
    meanfuncRE = lambda r: pdf(r)*np.power(2*r,nu)*np.cos(q*r)*Psi(q*r)
    mean_intRE = integrate.quad(meanfuncRE, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    meanfuncIM = lambda r: pdf(r)*np.power(2*r,nu)*np.sin(q*r)*Psi(q*r)
    mean_intIM = integrate.quad(meanfuncIM, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   c*(mean_intRE + 1j*mean_intIM)

def F11(q):
    return 1- ksi(3) + mean_dnu_eiX_Fi(q,3)

def F12(q):
    return mean_dnu_eiX_Fi(q,4)
       
def F22(q):
    return 1- ksi(3) + 3.0*mean_dnu_eiX_Psi(q,3)

def F21(q):
    return 0.5*(1- ksi(3))*1j*q - 3.0*ksi(2) + 3.0*mean_dnu_eiX_Psi(q,2)

def DeltaK(q):
    return np.power(1- ksi(3),-4)*np.abs(F11(q)*F22(q)-F12(q)*F21(q))**2

def B(q,r):
    X = q*r
    return (3.0/(X)**3.0*(np.sin(X)-X*np.cos(X)))

def f(r):
    return get_Vsp(r)

def mean_f_B_eiX(q):
    meanfuncRE = lambda r: pdf(r)*f(r)* B(q,r) * np.cos(q*r)
    mean_intRE = integrate.quad(meanfuncRE, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    meanfuncIM = lambda r: pdf(r)*f(r)* B(q,r) * np.sin(q*r)
    mean_intIM = integrate.quad(meanfuncIM, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   c*(mean_intRE + 1j*mean_intIM)
                                                                           
def mean_d_f_B_eiX(q):
    meanfuncRE = lambda r: pdf(r)*(2*r)* f(r)* B(q,r) * np.cos(q*r)
    mean_intRE = integrate.quad(meanfuncRE, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    meanfuncIM = lambda r: pdf(r)*(2*r)* f(r)* B(q,r) * np.sin(q*r)
    mean_intIM = integrate.quad(meanfuncIM, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   c*(mean_intRE + 1j*mean_intIM)


def T1(q):
    return F11(q)*F22(q)-F12(q)*F21(q)

def T2(q):
    return F21(q)*mean_d_f_B_eiX(q)-F22(q)*mean_f_B_eiX(q)

def T3(q):
    return F12(q)*mean_f_B_eiX(q)-F11(q)*mean_d_f_B_eiX(q)


def pdf(Rg):
    #interpolate.CubicSpline(M[:,6], M[:,7], axis=0, bc_type='not-a-knot', extrapolate=None)
    return np.interp(Rg,vector_rg, NDF)/norm
    #return np.power(Rg,shape-1)*np.exp(-Rg/scale) /(sps.gamma(shape)*np.power(scale,shape))

def mean_f2_B2(q):
    meanfunc = lambda r: pdf(r)*f(r)**2 * B(q,r)**2
    mean_int = integrate.quad(meanfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return c*mean_int    

def mean_d6_Fi2(q):
    meanfunc = lambda r: pdf(r)*(2*r)**6 * Fi(q*r)**2
    mean_int = integrate.quad(meanfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return c*mean_int 
    #np.sum((2*r)**6 * Fi(X)**2)

def mean_d4_Psi2(q):
    meanfunc = lambda r: pdf(r)*(2*r)**4 * Psi(q*r)**2
    mean_int = integrate.quad(meanfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   c*mean_int
    #np.sum((2*r)**4 * Psi(X)**2)

def mean_f_B_d3_Fi(q):
    meanfunc = lambda r: pdf(r)*f(r)* B(q,r) * (2*r)**3*Fi(q*r)
    mean_int = integrate.quad(meanfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   c*mean_int
    #X = q*r
    #np.sum(f(r)* B(q,r) * (2*r)**3*Fi(X))

def mean_f_B_d2_Psi(q):
    meanfunc = lambda r: pdf(r)*f(r)* B(q,r) * (2*r)**2*Psi(q*r)
    mean_int = integrate.quad(meanfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   c*mean_int
    #X = q*r
    #np.sum(f(r)* B(q,r) * (2*r)**2*Psi(X))

def mean_d5_FiPsi(q):
    meanfunc = lambda r: pdf(r)*(2*r)**5*Fi(q*r)*Psi(q*r)
    mean_int = integrate.quad(meanfunc, RMIN, RMAX, limit=lim_const,epsabs=Epsrel, epsrel=Epsrel)[0]
    return   c*mean_int
    #np.sum((2*r)**5*Fi(X)*Psi(X))

def Df(q):
    AA = mean_f2_B2(q)*np.abs(T1(q))**2
    BB = mean_d6_Fi2(q)*np.abs(T2(q))**2
    CC = 9.0*mean_d4_Psi2(q)*np.abs(T3(q))**2
    DD = mean_f_B_d3_Fi(q)*2*np.real(T1(q)*np.conj(T2(q)))
    EE = 3.0*mean_f_B_d2_Psi(q)*2*np.real(T1(q)*np.conj(T3(q)))
    FF = 3.0*mean_d5_FiPsi(q)*2*np.real(T2(q)*np.conj(T3(q)))
    return (AA + BB + CC + DD + EE + FF)/(-np.pi/6*(1- ksi(3))**4) 

def sum_intens_vrija(q):
    return -Df(q)/DeltaK(q)


#MATH END HERE
NC = None
NDF = None #np.loadtxt("./data200724/1_vfdf_0.00019952623149688828Rg_vfdf_vfdfVal_vfdfPos_vfdfPosVal_vfdfAmbiguity_R_VFDFR_trapzNormaValuate.txt")
RMIN =  None # np.min(NDF[:,6])
RMAX =  None #np.max(NDF[:,6])
norm = None # numpy.trapz(NDF[:,7], NDF[:,6])
#NC= 0.000002
# NCarr=[0.000002,0.00002,0.0002,0.002,0.02,0.2,0.3,0.4,0.5]
#shape = 0.0
#scale = 0.0
shape = 6.0
scale = 2.5

#Rglob = get_RGlob(NC)
#SV = get_Vsp(Rglob)
#c = np.pi*NC/(6.0*get_Vmean())
#c = np.pi/(6.0*get_Vsp(Rglob))


#M2 = np.loadtxt("./data200724/no_volume_vrija_NC=0.2_shape=6.0scale=0.2.txt")
 
"""
vrija = []

mono="./data200724/_vrijaREIM"+"_NC="+str(NC)+"_Rgl="+str(round(Rglob, 1))+"_shape="+str(shape)+"scale="+str(scale)+'.txt'
print(mono)
for q in M2 [:,0]:
    vrija.append(sum_intens_vrija(q))
    print(q)
  
np.savetxt( mono,np.array([np.array(M2 [:,0]),SV*np.array(vrija)]).T)
"""
"""
for NC in NCarr: 
    c = np.pi*NC/(6.0*get_Vmean())
    vrija = []
    mono="./data200724/no_volume_vrija_"+"NC="+str(NC)+"_shape="+str(shape)+"scale="+str(scale)+'.txt'
    print(mono)
    for q in M2[:,0]:
        vrija.append(sum_intens_vrija(q))
        print(q)
    np.savetxt( mono,np.array([M2[:,0],np.array(vrija),np.sqrt(vrija)]).T)
"""
