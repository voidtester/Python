import subprocess
import os
from configparser import ConfigParser

dir=os.getcwd()
print(dir)
#This gives the path to batch files 
bat_path= dir +'batch_files_tomcat/'
config =ConfigParser()
config.read('conf.ini')
print(config.sections())


#subprocess.call([r'G:\VScode\Python\batch_files_tomcat\keystore.bat',config['tomcat']['keytool'],config['tomcat']['keystore'],config['tomcat']['pass'],config['tomcat']['csr'],config['tomcat']['cn'],config['tomcat']['o'],config['tomcat']['st'],config['tomcat']['ou'],config['tomcat']['l'],config['tomcat']['c']])
subprocess.call(['G:\VScode\Python\batch_files_tomcat\keystore_2.bat'])
from subprocess import *
cmd= 'G:\VScode\Python\batch_files_tomcat\try_bat.bat'
p = Popen(cmd,shell=True )
output, errors = p.communicate()
p.wait() # wait for process to terminate
