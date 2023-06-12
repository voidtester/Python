# Make sure this  scrit is added to Sudoers file in linux Ooperating system to operate with full functionality 
# For windows it does not sue any priviledge escalation so it is good to use as it is 

import subprocess
import configparser
import os
import platform
import distro

dir_path = os.path.dirname(os.path.realpath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(dir_path, 'conf.ini'))

tomcat = conf['tomcat']
iis = conf['IIS']

# to access CA information
ca = conf['CA']

apache = conf['Apache']

# This finds out which OS is being used Windows/Linux.
system=platform.system()

# Setting Documents and Downloads folder along with A folder named EncryptionConsulting to store Certificate to use for SSL renewal.  
if system =="Windows" or system=="windows":
    downloads=os.path.expanduser("~")+"\Downloads"
    documents=os.path.expanduser("~")+"\Documents"
    ecfolder=downloads+"\EncryptionConsulting"
elif system=="Linux":
    # If OS is Linux, finding the flavor. 
    # Setting Documents and Downloads folder along with A folder named EncryptionConsulting to store Certificate to use for SSL renewal.  

    distribution_info = distro.linux_distribution()
    flavor_name = distribution_info[0].split()[0]
    downloads=os.path.expanduser("~")+"/Downloads"
    documents=os.path.expanduser("~")+"/Documents"
    ecfolder=downloads+"/EncryptionConsulting"



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
    


#Use powershell script to renew ssl on IIS Server. Script is integrated in this code only.
#Note: Script not working properly on Standalone system; elaborating situation- a system where only IIS is configured and not a part of PKI.
def certificate_renew_iis():
    #unzipping folder to get content cert, private key , passphrase
    certpath=unzip_file(a,b)
    
    #getting the path of unzipped certfile
    certificate=certpath+r"\b"
    
    site=iis['sitename']
    #binding PowerShell script path 
    script_path =f'''$sitename = "{site}" 
 
$certstore = "LocalMachine" 
 
$certfile="{certificate}" 
 
# Import certificate from file to store 
 
try {{ 
 
    $cert = Import-Certificate -FilePath $certfile -CertStoreLocation Cert:\$certstore\My 
 
}} 
 
catch {{ 
 
    Write-Error "Failed to import certificate from file." 
 
}} 
 
# Get certificate thumbprint 
 
$certhash = $cert.Thumbprint 
 
# Get site from IIS 
 
$site = Get-WebSite | Where-Object {{$_.Name -eq $sitename}} 
 
# Check if site exists 
 
if ($null -eq $site) {{ 
 
    Write-Error "Site not found." 
 
    exit 
 
}} 
 
# Check if bindings exist 
 
if ($null -eq $bindings) {{ 
 
    Write-Error "No SSL bindings found." 
 
    exit 
 
}}
 
# Load the WebAdministration module 
 
 
Import-Module WebAdministration 
 
 
# Get Import-Module WebAdministrationexisting SSL bindings for site 
 
$bindings = Get-WebBinding | Where-Object {{$_.protocol -eq 'https' -and $_.ItemXPath.Contains($sitename)}} 
 
$bindings.AddSslCertificate($certhash, "my") 
  
Write-Output "Certificate bound successfully."'''
    
    # Build the PowerShell command
    command = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", script_path]

    # Run the PowerShell command
    result = subprocess.run(command,input="R\n", capture_output=True, text=True)

    # Print the PowerShell script output
    print(result.stdout)
    


#Approach:- always deleting keystore during SSL renew and creating a new keystore 
def certificate_renew_tomcat():
    #checking for system type Windows or Linux
    
    if system=='Windows':
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
        
   
    if platform.system() == 'Linux' and flavor_name=='debian':
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
    
    if platform.system() == 'Linux' and (flavor_name=='Red Hat Enterprise Linux'or flavor_name=="RHEL"):
        # create fresh keystore for tomcat server (ACME)
        keystore = "echo {passw} | keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(
            key=tomcat['keystore_linux'], passw=tomcat['pass_linux'], common=tomcat['cn'], unit=tomcat['ou'], org=tomcat['o'], local=tomcat['l'], state=tomcat['st'], country=tomcat['c'])

        try:
            subprocess.run(keystore, shell=True, executable='/bin/sh', check=True)
        except subprocess.CalledProcessError as e:
            print(e)    
    



