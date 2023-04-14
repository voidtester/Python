from configparser import ConfigParser

conf=ConfigParser()
conf.read('conf.ini')
print(conf.sections())

tomcat=conf['tomcat']
tomcat['keystore']=input("Enter the path to keystore : ")
tomcat['keytool']=input("Enter the keytool path here : ")
tomcat['cn']=input("Enter the CN : ")
tomcat['ou']=input("Enter the OU : ")
tomcat['st']=input("Enter the ST : ")
tomcat['o']=input("Enter the O : ")
tomcat['c']=input("Enter the C : ")
with open('G:\VScode\Python\conf.ini','w') as tcon:
    conf.write(tcon)

iis=conf['IIS']

iis['hostname']=input("Enter the Hostname : ")
iis['sitename']=input("Enter the web site name : ")
iis['certname']=input("Enter the Certificate location : ")
iis['caname']=input("Enter the CA name : ")
with open('G:\VScode\Python\conf.ini','w') as icon:
    conf.write(icon)

acme=conf['ACME']
acme['domain']=input("Enter the Domain name of website : ")
with open('G:\VScode\Python\conf.ini','w') as acon:
    conf.write(acon)
