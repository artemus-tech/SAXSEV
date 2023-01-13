# -*- coding: utf-8 -*-
import os
import shutil
import numpy as np
from single_body import SingleBody
import config as cfg
import cast as ct
import scipy as scp
import sp_vrija_no_volumeComplex_2N200723 as vrij

class VFDF(SingleBody):




    def __init__(self, intens, q, rg_arr, intens_ambiguity = None, alpha=None):
        self.q = q
        self.rg_arr = rg_arr
        self.intens = intens
        self.q_num = len(self.q)
        self.rg_num =len(self.rg_arr) 
        self.delta = np.eye(self.q_num) 
        self.intens_ambiguity = intens_ambiguity if np.any(intens_ambiguity) else np.sqrt(np.abs(intens))

        if np.any(self.intens_ambiguity):
            print("SHUMMM")
        else:
            print("NOT SHUM")

        self.vfdf_dir_pref = cfg.options["vfdf_dir_pref"]
        # params for generated array for regulasation param alpha
        if alpha == None:
            alpha_start =     float(cfg.options["default_alpha_start"])
            alpha_end   =     float(cfg.options["default_alpha_end"])
            alpha_num   =     int(cfg.options["default_alpha_num"])
            alpha_base  =     float(cfg.options["default_alpha_base"])
            # generate alpha-vector  
            self.alpha = np.logspace(alpha_start ,alpha_end , num=alpha_num, base=alpha_base)
        else:
            self.alpha = np.array([alpha])

        # coefficients
        self.coef = self.__coef_eval()
        self.d_coef = self.__d_coef_eval()

    def __coef_eval(self):
        coef=[]
        coef.append(0.5*(self.rg_arr[1] - self.rg_arr[0]))
        for j in range(1,self.rg_num-1):
            coef.append(0.5*(self.rg_arr[j+1] - self.rg_arr[j-1]))
        coef.append(0.5*(self.rg_arr[self.rg_num-1] - self.rg_arr[self.rg_num-2]))
        return coef

    def __d_coef_eval(self):
        coef=[]
        coef.append(0.5*(self.rg_arr[2] - self.rg_arr[1]))
        for j in range(2,self.rg_num-2):
            coef.append(0.5*(self.rg_arr[j+1] - self.rg_arr[j-1]))
        coef.append(0.5*(self.rg_arr[self.rg_num-2] - self.rg_arr[self.rg_num-3]))
        return coef

      
    def __coef_addon(self,K):
        for i in range(len(self.coef)):
            K[:,i] = self.coef[i]*K[:,i]
        return K

    def restore_ell(self,epsilon):    
        """restore distribution using ellipsoid particle form factor"""
        volume_coef=4*np.pi/3.0*(5.0/(2.0 + epsilon**2))**1.5
        self.k_matrix = epsilon*np.mat([volume_coef*self.rg**3*np.array(self.get_scat_intens_from_ell(epsilon))[:,0] for self.rg in self.rg_arr]).T
        self.k_matrix = self.__coef_addon(self.k_matrix)
        self.sigma  = self.delta/np.power(self.intens_ambiguity, 2)
        self.b_matrix = self.k_matrix.T * self.sigma * self.k_matrix
        self.omega_matrix  = ct.gen_hessian(self.rg_arr, self.d_coef)
        self.__mk_dir("ellipsoid_" + str(epsilon))
        self.__estimate(self.alpha[0])
        return list(map(self.__estimate,self.alpha))
                                                                                 
    def restore_cil(self,epsilon):    
        """restore distribution using cilindr particle form factor"""
        VFactor=np.pi/4.0*(24.0/(3.0+2*epsilon**2))**1.5
        self.k_matrix = epsilon*np.mat([VFactor*self.rg**3*np.array(self.get_scat_intens_from_cil(epsilon)) for self.rg in self.rg_arr]).T 
        self.k_matrix = self.__coef_addon(self.k_matrix)
        self.sigma = self.delta/np.power(self.intens_ambiguity, 2)
        self.b_matrix = self.k_matrix.T * self.sigma * self.k_matrix
        self.omega_matrix  = ct.gen_hessian(self.rg_arr, self.d_coef)
        self.__mk_dir("cilindr_" + str(epsilon))
        return list(map(self.__estimate,self.alpha))

    def restore_par(self,epsilon):    
        """restore distribution using paralelipiped particle form factor"""
        volume_coef=(12.0/(2.0+epsilon**2))**1.5
        self.k_matrix = epsilon*np.mat([volume_coef*self.rg**3*np.array(self.get_scat_intens_from_par(epsilon))[:,0] for self.rg in self.rg_arr]).T 
        self.k_matrix = self.__coef_addon(self.k_matrix)
        self.sigma = self.delta/np.power(self.intens_ambiguity, 2)
        self.b_matrix = self.k_matrix.T * self.sigma * self.k_matrix
        self.omega_matrix  = ct.gen_hessian(self.rg_arr, self.d_coef)        
        self.__mk_dir("paralellipiped_" + str(epsilon))
        return list(map(self.__estimate,self.alpha))

    def __mk_dir(self,ft):
        """create directory which will store results"""
        self.vfdf_dir = self.vfdf_dir_pref +"_"+ ft 
        if not os.path.exists(self.vfdf_dir):
            os.makedirs(self.vfdf_dir)
        else:
            self.__clear_dir(self.vfdf_dir)

    def __clear_dir(self,dir_path):
        """delete all directory contents"""
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                proof = os.path.join(root, f)
                if "vrija" not in proof:
                    os.remove(os.path.join(root, f))
                
            for d in dirs:
                if "vrija" not in d:
                    shutil.rmtree(os.path.join(root, d))
        
    def entropy(self,V):
        ent=[]
        for i in range(1,len(V)-1):
            m = np.mean([V[i-1],V[i+1]])
            ent.append(-V[i]*np.log(V[i]/m)+V[i]-m)
        return np.abs(np.sum(ent))
  
    def __estimate(self, alpha):
        f = self.b_matrix + alpha * self.omega_matrix

        print(self.alpha)
        f_inverse = f.I            
        vfdf = f_inverse * self.k_matrix.T * self.sigma * np.mat(self.intens).T       
        vfdf_nonnegative = vfdf.clip(min=0)
        vfdf_nonnegative_valuate = ct.valuate(vfdf_nonnegative)
        vfdf_nonnegative_trapzNormaValuate = np.array(ct.valuateVolume(self.rg_arr,vfdf_nonnegative))       
        t=ct.valuate(vfdf_nonnegative)
        vfdf_valuate = np.transpose(ct.valuate(vfdf))
        vfdf_positivity  =  1 - np.linalg.norm(vfdf_nonnegative)/np.linalg.norm(vfdf)
        vfdf_ambiguity = np.sqrt(np.diag(f_inverse)) 
        # intensity
        intens_from_vfdf = self.k_matrix*vfdf
        vfdfConverted_nonValuate = np.divide ( np.reshape(vfdf_nonnegative [:,0], np.shape(self.rg_arr)[0]) * np.sqrt(3.0/5.0) / (4*np.pi/3.0*(5.0/3.0)**1.5),self.rg_arr**3)
        intens_from_vfdf_converted = self.k_matrix*np.transpose(vfdfConverted_nonValuate)
        intens_from_nonnegative_vfdf = self.k_matrix*vfdf_nonnegative 
        
        vfdfConverted = np.array(vfdf_nonnegative_valuate) * np.sqrt(3.0/5.0) / (4*np.pi/3.0*(5.0/3.0)**1.5)/self.rg_arr**3
        norm = np.trapz(vfdfConverted, self.rg_arr*np.sqrt(5.0/3.0))
        vfdfConverted = vfdfConverted/norm

        # estimation function
        fi = np.sum(np.power(np.divide(np.subtract(self.intens,intens_from_vfdf.T),self.intens_ambiguity),2))/self.q_num
        fi0 = np.sum(np.power(np.divide(np.subtract(self.intens,intens_from_nonnegative_vfdf.T),self.intens_ambiguity),2))/self.q_num
        sqd = np.mat(vfdf).T*self.omega_matrix * np.mat(vfdf)
        print("==========================SQD==========================")
        print(sqd)
        print("==========================SQD==========================")
        
        np.savetxt( self.vfdf_dir + "/vfdf_"+str(alpha) + "_fi=" + str(fi) + "_fiplus=" + str(fi0)+"_sqd=" + str(sqd)  + "_Rg["+str(self.rg_arr[0])+","+str(self.rg_arr[self.rg_num-1]) + "]@Rg_vfdf_vfdfVal_vfdfPos_vfdfPosVal_vfdfAmbiguity_R_VFDFR_trapzNormaValuate.txt",np.c_[self.rg_arr, vfdf, vfdf_valuate, vfdf_nonnegative, vfdf_nonnegative_valuate, vfdf_ambiguity, self.rg_arr*np.sqrt(5.0/3.0), vfdfConverted,vfdf_nonnegative_trapzNormaValuate])
        np.savetxt( self.vfdf_dir + "/i[vfdf]_" + str(alpha) + "_fi=" + str(fi) + "_fiplus=" + str(fi0) + "_Rg["+str(self.rg_arr[0])+","+str(self.rg_arr[self.rg_num-1])+"_" + str(fi) + "]@Q_IResPos_IRes_ISrc_IAmb_IvdfNV.txt",np.c_[self.q,intens_from_nonnegative_vfdf,intens_from_vfdf,self.intens, self.intens_ambiguity, intens_from_vfdf_converted])
        #-------output
        #[self.rg_arr, vfdf, vfdf_valuate, vfdf_nonnegative, vfdf_nonnegative_valuate, vfdf_ambiguity, self.rg_arr*np.sqrt(5.0/3.0), vfdfConverted,vfdf_nonnegative_trapzNormaValuate]
        #output = [self.rg_arr, vfdf, vfdf_valuate, vfdf_nonnegative, vfdf_nonnegative_valuate, vfdf_ambiguity, self.rg_arr*np.sqrt(5.0/3.0), vfdfConverted,vfdf_nonnegative_trapzNormaValuate]


        return [alpha,fi,fi0, sqd.item(),vfdf_positivity] 