# Approach Replacing old certificates with same name new certificate to avoid changing config file
# Migrating certificate and private key to the location where previous files are 
def certificate_renew_apache():
    # For windows system         
    if(system=='Windows'):
        certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
        
        try:
            if folder_exists(ecfolder):
                #for certificate
                move_file_windows(,ecfolder)
                #for private key
                move_file_windows(,ecfolder)
        
            else:
                createfolder=f"New-Item -Path {ecfolder} -ItemType Directory"
                subprocess.run([createfolder], capture_output=True,executable='/bin/sh', text=True)   
                move_file_windows(,ecfolder)
                #for private key
                move_file_windows(,ecfolder)
        except:
            "Failed to import cert to folder "
        
        # Restarting the apache server and deleting the certofocaet and key file.     
        stop_apache()
        start_apache()
        delete_file_windows()
        delete_file_windows() 
        
    # If the OS is linux flavor is debian, this code followed.     
    if platform.system() == 'Linux' and flavor_name=='debian':
        certpath=unzip_file(z,downloads)
        #certfile=certpath+r"\b"
        #certfile=certpath+r"\b"
        try:
            if folder_exists(ecfolder):
                #for certificate
                move_file_Linux()
                #for private key
                move_file_Linux()
        
            else:
                os.mkdir(ecfolder)
                #for certificate
                move_file_Linux()
                #for private key
                move_file_Linux()
        except:
            "Failed to import cert to folder "
        
        
        # Restarting the apache server and deleting the certificate and key file.
        stop_apache()
        start_apache()
        delete_file_Linux()
        delete_file_Linux() 
        
    # If the OS is linux flavor is RHEL, this code followed.        
    if platform.system() == 'Linux' and flavor_name=='Red Hat Enterprise Linux':
        certpath=unzip_file(z,un)
        #certfile=certpath+r"\b"
        try:
            if folder_exists(ecfolder):
                #for certificate
                move_file_Linux()
                #for private key
                move_file_Linux()
        
            else:
                os.mkdir(ecfolder)
                #for certificate
                move_file_Linux()
                #for private key
                move_file_Linux()
        except:
            "Failed to import cert to folder "
        
        # Restarting the apache server and deleting the certoficate and key file.
        stop_apache()
        start_apache()
        delete_file_Linux()
        delete_file_Linux()
        

#Approach Replacing old certificates with same name new certificate to avoid changing config file
#Migrating certificate and private key to the location where previous files are 
        
def certificate_renew_nginx():
    
       
    if(system=='Windows'):
        certpath=unzip_file(z,downloads)
        #certfile=certpath+r"\b"
        try:
            # Checking whether the folder exists or not 
            # If exists Copy the files to EC folder.
            if folder_exists(ecfolder):
                #for certificate
                move_file_windows()
                #for private key
                move_file_windows()
        
            else:
                # IF folder does not exist create a new folder adn copy the files there.
                createfolder=f"New-Item -Path {ecfolder} -ItemType Directory"
                subprocess.run(["powershell.exe",  "-Command", createfolder], capture_output=True, text=True)   
                move_file_windows(ecfolder)
                #for private key
                move_file_windows()
        except:
            "Failed to import cert to folder "
        
        # Restarting the Nginx server and deleting the certificate and key file.
        stop_nginx()
        start_nginx()
        delete_file_windows()
        delete_file_windows()
        
    if platform.system() == 'Linux' and flavor_name=='Debian':
        certpath=unzip_file_linux(z,downloads)
        #certfile=certpath+r"\b"
        try:
            if folder_exists(ecfolder):
                #for certificate
                move_file_Linux()
                #for private key
                move_file_Linux()
        
            else:
                os.mkdir(ecfolder)
                #for certificate
                move_file_Linux()
                #for private key
                move_file_Linux()
        except:
            "Failed to import cert to folder "
        
        # Restarting the Nginx server and deleting the certificate and key file.
        stop_nginx()
        start_nginx()         
        delete_file_Linux()
        delete_file_Linux()
        
        
    if platform.system() == 'Linux' and flavor_name=='Red Hat Enterprise Linux':
        certpath=unzip_file_linux(z,downloads)
        try:
            if folder_exists(ecfolder):
                #for certificate
                move_file_Linux()
                #for private key
                move_file_Linux()
        
            else:
                os.mkdir(ecfolder)
                #for certificate
                move_file_Linux()
                #for private key
                move_file_Linux()
        except:
            print("Failed to import cert to folder ")
        
        # Restarting the Nginx server and deleting the certificate and key file.
        stop_nginx()
        start_nginx() 
        delete_file_Linux()
        delete_file_Linux()

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
        

