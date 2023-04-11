
import os 
from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
conf=ConfigParser()
conf.read(conf_file)

#to access CA information 
ca=conf['CA']
#to access tomcat variables & information 

tomcat=conf['tomcat']

def keystore():
    try:    
        keystore="echo {passw}| keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(key=tomcat['keystore'], passw=tomcat['pass'],common=tomcat['cn'],unit=tomcat['ou'],org=tomcat['o'],local=tomcat['l'],state=tomcat['st'],country=tomcat['c'])

        print(keystore)
       # os.system(keystore)

        csr="keytool -certreq -alias tomcat -keyalg RSA -file {csrfile} -keystore {key} -storepass {passw}".format(csrfile=tomcat['csr'], key=tomcat['keystore'],passw=tomcat['pass'])
        print(csr) 
       # os.system(csr)
        #create certificate through
        
        certificate=r"certreq.exe -submit -q -config "+ "{}\{} ".format(ca['host'],ca['caname'])+ "{} ".format(tomcat['csr'])+ "{} ".format(tomcat['issucert'])+ "{} ".format(tomcat['certchain']) + "{} ".format(tomcat['response'])
        print(certificate)
       # os.system(certificate)
        
    except Exception as e:
        print(e)
        
        
        
        
       

keystore()


