import os
import subprocess
from configparser import ConfigParser
dir=os.getcwd()
print(dir)
conf_file=dir+"\conf.ini"
print(conf_file)
conf=ConfigParser()
conf.read(conf_file)
apache=conf['Apache'] 


# Stop the Apache service
#subprocess.run(["Stop-Service", "-Name", "Apache2.4"], check=True)

# Obtain the certificate using Certbot
subprocess.run(["certbot", "--register-unsafely-without-email", "-d", apache['domain'], 
                "--manual", "--preferred-challenges", "dns", "certonly", "--config-dir=" + apache['certificate_path'],
                "--agree-tos", "--force-renew"], check=True)

# Start the Apache service
##subprocess.run(["Start-Service", "-Name", "Apache2.4"], check=True)