# Copy file from Source folder to ECfolder to renew certificates in Apache and Nginx servers Windows.
def move_file_windows(src_file_path, dest_dir_path):
        # For Windows
        command=f"Copy-Item {src_file_path} {dest_dir_path}"

# Copy file from Source folder to ECfolder to renew certificates in Apache and Nginx servers Linux.
def move_file_Linux(src_file_path, dest_dir_path):
        # For Linux
        command=f"cp {src_file_path} {dest_dir_path}"
        subprocess.run(command, shell=True, check=True)


# Deleting files in Windows system         
def delete_file_windows(file_path):
    # Check the operating system
    # For Windows
    os.remove(file_path)

    
# Deleting files in linux system     
def delete_file_Linux(file_path):
    # For Linux
    command=f"sudo rm -rf {file_path}"
    subprocess.run(command, shell=True, check=True)


# Functions remove_passphrase and conver_to_pem are to be used together for Apache and Nginx servers.
# Apacshe and Nginx are more comfortable with PEM files so using .Pem certifiacte and .key private key.   
# This removes the passphrase from privaet key using openssl .
def remove_passphrase():
    command="echo x`h#jU1w/)<M}imWCw4N | openssl rsa -in {inkey} -out {outkey}}".format(inkey="C:\key.key",outkey="C:\key.key")
    os.system(command)

# Thsi function coverts .cer file to .pem file
def covert_to_pem(cert,pemcert):
    command = f"openssl x509 -inform der -in {cert} -out {pemcert}"
    os.system(command)


# This function starts apache service in windows and linux.    
def start_apache():
    if platform.system() == 'Windows':
        # Windows command to start Apache service
        subprocess.run(["powershell","-Command","Get-Service *Apache2.4*| Start-Service"])
    elif platform.system() == 'Linux':
        # Linux command to start Apache service
        subprocess.run(['sudo', 'systemctl', 'start', 'apache2'])
    else:
        print("Unsupported operating system.")


# This function stops apache service in windows and linux.
def stop_apache():
    if platform.system() == 'Windows':
        # Windows command to stop Apache service
        subprocess.run(["powershell","-Command","Get-Service *Apache2.4*| Stop-Service"])
    elif platform.system() == 'Linux':
        # Linux command to stop Apache service
        subprocess.run(['sudo', 'systemctl', 'stop', 'apache2'])
    else:
        print("Unsupported operating system.")


# This function starts nginx service in windows and linux.
def start_nginx():
    if platform.system() == 'Windows':
        # Windows command to start NGINX service
        subprocess.run(["powershell","-Command","Get-Service *nginx*| Start-Service"])
    elif platform.system() == 'Linux':
        # Linux command to start NGINX service
        subprocess.run(['sudo', 'systemctl', 'start','nginx.service'])
    else:
        print("Unsupported operating system.")


# This function stops nginx service in windows and linux.
def stop_nginx():
    if platform.system() == 'Windows':
        # Windows command to stop NGINX service
        subprocess.run(["powershell","-Command","Get-Service *nginx*| Stop-Service"])
    elif platform.system() == 'Linux':
        # Linux command to stop NGINX service
        subprocess.run(['sudo','systemctl', 'stop','nginx.service'])
    else:
        print("Unsupported operating system.")


# Checks whether a folder exists or not in OS.  
def folder_exists(folder_path):
    return os.path.exists(folder_path) and os.path.isdir(folder_path)

    

#certificate_renew_tomcat()
#cert_import()
#certificate_renew_iis()
#certificate_renew_nginx()
#certificate_renew_apache()
#move_file(r"K:\test.txt",r"K:\test")
#delete_file(r"K:\test.txt")