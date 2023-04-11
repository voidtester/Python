#Install cryptography module by running 
#pip install cryptography on the terminal
#Approach 1 through cryptography module
from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import pkcs12

pem_path = 'path/to/certificate.pem'
key_path = 'path /to/private/key.pem'
pfx_path = 'path/to/certificate.pfx'
password = 'myPassword123'

def pem_to_pfx(pem_path, pfx_path, password):
    # Load the PEM file
    with open(pem_path, 'rb') as pem_file:
        pem_data = pem_file.read()
    cert = x509.load_pem_x509_certificate(pem_data)

    # Create a new private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Sign the certificate with the private key
    builder = x509.CertificateBuilder().subject_name(cert.subject)
    builder = builder.issuer_name(cert.issuer).public_key(cert.public_key())
    builder = builder.serial_number(cert.serial_number).not_valid_before(cert.not_valid_before)
    builder = builder.not_valid_after(cert.not_valid_after).add_extension(cert.extensions[0], False)
    signed_cert = builder.sign(private_key, x509.sha256,)

    # Convert the private key and signed certificate to PKCS12 format
    pkcs12_data = pkcs12.serialize_key_and_certificates(
        name='My Certificate',
        key=private_key,
        cert=signed_cert,
        ca_certs=[cert],
        password=password.encode('utf-8'),
        key_algorithm=serialization.NoEncryption(),
        cert_chain_policy=pkcs12.CERT_CHAIN_POLICY_NONE,
    )

    # Write the PKCS12 data to a file
    with open(pfx_path, 'wb') as pfx_file:
        pfx_file.write(pkcs12_data)
        
        
pem_to_pfx(pem_path, pfx_path, password)

#Approach 2 :- using openSSL 
# #

def openssl():
    command="openssl pkcs12 -export -out {} -in {} -inkey {} -passin pass:{passw} -passout pass:{passw}".format(pfx_path,pem_path,key_path,passwd=password)
    os.system(command)