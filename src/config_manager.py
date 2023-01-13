# -*- coding: utf-8 -*-
import configparser 

class Config():
    def __init__(self, inifile="saxsm.ini"):
        # create new instance of configparser
        self.conf = configparser.ConfigParser()
        # set read ini-file
        self.inifile = inifile
        # read ini-file
        self.conf.read(self.inifile) 
        # characters to strip
        self.rules='"\''
        # set shapes list

    def parse_section(self,section):
        """parse ini-file section"""
        options = self.conf.items(section)
        opt = {}
        for key, val in  options:    
            opt[key] = val.strip(self.rules)    
        return opt

    def write_conf(self, opt, path, pc_w, pc_c, pc_a, nb, disp):
        """write config into file"""
        self.conf["OPTION"] = opt
        self.conf["PATH"] = path 
        self.conf["PARAMS_W"] = pc_w
        self.conf["PARAMS_C"] = pc_c
        self.conf["PARAMS_A"] = pc_a
        self.conf["NETBOX"] = nb
        self.conf["DISPLAY"] = disp
        with open(self.inifile, 'w') as configfile:
            self.conf.write(configfile)

