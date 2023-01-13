# -*- coding: utf-8 -*-
import numpy as np
import cast as ct

class Surface:

    def __init__(self, rg, vfdf, vfdf_ambiguity): 
        """initialize methods""" 
        self.vfdf = vfdf
        self.rg = rg
        self.vfdf_amb = vfdf_ambiguity
        self.amb = None
      
    def cil(self,exc = 1):
        """the specific surface area evaluation for cylindrical shape"""
        exc = float(exc)
        cilCoef = (2+4*exc) / (exc*np.sqrt(24.0/(3.0+2.0*exc**2)))
        self.amb = self.__amb()
        return cilCoef * self.__interp()

    def par(self,exc = 1):
        """the specific surface area evaluation for parallelepiped shape"""
        exc = float(exc)
        parCoef = (2+4*exc) / (exc*np.sqrt(12.0/(2.0+exc**2)))
        self.amb = self.__amb()
        return parCoef * self.__interp()
    
    def ell(self,exc = 1):
        """the specific surface area evaluation for ellipsoidal shape"""
        exc = float(exc)
        ellCoef=np.sqrt(5.0/(exc**2+2)) * exc
        self.amb = self.__amb()
        if exc < 1:
            aniFlat = (1 + np.sqrt(1-exc**2))/exc
            ellFlatCoef = 3*( 1 + exc**2/np.sqrt(1-exc**2) * np.log(aniFlat)  )   / ( 2.0 * ellCoef)
            return ellFlatCoef * self.__interp()
        if exc > 1 :
            aniLong = np.sqrt(exc**2 - 1)/exc
            ellLongCoef = 3*( 1 + exc/aniLong * np.arcsin(aniLong ) ) / ( 2.0 * ellCoef)
            return ellLongCoef * self.__interp()           
        if exc == 1:
            spCoef = 3*np.sqrt(3.0/5.0)
            return spCoef * self.__interp()
            

    def __interp(self):
        """integration with trapezoid method"""
        numerator  = np.trapz(self.vfdf/self.rg,self.rg)
        denominator = np.trapz(self.vfdf,self.rg)
        return numerator/denominator

    def __amb(self):
        """estimation Ambiguity for trapezoid method"""
        self.C = ct.custom_trapezoid_coef(self.rg)
        n, = self.rg.shape
        a = min(self.rg)
        b = max(self.rg)
        #integral sum for trapezoid method
        sIsum=0
        vIsum=0
        for i in range(1,n-1):
            vIsum +=self.C[i]*self.vfdf[i]
            sIsum +=self.C[i]*self.vfdf[i]/float(self.rg[i])

        fa=self.vfdf[0]
        fb=self.vfdf[n-1]

        self.__S = self.C[0]*fa/float(a) + self.C[n-1]*fb/float(b) + sIsum
        self.__V = self.C[0]*fa + self.C[n-1]*fb + vIsum

        amb=0
        for k in range(1,n):
            amb += (self.vfdf_amb[k]*self.C[k]/self.__V * (1/self.rg[k] - self.__S/self.__V))**2
        return np.sqrt(amb) 
