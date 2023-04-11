import subprocess
import configparser
import os
import xml.etree.ElementTree as ET
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pkcs12


dir_path = os.path.dirname(os.path.realpath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(dir_path, 'conf.ini'))

tomcat = conf['tomcat']
iis = conf['IIS']
acme = conf['ACME']
# to access CA information
ca = conf['CA']

apache = conf['Apache']

iisacme = conf['ACMEIIS']

tomcatacme = conf['ACMETomcat']


def certificate_generation_Tomcat():
    try:
        keystore = "echo {passw} | keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(
            key=tomcat['keystore'], passw=tomcat['pass'], common=tomcat['cn'], unit=tomcat['ou'], org=tomcat['o'], local=tomcat['l'], state=tomcat['st'], country=tomcat['c'])

        print(keystore)
        os.system(keystore)

        csr = "keytool -certreq -alias tomcat -keyalg RSA -file {csrfile} -keystore {key} -storepass {passw}".format(
            csrfile=tomcat['csr'], key=tomcat['keystore'], passw=tomcat['pass'])
        print(csr)
        os.system(csr)

        certificate = r"certreq.exe -submit -q -config " + "{}\{} ".format(ca['host'], ca['caname']) + "{} ".format(
            tomcat['csr']) + "{} ".format(tomcat['issucert']) + "{} ".format(tomcat['certchain']) + "{} ".format(tomcat['response'])
        print(certificate)

        os.system(certificate)

        return "Certificate issued successfully"
    except Exception as e:
        print(e)


def cert_import():
    try:
        rca = "echo yes |keytool -import -trustcacerts -alias rootca -keystore {key} -storepass {passw} -file {rootca}".format(
            key=tomcat['kesytore'], passw=tomcat['pass'], rootca=tomcat['root'])
        ica = "echo yes |keytool -import -trustcacerts -alias issuingca -keystore {key} -storepass {passw} -file {issuingca}".format(
            key=tomcat['keystore'], passw=tomcat['pass'], issuingca=tomcat['issuing'])
        intca = "echo yes |keytool -import -trustcacerts -alias intermediateca -keystore {key} -storepass {passw} -file {intermediateca}".format(
            key=tomcat['kesytore'], passw=tomcat['pass'], intermediateca=tomcat['intermediate'])
        print(rca)
        print(ica)
        print(intca)
        try:
            os.system(rca)
        except:
            print("Root CA certifiacte not found")
        try:
            os.system(ica)
        except:
            print("Root CA certifiacte not found")

        try:
            os.system(intca)
        except:
            print("Intermediate CA certifiacte not found")

    except Exception as e:
        print(e)

    finally:
        # To change the server.xml file
        xml_file_update(tomcat['conf_path'],r"C:\Updated.xml",tomcat['keystore'],tomcat['pass'])


def certificate_renew_iis():
    try:
        policy = dir_path+"/policy.inf"
        script_path = dir_path+"/Powershell_scripts/renew.ps1"
        # Build the PowerShell command
        command = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", script_path, iis['hostname'],
                   iis['CAName'], iis['sitename'], iis['certfile'], iis['csr'], iis['certchain'], iis['response']]

        # Run the PowerShell command
        result = subprocess.run(command, capture_output=True, text=True)

        # Print the PowerShell script output
        print(result.stdout)

        return (result)

    except Exception as e:
        print(e)


