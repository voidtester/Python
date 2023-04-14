import os
from configparser import ConfigParser 
conf=ConfigParser()
conf.read('conf.ini')
dir=os.getcwd()
print(dir+"\conf.ini")
tomcat=conf['tomcat']
iis=conf['IIS']
acme=conf['ACME']

try:
    print("-------------------------------------------------------------------")
    print("\t This program will helo you setup your IIS, Tomcat, ACME")
    print("-------------------------------------------------------------------")

    print("\nchoose 1 for IIS ")
    print("Choose 2 for Tomcat")
    print("Choose 3 for ACME")

    choice=int(input("Please enter your choice : "))

except Exception as e:
        print("Wrong input ", e)


while(choice <= 0 or choice >= 4):
    try:
        print("Wrong choice")
        print("\nchoose 1 for IIS ")
        print("Choose 2 for Tomcat")
        print("Choose 3 for ACME")
        choice=int(input("Please enter your choice : "))
    except Exception as e:
            print("Wrong input ",e)

else:
    if choice==1:
        iis['hostname']=input("Enter the Hostname : ")
        iis['sitename']=input("Enter the web site name : ")
        iis['certname']=input("Enter the Certificate location : ")
        iis['caname']=input("Enter the CA name : ")
        with open(dir +'\conf.ini','w') as icon:
            conf.write(icon)

    
    elif choice==2:
        print(" Please enter the following information  \n")
       
        tomcat['keystore']=input("Enter the path to keystore : ")
        tomcat['pass']=input("Enter teh keystore password :")
        tomcat['cn']=input("Enter the CN : ")
        tomcat['ou']=input("Enter the OU : ")
        tomcat['st']=input("Enter the ST : ")
        tomcat['o']=input("Enter the O : ")
        tomcat['c']=input("Enter the C : ")
        tomcat['csr']=input("Enter the CSR path : ")
        print("\nDo you have a Root CA certificate ?")
        root=input("Enter (Y) for yes and (N) for no :")
        if(root=='Y' or root=='y'):
            tomcat['root']=input("Enter the root CA certificate path : ")
        else:
            pass
        print("\nDo you have a Issuing CA certificate ?")
        issue=input("Enter (Y) for yes and (N) for no :")
        if(issue=='Y' or issue=='y'):
            tomcat['issuing']=input("Enter the Issuing CA certificate path : ")
        else:
            pass
        print("\nDo you have a Intermediate CA certificate ?")
        root=input(" Enter (Y) for yes and (N) for no :")
        if(root=='Y' or root=='y'):
            tomcat['intermediate']=input("Enter the Intermediate CA certificate path : ")
        else:
            pass

        with open(dir+'\conf.ini','w') as con:
            conf.write(con)

    elif choice==3:
        acme['domain']=input("Enter the Domain name of website : ")
        with open(dir+'\conf.ini','w') as acon:
            conf.write(acon)

    
    else:
        pass
print(dir)