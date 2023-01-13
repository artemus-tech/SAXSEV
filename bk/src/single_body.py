# -*- coding: utf-8 -*-
import numpy as np
import scipy.special as sps       
from scipy.integrate import quad, dblquad
import cast as ct

class SingleBody:
    """Class that generate scattering intensity from single particle""" 
    def __init__(self, q, rg):#, to_q = False):
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
 

    @staticmethod
    def ell_quad(q):
        c1 = q * SingleBody.ell_const1
        c2 = SingleBody.ell_const2
        return  quad(lambda x : 9*((np.sin(c1*(1+c2*x**2)**0.5) - c1*(1+c2*x**2)**0.5*np.cos(c1*(1+c2*x**2)**0.5))/(c1*(1+c2*x**2)**0.5)**3)**2,0,1)




    def get_scat_intens_from_ell(self, epsilon):
        """method to evaluate vector intensity for ellipsoid-particle, input params coef of anisometry."""
        eps=float(epsilon)     
        SingleBody.ell_const1 = self.rg*(5/(2.0+eps**2))**0.5
        SingleBody.ell_const2 = eps**2-1
        return list(map(SingleBody.ell_quad, self.q))