def certbot_certificate(domain, certificate_path):
    try:
        subprocess.run(["certbot", "--register-unsafely-without-email", "-d",domain,
                        "--manual", "--preferred-challenges", "dns", "certonly", "--config-dir=" +
                        certificate_path,
                        "--agree-tos"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Certbot command failed with exit code {e.returncode}: {e.output}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
       


def winacme_certificate_iis():

    certbot_certificate(iisacme['domain'],iisacme['certificate_path'])

    # binding the certificate to IIS

    # convert the certificate.pem to certificate.pfx

    # make sure openSSL is installed an path is set in the environment varirables
    pem_path = iisacme['certificate_path'] + \
        '/archive/'+iisacme['domain']+'/cert1.pem'
    key_path = iisacme['certificate_path']+'/archive/'+iisacme['domain']+'privkey1.pem'
    pfx_path = r'C:\certificate.pfx'
    pfx_password = iisacme['pfx_password']
    

    command = "openssl pkcs12 -export -out {} -in {} -inkey {} -passin pass:{passw} -passout pass:{passw}".format(
        pfx_path, pem_path, key_path, passw=pfx_password)
    try:
        os.system(command)
    except Exception as e:
        print(e)

        # Command to bind the certificate using netsh
    
    # Load the PFX file
    with open(pfx_path, 'rb') as f:
        pfx_data = f.read()

    # Load the PFX data and extract the certificate
    pfx = load_pkcs12(pfx_data, pfx_password)
    cert = pfx.public_key().certificate

    # Calculate the thumbprint of the certificate
    thumbprint = cert.fingerprint(hashes.SHA1())

    binding(iisacme['site_name'],thumbprint)
    

def winacme_certificate_tomcat():
    certbot_certificate(tomcatacme['domain'],tomcatacme['certificate_path'])
    
    # combine private key and cetrtificate file to import as a single file
    pem_path = tomcatacme['certificate_path'] + \
        '/live/'+tomcatacme['domain']+'/cert.pem'
    key_path = tomcatacme['certificate_path'] + \
        '/live/'+tomcatacme['domain']+'/privkey.pem'
    combine = tomcatacme['certificate_path'] + \
        '/live/'+tomcatacme['domain']+'/combine.pem'

    # Adding new line at the end of the certificate file.
    new_line = "echo. >>{}".format(pem_path)
    os.system(new_line)
    # combine the certificate and the private key
    combine = "type {} {} > {}".format(pem_path, key_path, combine)
    try:
        os.system(combine)
    except Exception as e:
        print(e)
    # create fresh keystore for tomcat server (ACME)
    keystore = "echo {passw} | keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(
        key=tomcatacme['keystore'], passw=tomcatacme['pass'], common=tomcatacme['cn'], unit=tomcatacme['ou'], org=tomcatacme['o'], local=tomcatacme['l'], state=tomcatacme['st'], country=tomcatacme['c'])

    try:
        os.system(keystore)
    except Exception as e:
        print(e)

    # import the certificate to keystore
    certimport = "echo yes | keytool -import -trustcacerts -alias ACMEcertTomcat -keystore {key} -storepass {passw} -file {issuingca}".format(
        key=tomcat['keystore'], passw=tomcat['pass'], issuingca=combine)

    try:
        os.system(certimport)
    except:
        print("Certificate not found")


def certbot_certificate_renew():
    renew = "certbot renew --dry-run"
    try:
        os.system(renew)
    except Exception as e:
        print(e)

def xml_file_update(original_file,updated_file,keystore,password):
        # parse the server.xml file
        file = original_file + "/server.xml"
        tree = ET.parse(file)
        root = tree.getroot()

        # find the Service element with name="Catalina"
        service_elem = root.find("./Service[@name='Catalina']")

        # create the Connector element
        connector_elem = ET.Element('Connector')
        connector_elem.set('port', '8443')
        connector_elem.set('protocol', 'HTTP/1.1')
        connector_elem.set('connectionTimeout', '20000')
        connector_elem.set('redirectPort', '8443')
        connector_elem.set('SSLEnabled', 'true')
        connector_elem.set('scheme', 'https')
        connector_elem.set('secure', 'true')
        connector_elem.set('sslProtocol', 'TLS')
        connector_elem.set('keystoreFile', keystore)
        connector_elem.set('keystorePass', password)

        # insert the new Connector element before the first Engine element
        inserted = False
        for service_child in service_elem:
            if service_child.tag == 'Engine':
                service_elem.insert(list(service_elem).index(
                    service_child), connector_elem)
                inserted = True
                break

        if not inserted:
            service_elem.append(connector_elem)

        # write the updated server.xml file

        tree.write(updated_file)


def binding(site_name,thumbprint):
        # Construct the command string
        command = f'New-IISSiteBinding -Name "{site_name}" -BindingInformation "*:443:" -CertificateThumbPrint "{thumbprint}" -CertStoreLocation "Cert:\\LocalMachine\\My" -Protocol https'

        # Execute the command as a subprocess
        result=subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)

        # Check the output for any errors
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
        else:
            print("Site binding added successfully.")
            
            

# certbot_certificate_renew()
# winacme_certificate_tomcat()
# certbot_certificate()
# certificate_generation_Tomcat()
# cert_import()
# certificate_renew_iis()
# winacme_certificate_iis()
