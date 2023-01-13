# -*- coding: utf-8 -*-
import numpy as np
import glob
import cast as ct
import config as cfg

class PerceptCriteria:
    def __init__(self, vfdf_str = "vfdf", ivfdf_str = "i[vfdf"):
        self.file_ext = ".txt"
        self.vfdf_str = vfdf_str + "*" + self.file_ext
        self.ivfdf_str = ivfdf_str + "*" + self.file_ext
        self.vfdf_files = [file_name for file_name in sorted(glob.glob(self.vfdf_str), key=ct.get_alpha_from_filename)]
        self.ivfdf_files = [file_name for file_name in sorted(glob.glob(self.ivfdf_str), key=ct.get_alpha_from_filename)]
     
    def check_valcen(self, rg_arr, vfdf):
        """
        VALCEN
        """
        rgNum = len(rg_arr)
        vfdf_cut=[]
        delta_rg = rg_arr[rgNum-1] - rg_arr[0]
        start = rg_arr[0] + 0.05*delta_rg
        end = rg_arr[rgNum-1] - 0.5*delta_rg
        for i in range(len(vfdf)):
            if rg_arr[i] < start or rg_arr[i] > end : 
                vfdf_cut.append(0)
            else:
                vfdf_cut.append(vfdf[i])
        return ct.norm_distr(rg_arr,vfdf_cut) / ct.norm_distr(rg_arr,vfdf)

    def check_stabil(self, alpha1, alpha2, rg, vfdf1, vfdf2):
        """
        STABIL
        """
        vfdf_delta=vfdf2-vfdf1
        res = ct.norm_distr(rg, vfdf_delta) / ct.norm_distr(rg, vfdf1)/ (alpha2 - alpha1) * alpha1
        alphaMean = np.average([alpha1,alpha2]) 
        return  {'alpha':alphaMean,'stabil':res}

    def check_sysdev(self, intens1, intens2):
        """
        SYSDEV
        """
        delta_intens=intens2-intens1
        ns=0
        for i in range(len(delta_intens)-1):
            if np.sign(delta_intens[i])!=np.sign(delta_intens[i+1]):
                ns+=1
        return ns/(len(delta_intens)/2.0)

    def check_errdev(self, intens1, intens2, intens_ambiguity, num=2):
        """
        ERRDEV
        """
        delta_intens=intens2-intens1
        ns=0
        for i in range(len(delta_intens)):
            if np.abs(delta_intens[i])>=num*intens_ambiguity[i]:
                ns+=1
        return ns/len(delta_intens)

    def check_oscil(self, rg_arr, vfdf):
        """
        OSCIL
        """
        delta_rg = rg_arr[len(rg_arr)-1]-rg_arr[0]
        der=[]
        delta_rg_arr=[]
        for i in range(len(rg_arr)-1):
            der.append((vfdf[i+1]-vfdf[i])/(rg_arr[i+1]-rg_arr[i]))
            delta_rg_arr.append(np.average([rg_arr[i],rg_arr[i+1]]))
        return ct.norm_distr(delta_rg_arr,der)/ct.norm_distr(rg_arr,vfdf)/(np.pi/delta_rg)
    
    def check_positiv(self, rg_arr, vfdf):
        """
        POSITIV
        """
        vfdf_positive=[]
        for i in range(len(vfdf)):
            if vfdf[i]<=0: 
                vfdf_positive.append(0)
            else:
                vfdf_positive.append(vfdf[i])
        return ct.norm_distr(rg_arr,vfdf_positive) / ct.norm_distr(rg_arr,vfdf)

    def check_impmin(self, fi, fi_nonnegative):
        """
        IMPMIN
        """
        return fi_nonnegative-fi


    def check_discrp(self, fi1, fi0):
        """
        DISCRP
        """
        return np.sqrt(np.abs(fi1**2-fi0**2))
   
    def check_total(self, v_act):
        """
        TOTAL
        """
        #w = {'DISCRP':3.0,'OSCIL':1.0,'STABIL':1.0,'SYSDEV':2.0,'POSITIV':1.0,'VALCEN':1.0,'ERRDEV':6.0, 'IMPMIN':6.0}       
        #c = {'DISCRP':0.2,'OSCIL':1.3,'STABIL':0.02,'SYSDEV':0.2,'POSITIV':0.01,'VALCEN':0.01,'ERRDEV':0.1,'IMPMIN':0.2}
        #a = {'DISCRP':0.7,'OSCIL':0.3, 'STABIL':0.0, 'SYSDEV':1.0, 'POSITIV':1.0, 'VALCEN':1.0,'ERRDEV':0.0,'IMPMIN':0.0}
        a = ct.dict_keys_to_upper(cfg.pc_a)
        c = ct.dict_keys_to_upper(cfg.pc_c)
        w = ct.dict_keys_to_upper(cfg.pc_w)
        t=0
        for key in v_act:
            t += w[key]*np.exp(-((a[key]-v_act[key])/c[key])**2)
        return 2*t/sum(w.values())
         
    def get_pc_dict(self):
        """Create stores dictionary of percept criteria"""                               
        norma_delta_inens_from_nonnegative_vfdf = []
        norma_delta_intens_src = []
        alpha = []
        vfdf_valuate = []
        intens_src = []
        intens_from_vfdf = []
        intens_from_nonnegative_vfdf = []
        intens_ambiguity = []
        rg = []
        stabil=[]
        total = []
        sysdev = []
        res = []
        for i in range(len(self.vfdf_files)):
            intens_src.append(ct.get_vect(self.ivfdf_files[i],'ISrc') )
            intens_from_vfdf.append(ct.get_vect(self.ivfdf_files[i],'IRes') )
            intens_ambiguity.append( np.sqrt(np.abs(intens_src[i])))
            norma_delta_intens_src.append( np.sqrt(np.sum(np.power(np.divide(np.subtract(intens_src[i],intens_from_vfdf[i]),intens_ambiguity[i]),2))/float(len(intens_src[i])-1)))
            
 
        
        for i in range(len(self.vfdf_files)):
            # extract corresponding vectors from each file
            alpha.append(float(self.vfdf_files[i].split('_')[1]))
            rg.append(ct.get_vect(self.vfdf_files[i],'Rg'))
            vfdf_valuate.append( ct.get_vect(self.vfdf_files[i],'vfdfVal'))
            
            #intens_src.append(ct.get_vect(self.ivfdf_files[i],'ISrc') )
            #intens_from_vfdf.append(ct.get_vect(self.ivfdf_files[i],'IRes') )
            intens_from_nonnegative_vfdf.append( ct.get_vect(self.ivfdf_files[i],'IResPos') )
            #intens_ambiguity.append( np.sqrt(np.abs(intens_src[i])))
           
            #norma_delta_intens_src.append( np.sqrt(np.sum(np.power(np.divide(np.subtract(intens_src[i],intens_from_vfdf[i]),intens_ambiguity[i]),2))/float(len(intens_src[i])-1)))
            norma_delta_inens_from_nonnegative_vfdf.append(np.sqrt(np.sum(np.power(np.divide(np.subtract(intens_src[i],intens_from_nonnegative_vfdf[i]),intens_ambiguity[i]),2))/float(len(intens_src[i])-1)))
     
            oscil =   self.check_oscil(rg[i],vfdf_valuate[i])
            positiv = self.check_positiv(rg[i],vfdf_valuate[i])
            valcen =  self.check_valcen(rg[i],vfdf_valuate[i])       
            #discrp =  self.check_discrp(norma_delta_intens_src[i],norma_delta_intens_src[0])
            discrp =  self.check_discrp(norma_delta_intens_src[i],np.min(norma_delta_intens_src))
            impmin =  self.check_impmin(norma_delta_intens_src[i],norma_delta_inens_from_nonnegative_vfdf[i])  
            sysdev =  self.check_sysdev(intens_from_vfdf[i],intens_src[i])
            errdev =  self.check_errdev(intens_from_vfdf[i],intens_src[i],intens_ambiguity[i])
                                                                                                          
            if i > 0:     
                stabil_dict = self.check_stabil(alpha[i-1],alpha[i],rg[i],vfdf_valuate[i-1],vfdf_valuate[i])
                stabil = stabil_dict["stabil"]
                total = self.check_total({'OSCIL':oscil,'POSITIV':positiv,'VALCEN':valcen,'DISCRP':discrp,"STABIL":stabil,"SYSDEV":sysdev,"ERRDEV":errdev, "IMPMIN":impmin})
                res.append({"OSCIL":oscil,"POSITIV":positiv,"VALCEN":valcen,"DISCRP":discrp,"STABIL":stabil,"SYSDEV":sysdev,"TOTAL":total,"ALPHA":alpha[i],"ERRDEV":errdev, "IMPMIN":impmin})                         
        # return transposed percept criteria vector
        return self.__pc_dict_transpose(res)

    def __pc_dict_transpose(self,pc_dict):                             
        """transposition of dictionary which stores percept criteria"""
        oscil = []
        discrp = []
        stabil = []
        total = []
        alpha = []
        positiv =[]
        valcen = []
        sysdev = []
        errdev = []
        impmin = []
        for ls in pc_dict: 
            oscil.append(ls["OSCIL"])
            discrp.append(ls["DISCRP"])
            stabil.append(ls["STABIL"])
            total.append(ls["TOTAL"])
            positiv.append(ls["POSITIV"])
            alpha.append(ls["ALPHA"])
            valcen.append(ls["VALCEN"])
            sysdev.append(ls["SYSDEV"])
            errdev.append(ls["ERRDEV"])
            impmin.append(ls["IMPMIN"])
        return {"OSCIL":oscil, "DISCRP":discrp, "STABIL":stabil, "ALPHA":alpha, "TOTAL":total, "VALCEN":valcen, "POSITIV":positiv,"SYSDEV":sysdev,"ERRDEV":errdev,"IMPMIN":impmin}
