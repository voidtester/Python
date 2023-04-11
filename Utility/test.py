str="New-IISSiteBinding -Name "TestSite" -BindingInformation "*:443:" -CertificateThumbPrint "D043B153FCEFD5011B9C28E186A60B9F13103363" -CertStoreLocation "Cert:\LocalMachine\Webhosting" -Protocol https"


##########################################################################
#thumbprint extraction using cryptography module

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

with open(pfx_path, 'rb') as f:
    pfx_data = f.read()
pfx = crypto.load_pkcs12(pfx_data, pfx_password)

# Get the certificate from the PFX data
cert = pfx.get_certificate()

# Calculate the thumbprint of the certificate
thumbprint = cert.fingerprint(hashes.SHA1(), default_backend())
thumbprint = ":".join([format(b, '02x') for b in thumbprint])
