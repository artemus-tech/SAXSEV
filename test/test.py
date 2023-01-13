# -*- coding: utf-8 -*-
import numpy as np
import scipy.special as sps       
from scipy.integrate import quad, dblquad
import cast as ct

class SingleBody:
    """Class that generate scattering intensity from single particle""" 
    def __init__(self, q, rg):
        """To construct object of this class necessary passing of two args: rg, and vector of angles"""
        self.rg = float(rg)
        self.q = q

    def _par_quad(self,q):
        c1 = q*self.par_const1
        c2 = q*self.par_const2
        c3 = q*self.par_const3
        c4 = self.par_const4
        return dblquad(lambda x,y:c4*(
                                  np.sin(c1*x)*
                                  np.sin(c2*(1-x**2)**0.5*np.sin(y))*
                                  np.sin(c3*(1-x**2)**0.5*np.cos(y))/(c1*c2*c3*x*(1-x**2)*np.sin(y)*np.cos(y)))**2,
                                  0,0.5*np.pi,lambda x:0,lambda x :1,epsabs=1.49e-03)

    def get_scat_intens_from_par(self, epsilon):
        """method to evaluate vector intensity for paralellipiped-particle, input params coef of anisometry."""
        eps = float(epsilon)
        self.par_const1 = 0.5*self.rg*(12/(2.0+eps**2))**0.5*eps
        self.par_const2 = 0.5*self.rg*(12/(2.0+eps**2))**0.5
        self.par_const3 = 0.5*self.rg*(12/(2.0+eps**2))**0.5
        self.par_const4 = 2.0/np.pi
        return list(map(self._par_quad, self.q))

    def _cil_quad(self,q):
        c1 = q*self.cil_const1
        c2 = q*self.cil_const2
        return  quad(lambda x : 4*(sps.j1(c1*(1-x**2)**0.5)/(c1*(1-x**2)**0.5)*np.sin(c2*x)/(c2*x))**2,0,1)

    def get_scat_intens_from_cil(self, epsilon):
        """method to evaluate vector intensity for cilindr-particle, input params coef of anisometry."""
        eps=float(epsilon)
        self.cil_const1=(self.rg*(24/(3.0+2*eps**2))**0.5)/2
        self.cil_const2=self.cil_const1*eps 
        return list(map(self._cil_quad, self.q))
 

    def _ell_quad(self,q):
        c1 = q * self.ell_const1
        c2 = self.ell_const2
        return  quad(lambda x : 9*((np.sin(c1*(1+c2*x**2)**0.5) - c1*(1+c2*x**2)**0.5*np.cos(c1*(1+c2*x**2)**0.5))/(c1*(1+c2*x**2)**0.5)**3)**2,0,1)


    def get_scat_intens_from_ell(self, epsilon):
        """method to evaluate vector intensity for ellipsoid-particle, input params coef of anisometry."""
        eps=float(epsilon)     
        self.ell_const1 = self.rg*(5/(2.0+eps**2))**0.5
        self.ell_const2 = eps**2-1
        return list(map(self._ell_quad, self.q))



# Scatterign vector,nm
#numTHETTA   = 100
#startTHETTA = 0.004
#endTHETTA   = 0.02
#THETTA = np.linspace(startTHETTA, endTHETTA, numTHETTA)
# Wave length const, nm
#q  = ct.scat_vect(THETTA, m=1) #mrad

x0=0.004
xn=0.2
#q=np.logspace(np.log(x0), np.log(xn), 100, base=np.e)
q=np.arange(x0, xn,0.001)
print(q)
#print(np.shape(q))
#q=np.linspace(x0, xn,100)
sb= SingleBody(q, 4.0)#nm
buf = np.mat(sb.get_scat_intens_from_ell(1))

#print(buf[:,0])
#np.concatenate([buf[:,0],buf[:,1]])
res = np.column_stack([buf[:,0],q])#buf[:,1]])
#print(res[::-1])
print(res)
#print(np.shape(res))
#print(buf[:,0][99],",",buf[:,1][99])

