
##########################################################################




import subprocess

site_name = "TestSite"
thumbprint = "D043B153FCEFD5011B9C28E186A60B9F13103363"
def binding(site_name,thumbprint):
        # Construct the command string
        command = f'New-IISSiteBinding -Name "{site_name}" -BindingInformation "*:443:" -CertificateThumbPrint "{thumbprint}" -CertStoreLocation "Cert:\\LocalMachine\\Webhosting" -Protocol https'

        # Execute the command as a subprocess
        result=subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

        # Check the output for any errors
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        else:
            print("Site binding added successfully.")
            
#################################################################################################################

#Thumbprint using powershell 
import subprocess

def add_ssl_cert_to_binding(certfile, certstore, sitename):
    try:
        # Import certificate from file to store
        result = subprocess.run(["powershell", "-Command", f"$cert = Import-Certificate -FilePath '{certfile}' -CertStoreLocation Cert:\\{certstore}\\My; $cert.Thumbprint"], capture_output=True, text=True, check=True)
        cert_thumbprint = result.stdout.strip()

        # Get site from IIS
        result = subprocess.run(["powershell", "-Command", f"$site = Get-WebSite | Where-Object {{ $_.Name -eq '{sitename}' }}; if ($null -eq $site) {{ Write-Error 'Site not found.'; exit }}"], capture_output=True, text=True, check=True)

        # Get existing SSL bindings for site
        result = subprocess.run(["powershell", "-Command", f"$bindings = Get-WebBinding | Where-Object {{ $_.protocol -eq 'https' -and $_.ItemXPath.Contains('{sitename}') }}; if ($null -eq $bindings) {{ Write-Error 'No SSL bindings found.'; exit }}"], capture_output=True, text=True, check=True)

        # Add certificate to SSL binding
        result = subprocess.run(["powershell", "-Command", f"$bindings | ForEach-Object {{ $_.AddSslCertificate({cert_thumbprint}, '{certstore}') }}"], capture_output=True, text=True, check=True)

        return "Certificate bound successfully."

    except subprocess.CalledProcessError as e:
        return f"Failed to import certificate from file or add certificate to SSL binding: {e.stderr}"
    
    
    
#################################################################################################################
#coverting the powershell script to run in python     
import os

def x():
    #declare variables 
    hostname = "ca02.encon.com"

    CAName = "Encon Issuing CA"

    sitename = "Default Web Site"

    certstore = "LocalMachine"

    csr=r"c:\temp\request.csr"
    
    certchain=r"c:\temp\cert.p7b"

    certfile = r"c:\temp\response.cer"
    
    response=r"c:\temp\response.ful"

    # Create a new certificate request using policy.inf
    try:

        csr=f"certreq.exe -new -q -config {hostname}\\{CAName} policy.inf {csr} "
        os.sytem(csr)    

    except:

        print("Failed to create certificate request.")

    try:
        
        # Submit the certificate request to the CA and save the response files
        certreq=f"certreq.exe -submit -q -config {hostname}\\{CAName} {csr} {certfile} {certchain} {response} " 
        os.system(certreq)
    except:

        print("Failed to submit certificate request.")

    try:
        # Import certificate from file to store
        result = subprocess.run(["powershell", "-Command", f"$cert = Import-Certificate -FilePath '{certfile}' -CertStoreLocation Cert:\\{certstore}\\My; $cert.Thumbprint"], capture_output=True, text=True, check=True)
        cert_thumbprint = result.stdout.strip()
        print(cert_thumbprint)
    except:
        print("Failed to retrieve the thumbprint of the certificate")
 
print(os.path.expanduser("~")+"/Downloads")

def folder_exists(folder_path):
    return os.path.exists(folder_path) and os.path.isdir(folder_path)

if folder_exists(r"K:\ProjectS"):
    print("Folder exists!")
else:
    print("Folder does not exist.")