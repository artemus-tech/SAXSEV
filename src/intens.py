# -*- coding: utf-8 -*-
import numpy as np
import cast as ct
from single_body import  *


class Intens():
    def __init__(self):
        self.numRg = 80
        self.numTHETTA = 100
        self.startTHETTA = 0.0005#rad
        self.endTHETTA = 0.05#rad
        self.startRg = 1
        self.endRg = 60
        # Radius of Geration
        self.Rg = ct.gen_args(self.startRg ,self.endRg, num=self.numRg, grid="log", base = 1)    #log-step for Rg-collection elements
        # Scatterign angle, mrad
        self.THETTA = np.linspace(self.startTHETTA ,self.endTHETTA, num=self.numTHETTA)
        # Wave length const, nm
        self.lb = 0.1542
        # Scatterign vector,nm
        self.q  = ct.scat_vect(self.THETTA, m=1)
        self.betta = 0.4
        self.gamma = 15
        self.const = 0.001

    """VOLUME"""    
    def ell_volume( self, Rg, epsilon):
        return self.ell_const3*Rg**3

    """PDF"""    
    def single_mode_pdf(self, Rg):
        return Rg**5*np.exp(-self.betta*Rg)

    def double_mode_pdf(self,Rg):
        if Rg<self.gamma:
            second_mode = 0
        else:
           second_mode = (Rg - self.gamma)**5*np.exp(-self.betta*(Rg-self.gamma))
        first_mode = Rg**5*np.exp(-self.betta*Rg)
        return first_mode + second_mode

    """SINGLEBODY"""
    def get_intens_sb(self, q, Rg, eps):
        """
        SB = SingleBody(q, float(Rg))    #create SingleBody-class object

        SB.ell_const1 = SB.rg * self.ell_const1
        SB.ell_const2 = self.ell_const2

        sb_data = SB._ell_quad(q)
        return sb_data[0]
        """

        SingleBody.ell_const1 = Rg * self.ell_const1
        SingleBody.ell_const2 = self.ell_const2

        sb_data = SingleBody.ell_quad(q)
        return sb_data[0]



    def get_intens_ell(self,epsilon):

        eps=float(epsilon)

        self.ell_const1 = (5/(2.0+eps**2))**0.5     
        self.ell_const2 = eps**2-1
        self.ell_const3 = 4.0/3.0*np.pi*epsilon*self.ell_const1**3

        self.I = []
        for q in self.q:
            self.I.append(quad(lambda Rg :  self.ell_volume(Rg, epsilon)*self.double_mode_pdf(Rg)*self.get_intens_sb(q, Rg, epsilon) ,0, np.inf))
        return self.const * np.array(self.I)[:,0]
"""
epsilon=[0.5,0.75,1.0,1.25,1.5,1.75,2]
for eps in epsilon:
    I = Intens()
    i1 = I.get_intens_ell(eps)
    np.savetxt("../input/unittest/idata"+str(eps)+".txt",np.transpose([I.q,i1]))
    print("eps:"+str(eps)+" OK")
"""
I = Intens()
np.savetxt("../input/unittest/grid.txt",np.transpose([I.Rg]))
