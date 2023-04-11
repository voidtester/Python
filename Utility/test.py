
##########################################################################

#thumbprint extraction using cryptography module

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pkcs12

# Load the PFX file
with open(pfx_path, 'rb') as f:
    pfx_data = f.read()

# Load the PFX data and extract the certificate
pfx = load_pkcs12(pfx_data, pfx_password)
cert = pfx.public_key().certificate

# Calculate the thumbprint of the certificate
thumbprint = cert.fingerprint(hashes.SHA1())

###########################################################################################


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