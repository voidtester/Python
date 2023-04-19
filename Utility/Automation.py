import subprocess
import configparser
import os
import xml.etree.ElementTree as ET
import platform


dir_path = os.path.dirname(os.path.realpath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(dir_path, 'conf.ini'))

tomcat = conf['tomcat']
iis = conf['IIS']

# to access CA information
ca = conf['CA']

apache = conf['Apache']



def cert_import(alias,key,passw,certfile):
    
        imp=f"echo yes | keytool -import -trustcacerts -alias {alias} -keystore {key} -storepass {passw} -file {certfile}"
        
        try:
            os.system(imp)
        except:
            print("Certifiacte not found")

    




def certificate_renew_iis():

    certpath=unzip_file(a,b)
    certfile=certpath+r"\b"
    script_path = dir_path+"/site_binding.ps1"
    # Build the PowerShell command
    command = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", script_path, iis['sitename'],certfile]

    # Run the PowerShell command
    result = subprocess.run(command,input="R\n", capture_output=True, text=True)

    # Print the PowerShell script output
    print(result.stdout)
    

def certificate_renew_tomcat():
    system=platform.system()
    if(system=='Windows'):
        #certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
        
        # create fresh keystore for tomcat server (ACME)
        keystore = "echo {passw} | keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(
            key=tomcat['keystore'], passw=tomcat['pass'], common=tomcat['cn'], unit=tomcat['ou'], org=tomcat['o'], local=tomcat['l'], state=tomcat['st'], country=tomcat['c'])

        try:
            os.system(keystore)
        except Exception as e:
            print(e)

        # import the certificate to keystore
        cert_import("ssl",tomcat['keystore'],tomcat['pass'],certfile)

    
        try:
            subprocess.run(["powershell","-Command","Get-Service *tomcat*| Stop-Service"])
    
        except:
            print("failed to stop Tomcat Service")
        try:
            subprocess.run(["powershell","-Command","Get-Service *tomcat*| Start-Service"])
    
        except:
            print("failed to start Tomcat Service")
        
    if(system=='Linux'):
        if(platform.release=='Debian'):
             #certpath=unzip_file(z,un)
            #certfile=certpath+r"\b"
            
            # create fresh keystore for tomcat server (ACME)
            keystore = "echo {passw} | keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(
                key=tomcat['keystore_linux'], passw=tomcat['pass_linux'], common=tomcat['cn'], unit=tomcat['ou'], org=tomcat['o'], local=tomcat['l'], state=tomcat['st'], country=tomcat['c'])

            try:
                os.system(keystore)
            except Exception as e:
                print(e)

            # import the certificate to keystore
            cert_import("ssl",tomcat['keystore'],tomcat['pass'],certfile)
            if(platform.release=='Red Hat'):
                print()
        restart="systemctl | grep tomcat* | restart "        
        os.system(restart)

def certificate_renew_apache():
    system=platform.system()
    if(system=='Windows'):
        certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
    if(system=='Linux'):
        if(platform.release=='Debian'):
            print()
        if(platform.release=='Red Hat'):
            print()
        
    



def unzip_file(zip_path,unzip_path):
    command=f"Expand-Archive -LiteralPath {zip_path} -DestinationPath {unzip_path}"
    try:
        subprocess.run(["powershell.exe",  "-Command", command], capture_output=True, text=True)
    except Exception as e:
        print("Error encountered",e)
        

def unzip_linux(zip_file,destination_folder):
    command=f"unzip {zip_file} -d {destination_folder}"
    os.system(command)    
        
def add_pfxcert_to_store():
    # Replace these values with the actual path to your PFX file and password
    pfx_path = r'C:\path\to\certificate.pfx'
    password = 'yourpassword'

    # Convert password to secure string
    secure_password = subprocess.check_output(['powershell.exe', 'ConvertTo-SecureString', '-String', password, '-Force', '-AsPlainText']).strip()

    # Import PFX certificate
    subprocess.run(['powershell.exe', 'Import-PfxCertificate', '-FilePath', pfx_path, '-CertStoreLocation', 'Cert:\LocalMachine\My', '-Password', secure_password])

def cert_renew_Tomcat(keystore):
        remove_file(keystore)
        certificate_renew_tomcat()
        
      

def remove_file(file):
    
        subprocess.run(["powershell","-Command",f"Remove-Item {file}"], capture_output=True, text=True)
    
# certbot_certificate_renew()
# winacme_certificate_tomcat()
# certbot_certificate()
#certificate_renew_tomcat()
# cert_import()
# certificate_renew_iis()
# winacme_certificate_iis()
certificate_renew_apache()