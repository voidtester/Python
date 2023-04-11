import subprocess
import configparser
import os
import xml.etree.ElementTree as ET
import OpenSSL.crypto as crypto

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

        # parse the server.xml file
        file = tomcat['conf_path']
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
        connector_elem.set('keystoreFile', tomcat['keystore'])
        connector_elem.set('keystorePass', tomcat['pass'])

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

        tree.write('G:\server_copy1.xml')


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


def certbot_certificate():
    try:
        # Stop the Apache service
        # subprocess.run(["Stop-Service", "-Name", "Apache2.4"], check=True)

        # Obtain the certificate using Certbot
        subprocess.run(["certbot", "--register-unsafely-without-email", "-d", apache['domain'],
                        "--manual", "--preferred-challenges", "dns", "certonly", "--config-dir=" +
                        apache['certificate_path'],
                        "--agree-tos", "--force-renew"], check=True)

        # Start the Apache service
        # subprocess.run(["Start-Service", "-Name", "Apache2.4"], check=True)
    except Exception as e:
        print(e)


def winacme_certificate_iis():

    # Make winacme command for iis certificate issue.

    command = ["certbot", "--register-unsafely-without-email", "-d", iisacme['domain'],
               "--manual", "--preferred-challenges", "dns", "certonly", "--config-dir=" +
               tomcatacme['certificate_path'],
               "--agree-tos",
               ]
    # Convert the command to a string
    command_str = " ".join(command)
    print(command_str)
    try:
        # Run the command
        os.system(command_str)
    except Exception as e:
        print(e)

    # binding the certificate to IIS

    # convert the certificate.pem to certificate.pfx

    # make sure openSSL is installed an path is set in the environment varirables
    pem_path = iisacme['certificate_path'] + \
        '/archive/'+iisacme['domain']+'/cert1.pem'
    key_path = iisacme['certificate_path']+'/archive/'+iisacme['domain']+'privkey1.pem'
    pfx_path = r'C:\certificate.pfx'
    pfx_password = iisacme['pfx_password']
    port = 443
    site_id = iisacme['siteid']
    hostname = iisacme['hostname']

    command = "openssl pkcs12 -export -out {} -in {} -inkey {} -passin pass:{passw} -passout pass:{passw}".format(
        pfx_path, pem_path, key_path, passw=pfx_password)
    try:
        os.system(command)
    except Exception as e:
        print(e)

        # Command to bind the certificate using netsh
    
    def get_appid(site_name):
        # Connect to the IIS WMI provider
        iis = win32com.client.GetObject("winmgmts:root\WebAdministration")

        # Get the site object
        site = iis.Get("Site.Name='{}'".format(site_name))

        # Get the application object
        app = site.Applications[0]

        # Get the AppID value
        app_id = app.AppPoolId

        return app_id

    # Load the PFX data into a crypto object
    with open(pfx_path, 'rb') as f:
        pfx_data = f.read()
    pfx = crypto.load_pkcs12(pfx_data, pfx_password)

    # Get the certificate from the PFX data
    cert = pfx.get_certificate()
    
    # Calculate the thumbprint of the certificate
    thumbprint = cert.digest("sha1").decode("utf-8")
    thumbprint = ":".join([thumbprint[i:i+2] for i in range(0, len(thumbprint), 2)])
    app_id=get_appid("Default Web Site")
    binding_command = [
       "netsh", "http", "add", "sslcert",
        f"ipport=0.0.0.0:{port}",
        f"certhash={thumbprint}",
        f"appid={{{app_id}}}",
        f"certstorename=MY",
        "clientcertnegotiation=enable"
       ]
    command_str = " ".join(binding_command)
    try:
        # Run the command using psexec
        subprocess.run(["psexec", "-h", "-i", "1"] +
                       binding_command, capture_output=True)
        print(f"Certificate bound to {hostname}:{port}")
    except Exception as e:
        print(e)


def winacme_certificate_tomcat():
    # Winacme methode not suitable changing to obtaining certificate from certbot and importing to keystore.
    # Build the command to get the certificate
    command = ["certbot", "--register-unsafely-without-email", "-d", tomcatacme['domain'],
               "--manual", "--preferred-challenges", "dns", "certonly", "--config-dir=" +
               tomcatacme['certificate_path'],
               "--agree-tos",
               ]

    # Convert the command to a string
    command_str = " ".join(command)
    print(command_str)
    try:
        # Run the command
        os.system(command_str)
        print("Success")
    except Exception as e:
        print(e)
    # combine private key and cetrtificate file to import as a single file
    pem_path = tomcatacme['certificate_path'] + \
        '/live/'+tomcatacme['domain']+'/cert.pem'
    key_path = tomcatacme['certificate_path'] + \
        '/live/'+tomcatacme['domain']+'/key.pem'
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


# certbot_certificate_renew()
# winacme_certificate_tomcat()
# certbot_certificate()
# certificate_generation_Tomcat()
# cert_import()
# certificate_renew_iis()
# winacme_certificate_iis()
