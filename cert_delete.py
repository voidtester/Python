
import subprocess
import os 
from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
conf=ConfigParser()
conf.read(conf_file)

tomcat=conf['tomcat']   
    
def cert_delete():
    rca="keytool -delete -alias rootca -keystore {key} -storepass {passw}".format(key=tomcat['keystore'],passw=tomcat['pass'])
    ica="keytool -delete -alias issuingca -keystore {key} -storepass {passw}".format(key=tomcat['keystore'],passw=tomcat['pass']) 
    intca="keytool -delete -alias intermediateca -keystore {key} -storepass {passw}".format(key=tomcat['keystore'],passw=tomcat['pass'])
    print(rca)
    print(ica)
    print(intca) 
    os.system(rca)
    os.system(ica)
    os.system(intca) 

cert_delete()
