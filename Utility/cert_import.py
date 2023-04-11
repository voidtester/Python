
import os 
from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
conf=ConfigParser()
conf.read(conf_file)

tomcat=conf['tomcat']

def cert_import():
    try:
        rca="echo yes | keytool -import -trustcacerts -alias rootca -keystore {key} -storepass {passw} -file {rootca}".format(key=tomcat['kesytore'],passw=tomcat['pass'],rootca=tomcat['root'])
        ica="echo yes | keytool -import -trustcacerts -alias issuingca -keystore {key} -storepass {passw} -file {issuingca}".format(key=tomcat['keystore'],passw=tomcat['pass'],issuingca=tomcat['issuing']) 
        intca="echo yes | keytool -import -trustcacerts -alias intermediateca -keystore {key} -storepass {passw} -file {intermediateca}".format(key=tomcat['kesytore'],passw=tomcat['pass'],intermediateca=tomcat['intermediate'])
        print(rca)
        print(ica)
        print(intca)  
        os.system(rca)
        os.system(ica)
        os.system(intca) 
    except Exception as e:
        print(e)

cert_import()



