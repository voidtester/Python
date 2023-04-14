import subprocess
import os
from configparser import ConfigParser

dir=os.getcwd()
print(dir)
#This gives the path to batch files 
bat_path= dir +'batch_files_tomcat/'
conf =ConfigParser()
conf.read('conf.ini')
print(conf.sections())

tomcat=conf['tomcat']
iis=conf['IIS']
acme=conf['ACME']

def keystore_generation():
    path=dir+'keystore.py'
    subprocess.call["python",path]
    
def cert_impoort():
     path=dir+'cert_import.py'
     subprocess.call["python",path]
    


def cert_remove():
   path=dir+'cert_delete.py'
   subprocess.call["python",path]
    

def renew_iis():
    path=dir+'renew_iis.py'
    subprocess.call["python",path]
    
   
   
   
cert_impoort()
