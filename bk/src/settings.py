# -*- coding:utf-8 -*-
import config as cfg
from layout import LayoutMaker, Frame
from tkinter import *
import os

class ISettings:
    def __init__(self,root):
        #storage for settings from options- and path-sections
        self.root=root
        return

    def init_settings_presets(self):
        for v,k in self.pc_chbox:
            if cfg.disp.get(k)=='1':
                v.toggle()            


    def make_pc_params_form(self):
        """generate forms for percept criteria params"""
        # general layout config
        frame = Frame(self.root)
        frame.columnconfigure(0, pad=10)
        frame.columnconfigure(1, pad=10)
        frame.columnconfigure(2, pad=10)
        frame.columnconfigure(3, pad=10)        
        # setup presets
        self.keys=["discrp", "stabil", "valcen", "sysdev", "oscil", "positiv", "impmin", "errdev"]

        self.entry_pc_w={}
        self.entry_pc_c={}
        self.entry_pc_a={}
        self.chb_pc_disp =[]

        # percept criteria section entry
        lm_pc = LayoutMaker(lbl_width=12)
        lm_pc.make_pc_label_grid(frame, "Show" , "W-param", "C-param", "A-param")
        self.pc_chbox = []
        self.pc_chbox_dict = {"discrp": IntVar(), 
                              "stabil": IntVar(), 
                              "valcen": IntVar(), 
                              "sysdev": IntVar(), 
                              "oscil":  IntVar(), 
                              "positiv":IntVar(), 
                              "impmin": IntVar(), 
                              "errdev": IntVar()}
        for i in range(len(self.keys)):
            self.__mk_pc_entry(self.keys[i], frame, lm_pc,i+1)
            chbox, chval = lm_pc.make_pc_checkboxbar(frame,  pos=i+1, lbl_text=self.keys[i].upper(), var=self.pc_chbox_dict.get(self.keys[i]))
            self.pc_chbox.append([chbox,self.keys[i]])
        self.init_settings_presets()
        lm_pc.make_btn_grid(frame, row=10, column=3, btn_text="Save", cmd=self.save_pc_params)
        lm_pc.make_btn_grid(frame, row=10, column=0, btn_text="Defaults", cmd=self.restore_defaults_pc_params)
        frame.pack()
        return
        
    def restore_defaults_pc_params(self):
        """restoring percept critteria params to default"""
        for key_pc_w,val_pc_w, in self.entry_pc_w.items():
            val_pc_w.delete(0,'end')
        for key_pc_c,val_pc_c in self.entry_pc_c.items():
            val_pc_c.delete(0,'end')
        for key_pc_a,val_pc_a in self.entry_pc_a.items():
            val_pc_a.delete(0,'end')

        self.entry_pc_w["impmin"].insert(0, "6.0")
        self.entry_pc_w["stabil"].insert(0, "1.0")
        self.entry_pc_w["valcen"].insert(0, "1.0")
        self.entry_pc_w["sysdev"].insert(0, "2.0")
        self.entry_pc_w["positiv"].insert(0,"1.0")
        self.entry_pc_w["oscil"].insert(0,  "1.0")
        self.entry_pc_w["discrp"].insert(0, "3.0")
        self.entry_pc_w["errdev"].insert(0, "6.0")

        self.entry_pc_c["impmin"].insert(0, "0.2")
        self.entry_pc_c["stabil"].insert(0, "0.02")
        self.entry_pc_c["valcen"].insert(0, "0.01")
        self.entry_pc_c["sysdev"].insert(0, "0.2")
        self.entry_pc_c["positiv"].insert(0,"0.01")
        self.entry_pc_c["oscil"].insert(0,  "1.3")
        self.entry_pc_c["discrp"].insert(0, "0.2")
        self.entry_pc_c["errdev"].insert(0, "0.1")

        self.entry_pc_a["impmin"].insert(0, "0.0")
        self.entry_pc_a["stabil"].insert(0, "0.0")
        self.entry_pc_a["valcen"].insert(0, "1.0")
        self.entry_pc_a["sysdev"].insert(0, "1.0")
        self.entry_pc_a["positiv"].insert(0,"1.0")
        self.entry_pc_a["oscil"].insert(0,  "0.3")
        self.entry_pc_a["discrp"].insert(0, "0.7")
        self.entry_pc_a["errdev"].insert(0, "0.0")

        return 

    def save_pc_params(self):
        """saving percept critteria params to ini-file"""
        # set params list      
        for k in self.keys:
            self.__get_pc_val(k)
        #write all defined in config.py
        cfg.disp = {k:str(v) for k,v in cfg.disp.items()}
        cfg.config.write_conf(cfg.options, cfg.paths, cfg.pc_w, cfg.pc_c, cfg.pc_a, cfg.nb, cfg.disp)
        #return
    
    def make_generic_form(self):
        """generate forms for general settings"""
        frame = Frame(self.root)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, pad=10)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(5, pad=10)
        # layout manager initialize       
        lm_settings = LayoutMaker(lbl_width=48)
        # path section entry
        self.entry_logfilename    = lm_settings.make_entry_grid(frame, pos=1, lbl_text="log file name")
        self.entry_vfdfdirpref = lm_settings.make_entry_grid(frame, pos=2, lbl_text="Prefix for vfdf directory")
        self.entry_inputpath = lm_settings.make_entry_grid(frame, pos=3, lbl_text="Path to input")
        self.entry_outputpath = lm_settings.make_entry_grid(frame, pos=4, lbl_text="Path to results")
        self.entry_logpath = lm_settings.make_entry_grid(frame, pos=5, lbl_text="Path to Logs")
        # options section entry
        # set alpha-regulizer params
        self.entry_alphanum = lm_settings.make_entry_grid(frame, pos=6, lbl_text="alpha numbers")
        self.entry_alphastart = lm_settings.make_entry_grid(frame, pos=7, lbl_text="base^start is the starting value of the sequence")
        self.entry_alphaend  = lm_settings.make_entry_grid(frame, pos=8, lbl_text="base^end is the starting value of the sequence alpha")
        self.entry_alphabase = lm_settings.make_entry_grid(frame, pos=9, lbl_text="The base of the log space for alpha")               
        #seting values for path section
        self.entry_logfilename.insert(0, os.path.basename(cfg.paths["log_file_path"]))
        self.entry_logpath.insert(0, os.path.dirname(cfg.paths["log_file_path"]))
        self.entry_inputpath.insert(0, cfg.paths["input_data_path"])
        self.entry_outputpath.insert(0, cfg.paths["output_data_path"])
        #seting values for options section
        self.entry_vfdfdirpref.insert(0, cfg.options["vfdf_dir_pref"])
        self.entry_alphanum.insert(0, cfg.options["default_alpha_num"])
        self.entry_alphastart.insert(0, cfg.options["default_alpha_start"])
        self.entry_alphaend.insert(0, cfg.options["default_alpha_end"])
        self.entry_alphabase.insert(0, cfg.options["default_alpha_base"])
        # save button
        lm_settings.make_btn_grid(frame, row=10, column=1, btn_text="Save", cmd=self.save_settings)
        frame.pack()

                                                                                   
    def save_settings(self): 
        """saving settings to ini-file"""
        # set options list 
        cfg.options["default_alpha_num"] = self.entry_alphanum.get()
        cfg.options["default_alpha_start"]= self.entry_alphastart.get()
        cfg.options["default_alpha_end"] = self.entry_alphaend.get()
        cfg.options["default_alpha_base"] = self.entry_alphabase.get()
        cfg.options["vfdf_dir_pref"] = self.entry_vfdfdirpref.get()
        # create log path
        log_file_name = self.entry_logfilename.get()   
        log_dir = self.__mk_dir(self.entry_logpath.get())
        # set paths
        cfg.paths["input_data_path"] = self.__mk_dir(self.entry_inputpath.get())
        cfg.paths["output_data_path"] = self.__mk_dir(self.entry_outputpath.get())
        cfg.paths["log_file_path"] =  os.path.join(log_dir, log_file_name) 
        # save to file                
        cfg.config.write_conf(cfg.options, cfg.paths, cfg.pc_w, cfg.pc_c, cfg.pc_a, cfg.nb, cfg.disp)
        return

    def __mk_dir(self,path):
        """create directory"""
        if not os.path.exists(path):
            os.makedirs(path)
        return path
            
    def __mk_pc_entry(self, key, frame, lm_pc,i):
        """make arbitary entry"""
        #self.entry_pc_w[key], self.entry_pc_c[key], self.entry_pc_a[key] = lm_pc.make_pc_entry_grid(frame, pos=i, lbl_text=None, lbl_text=key) 
        self.entry_pc_w[key], self.entry_pc_c[key], self.entry_pc_a[key] = lm_pc.make_pc_entry_grid(frame, pos=i, lbl_text = "")
        self.entry_pc_w[key].insert(0, cfg.pc_w[key])
        self.entry_pc_c[key].insert(0, cfg.pc_c[key])
        self.entry_pc_a[key].insert(0, cfg.pc_a[key])
      
    def __get_pc_val(self, key):
        """get value from arbitary entry and overwrite it into settings storage"""
        cfg.pc_w[key] =self.entry_pc_w[key].get()
        cfg.pc_c[key] =self.entry_pc_c[key].get()
        cfg.pc_a[key] =self.entry_pc_a[key].get()
        cfg.disp[key] = self.pc_chbox_dict.get(key).get()

    def make_nb_session_form(self):
        """generate forms for general settings"""
        frame = Frame(self.root)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, pad=10)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(5, pad=10)
        # layout manager initialize       
        lm_settings = LayoutMaker(lbl_width=12)
        # path section entry
        self.entry_url = lm_settings.make_entry_grid(frame, pos=1, lbl_text="URL")
        self.entry_login = lm_settings.make_entry_grid(frame, pos=2, lbl_text="Login")
        #seting values for netbox section
        self.entry_url.insert(0, cfg.nb["url"])
        self.entry_login.insert(0, cfg.nb["login"])
        # save button
        lm_settings.make_btn_grid(frame, row=10, column=1, btn_text="Save", cmd=self.save_nb_settings)
        frame.pack()

    def save_nb_settings(self): 
        """saving netbox requisites to ini-file"""
        # set requisites list
        cfg.nb["url"] = self.entry_url.get()
        cfg.nb["login"]= self.entry_login.get()
        cfg.config.write_conf(cfg.options, cfg.paths, cfg.pc_w, cfg.pc_c, cfg.pc_a, cfg.nb, cfg.disp)
        return  