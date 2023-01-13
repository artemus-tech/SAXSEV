# -*- coding: utf-8 -*-
import datetime
from tkinter import *
import os

def save_log(file_name,contents):
    """saving log function for logManager"""
    now = datetime.datetime.now()
    f = open(file_name, 'a+')  
    f.write(now.strftime("%Y-%m-%d %H:%M") + "    " +contents + "\n")  
    f.close()
    
def read_log(fileName):
    """reading log function for logManager"""
    f = open(fileName, 'r')
    return f.read()

def make_title(confLocStr):
    """create title for viewDistribution"""
    formCollections = ["ellipsoid","paralellipiped","cilindr"]
    for formName in formCollections: 
        if formName in confLocStr:
            return "Volume Fraction Distribution Function\nrestored with:" + formName + "; anisometric coefficient " + confLocStr[confLocStr.rfind("_") + 1::]
    return "Unknown form:"

def set_location(lbl,path):
    """set text value to browse file field"""
    lbl.configure(state=NORMAL)
    lbl.delete(0, END)
    lbl.insert(0, path)
    return

def is_column_exist(ivfdf, index):
    """check column existance in numpy matrix"""
    try:
        ivfdf[:,index]
    except:
        return False
    return True

def is_matrix(ivfdf):
    """check numpy array on dimensions"""
    try:
        ivfdf.shape[1]
    except:
        return False
    return True

def get_float_from_entry(entry):
    """get float from entry"""
    try:
        res = float(entry.get().strip())                
    except:
        return False
    return res

def get_int_from_entry(entry):
    """get float from entry"""
    try:
        res = int(entry.get().strip())                
    except:
        return False
    return res

    
def get_string_from_combo(combo):
    """get selected value from dropdown list"""
    try:
        res = combo.get()                
    except:
        return False
    return res

def get_dir_name(path):
    norm_path= os.path.normpath(path)
    if os.path.isfile(norm_path):
        norm_path = os.path.dirname(norm_path)
    return os.path.basename(norm_path)

def get_full_dir_path(path):
    norm_path = os.path.normpath(path)
    if os.path.isfile(norm_path):
        return os.path.dirname(norm_path)
    else:
        return norm_path