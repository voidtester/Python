import os
from configparser import ConfigParser 
conf=ConfigParser()

dir=os.getcwd()
path=dir+'\conf.ini'
print(path)
conf.read(path)
tomcat=conf['tomcat']
iis=conf['IIS']
acme=conf['ACME']
print(tomcat['keystore'])

def keystore():
    keystore="echo yes |keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(key=tomcat['keystore'], passw=tomcat['pass'],common=tomcat['cn'],unit=tomcat['ou'],org=tomcat['o'],local=tomcat['l'],state=tomcat['st'],country=tomcat['c'])

    print(keystore)
    #os.system(keystore_command)

    csr="keytool -certreq -alias tomcat -keyalg RSA -file {csrfile} -keystore {key} -storepass {passw}".format(csrfile=tomcat['csr'], key=tomcat['keystore'],passw=tomcat['pass'])
    print(csr) 
    #os.system(csr)

def cert_import():
    rca="echo yes | keytool -import -trustcacerts -alias rootca -keystore {key} -storepass {passw} -file {rootca}".format(key=tomcat['kesytore'],passw=tomcat['pass'],rootca=tomcat['root'])
    ica="echo yes | keytool -import -trustcacerts -alias issuingca -keystore {key} -storepass {passw} -file {issuingca}".format(key=tomcat['keystore'],passw=tomcat['pass'],issuingca=tomcat['issuing']) 
    intca="echo yes | keytool -import -trustcacerts -alias intermediateca -keystore {key} -storepass {passw} -file {intermediateca}".format(key=tomcat['kesytore'],passw=tomcat['pass'],intermediateca=tomcat['intermediate'])
    print(rca)
    print(ica)
    print(intca)  
    #os.system(rca)
    #os.system(ica)
    #os.system(intca) 

def cert_delete():
    rca="keytool -delete -alias rootca -keystore {key} -storepass {passw}".format(key=tomcat['keystore'],passw=tomcat['pass'])
    ica="keytool -delete -alias issuingca -keystore {key} -storepass {passw}".format(key=tomcat['keystore'],passw=tomcat['pass']) 
    intca="keytool -delete -alias intermediateca -keystore {key} -storepass {passw}".format(key=tomcat['keystore'],passw=tomcat['pass'])
    print(rca)
    print(ica)
    print(intca) 
    #os.system(rca)
    #os.system(ica)
    #os.system(intca) 

keystore()