# -*- coding: utf-8 -*-
import numpy as np
from scipy import interpolate  
import os
import codecs
import ftplib
import io
import urllib


def valuateVolume(x,y):
    "==========================="
    print(y.shape)
    print(x.shape)
       
    "==========================="
    trapzNorma = np.trapz(y, x, axis=0)
    return y/trapzNorma
                             
def valuate(arr):
    """valuate function"""
    factor = max(arr, key=abs )
    return list(map(lambda x: np.asscalar(x)/float(abs(factor)), arr)) if factor != 0 else np.array(arr)
 
def gen_args(start, end, num, grid="log", base = 1):
    """Return evenly spaced numbers over a specified interval"""
    return np.linspace(start, end, num) if grid=="lin" else np.logspace(np.log(start), np.log(end), num, base = np.exp(1))

def scat_vect(ang, m=0.001):
    #if rad m=1; else 0.001
    """angle to scatering vector transform"""   
    return m*2*np.pi*ang/0.1542

def q2ang(q):
    """scatering vector to angle transform"""    
    return 0.1542*q/(2.0*np.pi)

def cubicInterp(F,argsInterp):
    """cubic interpolation method"""
    srcFunc = interpolate.interp1d(F['x'],F['y'], kind='cubic')
    return srcFunc(argsInterp)

def gen_hessian(x, vectCoef):
    """method for creation D-matrix of second derivatives"""
    dx = np.diff(x) 
    np.savetxt('C:\\log\\diff.txt', dx)
    d0 = []
    d1 = []
    d2 = []
    mcol=len(x)
    nrow=len(dx)-1
    for k in range(nrow):
        d0.append(2.0 / (dx[k]**2 + dx[k] * dx[k+1]))
        d1.append(-2.0 / (dx[k] * dx[k+1]))
        d2.append(2.0 / (dx[k+1]**2 + dx[k+1] * dx[k]))
    f = d0 * np.eye(N=nrow, M=mcol, k=0).T
    s = d1 * np.eye(N=nrow, M=mcol, k=1).T
    t = d2 * np.eye(N=nrow, M=mcol, k=2).T

    D = np.mat(f).T + np.mat(s).T + np.mat(t).T
    D1=D.T
    D2=np.mat(np.zeros(np.shape(D)))

    for i in range(len(vectCoef)):
        D2[i] = vectCoef[i]*D[i]

    return  D1 * D2

def get_vect(fileName,param):
    """get vector from restored vfdf-file by name"""
    keys = fileName[fileName.find("@")+1:fileName.rfind(".")].split('_') 
    ivfdf = np.loadtxt(fileName)
    return ivfdf[:,keys.index(param)]

def get_vect_svparams(file_name,param):
    """get vector of svergun params from [dir_name]_[anisometric_coef]@[PERCEPT_CRITERIA_PARAMS}.txt by name"""
    #keys = file_name[0:file_name.rfind(".")].split('_')
    keys = file_name[file_name.find("@")+1:file_name.rfind(".")].split('_')
    ivfdf = np.loadtxt(file_name)
    return ivfdf[:,keys.index(param)] 

def norm_distr(x,y):
    """Integral trapezoid norm"""
    return np.sqrt(np.trapz(np.power(np.asarray(y),2),np.asarray(x)))

def Rg_Bragg(q):
    """evaluate Rg-vector by scattering vector q"""
    return  np.pi/q/np.sqrt(5./3.)

def custom_trapezoid_coef(Args):             
    """evlute trapezoid coefficient"""
    n, = Args.shape
    a = min(Args)
    b = max(Args)
    #squear coeficients array
    C=np.zeros((n,)) 
    C[0] = 0.5*(Args[1]-a)
    for i in range(1,n-1):
        C[i]=(Args[i+1] - Args[i-1])*0.5
    C[n-1] = 0.5*(b - Args[n-1])
    return C

def sequence(*functions):
    """sequence function call"""
    def func(*args, **kwargs):
        return_value = None
        for function in functions:
            return_value = function(*args, **kwargs)
        return return_value
    return func

def np_arr_is_exists(arr):
    """check existstance of numpy array"""
    if arr is None:
        return False
    elif isinstance(arr, np.ndarray):
        return arr.size != 0
    else:
        return bool(arr)
    
def dict_keys_to_upper(d):
    """Converts dictionaries kys to UpperCase"""
    return {k.upper(): float(v) for k, v in d.items()}

def get_param_from_filename_by_key(filename, key):
    """get param value from file name by key"""
    for elm in  os.path.basename(filename).split("_"):
        if elm.find("=") != -1:
            k,v = elm.split("=")
            if k == key:
                return num(v)
    return None

def num(s):
    """check&convert if possible string to float"""
    try:
        return float(s)
    except ValueError:
        return False

def get_alpha_from_filename(filename):
    """get alpha fro file name"""
    return num(os.path.basename(filename).split('_')[1])

def file_get_contents(filename):
    """get file content"""
    with codecs.open(filename, encoding="utf8") as f:
        return f.read()

def file_put_contents(filename, content):
    """put file content"""
    with codecs.open(filename, 'w+', encoding="utf8") as f:
        f.write(content)
    f.close()

"""NETBOX ASSETS"""
def ftp_upload(filepath, host, login, password):
    """ftp_upload(filePath,'92.53.114.211','artemus_saxsev','SAXSEV')"""
    filename=os.path.basename(filepath)
    fields = filename[filename.find("@")+1:filename.rfind(".")].split('_') 
    newfilename='_'.join(fields) + '.csv'

    session = ftplib.FTP(host, login, password)
    file = open(filepath, 'rb')                      # file to send
    session.storbinary('STOR ' + newfilename, file)     # send the file
    file.close()                                     # close file and FTP
    session.quit()

def ftp_translate_params(filename, host, login, password, data):
    """ftp_upload(filePath,'92.53.114.211','artemus_saxsev','SAXSEV')"""
    bio = io.BytesIO("\n".join(data).encode('utf-8'))
    session = ftplib.FTP(host, login, password)
    session.storbinary('STOR ' + filename, bio)
    session.quit()

def send_request():
    """execute synchronization script"""
    params = urllib.parse.urlencode({'start_sync': 1})
    response = urllib.request.urlopen('http://saxsdb.net/sync.php/?%s'%params)
    html = response.read()
    info = response.info()
    code = response.getcode()
    return code


def print_exists_attr(self):
    for key, value in self.__dict__.items():
        s = str(value)
        if value != None and not isinstance(value, np.ndarray):
            print(key+"="+str(value))
