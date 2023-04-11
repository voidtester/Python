import os

from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
print(conf_file)
conf=ConfigParser()
conf.read(conf_file)

#using conf file 
acme=conf['ACME']
iisacme=conf['ACMEIIS']
# Build the command to run win-acme
command = [
    acme['winacme'],
    "--verbose",
    "--accepttos",
    "--email",
    acme['email'],
    "--store",
    "centralsslstore",
    "--centralsslstorebaseuri",
    "https://acme-v02.api.letsencrypt.org/directory",
    "--certificatepath",
    iisacme['certificate_path'],
    "--target",
    "manual",
    "--host",
    iisacme['domain'],
    "--validation",
    "dns-01",
    "--validationmode",
    "manual",
    "--installation",
    "iis",
    "--installationpath",
    "C:\path\to\site",
    "--installationalias",
    "mysite",
    "--preferred-challenge",
    "dns",
    "--renew"
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