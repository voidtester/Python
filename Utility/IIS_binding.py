#Install pywin32 module whcih contains win32com.client by running 
#pip install pywin32 on  the terminal 


import win32com.client
# Path to PFX file
pfx_path = r"C:\path\to\certificate.pfx"
# Password for PFX file
pfx_password = "password"
# Site ID of the IIS site to bind the certificate to
site_id = "1"
# Hostname to bind the certificate to
hostname = "example.com"
# Port to bind the certificate to
port = "443"

# Connect to the IIS WMI provider
iis = win32com.client.GetObject("winmgmts:root\WebAdministration")

# Get the site object for the specified site ID
site = iis.Get("Site.SiteName='Default Web Site'")

# Get the binding object for the specified hostname and port
binding = None
for b in site.Bindings:
    if b.Protocol == "https" and b.BindingInformation.endswith(f":{port}:{hostname}"):
        binding = b
        break

# If a binding was found, update it with the new certificate
if binding is not None:
    # Load the certificate from the PFX file
    cert = win32com.client.Dispatch("X509Enrollment.CX509CertificateEnrollment")
    cert.InitializeFromFileName(pfx_path, 0)
    cert.PrivateKeyExportable = True

    # Update the binding with the new certificate
    binding.CertificateHash = cert.GetCertHash()
    binding.CertificateStoreName = "MY"
    binding.Put_()
    print(f"Certificate bound to {hostname}:{port}")
else:
    print(f"No binding found for {hostname}:{port}")
    
    
##########################################################################################3   
    
#Approch 2 
#Install the module psexec before hand
# pip install psexec
import subprocess
import os

# Path to PFX file
pfx_path = r"C:\path\to\certificate.pfx"
# Password for PFX file
pfx_password = "password"
# Site ID of the IIS site to bind the certificate to
site_id = "1"
# Hostname to bind the certificate to
hostname = "example.com"
# Port to bind the certificate to
port = "443"

# Command to bind the certificate using netsh
command = [
    "netsh", "http", "add", "sslcert",
    f"ipport=0.0.0.0:{port}",
    f"certhash={os.path.splitext(os.path.basename(pfx_path))[0]}",
    f"appid={{{site_id}}}",
    f"certstorename=MY",
    f"password={pfx_password}",
    "clientcertnegotiation=enable"
]

# Run the command using psexec
subprocess.run(["psexec", "-h", "-i", "1"] + command, capture_output=True)
print(f"Certificate bound to {hostname}:{port}")