import shutil
import subprocess
import configparser
import os
import platform


dir_path = os.path.dirname(os.path.realpath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(dir_path, 'conf.ini'))

tomcat = conf['tomcat']
iis = conf['IIS']

# to access CA information
ca = conf['CA']

apache = conf['Apache']

downloads=os.path.expanduser("~")+"/Downloads"
tmp="/tmp/"
#certificate import for keystore 
#Tomcat using keystore
#alias is certificate alias to uniquely identify cert
#key is keystore name, passw is keystire password
#certfile is certificate file to import

def cert_import(alias, key, passw, certfile):
    #command to run 
    imp = f'echo "yes" | keytool -import -trustcacerts -alias {alias} -keystore {key} -storepass {passw} -file {certfile}'
    try:
        subprocess.run(imp, shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Certificate not found")
    


#Use powershell script to renew ssl on IIS Server
#Note: Script not working properly on Standalone system; elaborating situation a system where only IIS is 
#configured and not a part of PKI.


def certificate_renew_iis():
    #unzipping folder to get content cert, private key , passphrase
    certpath=unzip_file(a,b)
    
    #getting the path of unzipped certfile
    certfile=certpath+r"\b"
    
    #binding PowerShell script path 
    script_path = dir_path+"/site_binding.ps1"
    
    # Build the PowerShell command
    command = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", script_path, iis['sitename'],certfile]

    # Run the PowerShell command
    result = subprocess.run(command,input="R\n", capture_output=True, text=True)

    # Print the PowerShell script output
    print(result.stdout)
    
#Approach always deleting keystore during SSL renew and creating a new keystore 
def certificate_renew_tomcat():
    #checking for system type Windows or Linux
    system=platform.system()
    if(system=='Windows'):
        #certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
        
        # create fresh keystore for tomcat server 
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
        
   
    if platform.system() == 'Linux' and platform.release().startswith('debian'):
        # create fresh keystore for tomcat server 
        keystore = "echo {passw} | keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(
            key=tomcat['keystore_linux'], passw=tomcat['pass_linux'], common=tomcat['cn'], unit=tomcat['ou'], org=tomcat['o'], local=tomcat['l'], state=tomcat['st'], country=tomcat['c'])

        try:
            subprocess.run(keystore, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(e)

        # import the certificate to keystore
        cert_import("ssl",tomcat['keystore'],tomcat['pass'],certfile)
            
        restart="systemctl restart tomcat"        
        subprocess.run(restart, shell=True, check=True)
    
    if platform.system() == 'Linux' and platform.release().startswith('Red Hat Enterprise Linux'):
        # create fresh keystore for tomcat server (ACME)
        keystore = "echo {passw} | keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(
            key=tomcat['keystore_linux'], passw=tomcat['pass_linux'], common=tomcat['cn'], unit=tomcat['ou'], org=tomcat['o'], local=tomcat['l'], state=tomcat['st'], country=tomcat['c'])

        try:
            subprocess.run(keystore, shell=True, executable='/bin/sh', check=True)
        except subprocess.CalledProcessError as e:
            print(e)    
    
#Approach Replacing old certificates with same name new certificate to avoid changing config file
#Migrating certificate and private key to the location where previous files are 

def certificate_renew_apache():
    system=platform.system()
    if(system=='Windows'):
        certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
        move_file()
        stop_apache()
        start_apache()
    if platform.system() == 'Linux' and platform.release().startswith('debian'):
        certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
        move_file()
        stop_apache()
        start_apache()
    if platform.system() == 'Linux' and platform.release().startswith('Red Hat Enterprise Linux'):
        certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
        move_file()
        stop_apache()
        start_apache()

#Approach Replacing old certificates with same name new certificate to avoid changing config file
#Migrating certificate and private key to the location where previous files are 
        
def certificate_renew_nginx():
    system=platform.system()
    if(system=='Windows'):
        certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
        move_file()
        stop_nginx()
        start_nginx()
        
    if platform.system() == 'Linux' and platform.release().startswith('Debian'):
        certpath=unzip_file_linux(z,un)
        #certfile=certpath+r"\b"
        move_file_windows()
        stop_nginx()
        start_nginx()          

    if platform.system() == 'Linux' and platform.release().startswith('Red Hat Enterprise Linux'):
        certpath=unzip_file_linux(z,un)
        #certfile=certpath+r"\b"
        move_file_Linux()
        stop_nginx()
        start_nginx()          


