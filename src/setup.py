# -*- coding: utf-8 -*-
from  config_manager import  Config
import os

config  = Config()

conf={"OPTION":{},"PATH":{}}
                                              
options = {}
paths = {}
nb = {}
disp = {}

pc_w = {'DISCRP':3.0,'OSCIL':1.0,'STABIL':1.0,'SYSDEV':2.0,'POSITIV':1.0,'VALCEN':1.0,'ERRDEV':6.0, 'IMPMIN':6.0}       
pc_c = {'DISCRP':0.2,'OSCIL':1.3,'STABIL':0.02,'SYSDEV':0.2,'POSITIV':0.01,'VALCEN':0.01,'ERRDEV':0.1,'IMPMIN':0.2}
pc_a = {'DISCRP':0.7,'OSCIL':0.3, 'STABIL':0.0, 'SYSDEV':1.0, 'POSITIV':1.0, 'VALCEN':1.0,'ERRDEV':0.0,'IMPMIN':0.0}

path = os.getcwd()
parent_path = os.sep.join(path.split(os.sep)[:-1])

options["default_alpha_num"]  = 41
options["default_alpha_start"]= -10
options["default_alpha_end"]  = 11
options["default_alpha_base"] = 10
options["vfdf_dir_pref"] = "logExp"      
   
paths["input_data_path"] = os.path.join(parent_path, "input")
paths["output_data_path"] = os.path.join(parent_path, "output")
paths["log_file_path"] = os.path.join(parent_path, "log","saxs.log")
paths["doc_data_path"] = os.path.join(parent_path, "doc", "index.html")


nb["url"] = "saxsdb.net"
nb["login"] = "artemus_saxsev"

disp["oscil"] =  1
disp["discrp"] = 1
disp["valcen"] = 1
disp["stabil"] = 1
disp["impmin"] = 1
disp["sysdev"] = 1
disp["errdev"] = 1
disp["positiv"] = 1

config.write_conf(options, paths, pc_w, pc_c, pc_a, nb, disp)

print("INSTALLATION COMPLETE SUCCESSFULLY")