#unzipping file in windows machine. Take param zip_path: where zip file is ; unzip_path: path to unzip file at 
def unzip_file(zip_path,unzip_path):
    command=f"Expand-Archive -LiteralPath {zip_path} -DestinationPath {unzip_path}"
    try:
        subprocess.run(["powershell.exe",  "-Command", command], capture_output=True, text=True)
    except Exception as e:
        print("Error encountered",e)
        

#unzipping file in linux machine. Take param zip_path: where zip file is ; unzip_path: path to unzip file at
def unzip_file_linux(zip_file,destination_folder):
    command=f"unzip {zip_file} -d {destination_folder}"
    os.system(command)    
        
        
def cert_renew_Tomcat(keystore):
    try:
        delete_file_windows(keystore)
    except:
        pass
    try:    
        delete_file_Linux(keystore)
    except:
        pass
        
    certificate_renew_tomcat()
        


def move_file_windows(src_file_path, dest_dir_path):
        # For Windows
        shutil.move(src_file_path, dest_dir_path)

def move_file_Linux(src_file_path, dest_dir_path):
        # For Linux
        command=f"mv {src_file_path} {dest_dir_path}"
        subprocess.run(command, shell=True, check=True)
        
def delete_file_windows(file_path):
    # Check the operating system
    # For Windows
    os.remove(file_path)
    
def delete_file_Linux(file_path):
    # For Linux
    command=f"rm -f {file_path}"
    subprocess.run(command, shell=True, check=True)



def remove_passphrase():
    command="echo x`h#jU1w/)<M}imWCw4N | openssl rsa -in {inkey} -out {outkey}}".format(inkey="C:\key.key",outkey="C:\key.key")
    os.system(command)

def covert_to_pfx(cert,certkey,pfxcert):
    command = f"openssl pkcs12 -export -in {cert} -inkey {certkey} -out {pfxcert}"
    os.system(command)
    
def start_apache():
    if platform.system() == 'Windows':
        # Windows command to start Apache service
        subprocess.run(["powershell","-Command","Get-Service *Apache2.4*| Start-Service"])
    elif platform.system() == 'Linux':
        # Linux command to start Apache service
        subprocess.run(['sudo', 'systemctl', 'start', 'apache2'])
    else:
        print("Unsupported operating system.")

def stop_apache():
    if platform.system() == 'Windows':
        # Windows command to stop Apache service
        subprocess.run(["powershell","-Command","Get-Service *Apache2.4*| Stop-Service"])
    elif platform.system() == 'Linux':
        # Linux command to stop Apache service
        subprocess.run(['sudo', 'systemctl', 'stop', 'apache2'])
    else:
        print("Unsupported operating system.")


def start_nginx():
    if platform.system() == 'Windows':
        # Windows command to start NGINX service
        subprocess.run(["powershell","-Command","Get-Service *nginx*| Start-Service"])
    elif platform.system() == 'Linux':
        # Linux command to start NGINX service
        subprocess.run(['sudo', 'systemctl', 'start','nginx.service'])
    else:
        print("Unsupported operating system.")
        
def stop_nginx():
    if platform.system() == 'Windows':
        # Windows command to stop NGINX service
        subprocess.run(["powershell","-Command","Get-Service *nginx*| Stop-Service"])
    elif platform.system() == 'Linux':
        # Linux command to stop NGINX service
        subprocess.run(['sudo','systemctl', 'stop','nginx.service'])
    else:
        print("Unsupported operating system.")
    
# certbot_certificate_renew()
# winacme_certificate_tomcat()
# certbot_certificate()
#certificate_renew_tomcat()
# cert_import()
# certificate_renew_iis()
# winacme_certificate_iis()
#certificate_renew_apache()
#move_file(r"K:\test.txt",r"K:\test")
#delete_file(r"K:\test.txt")