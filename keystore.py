import subprocess
import os 
from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
conf=ConfigParser()
conf.read(conf_file)

tomcat=conf['tomcat']
# Build the PowerShell command

script=dir+'/Powershell/keystore.ps1'
print(script)

command=["powershell.exe", "-ExecutionPolicy", "Unrestricted", script,tomcat['keystore'],tomcat['pass'],tomcat['csr'],tomcat['cn'],tomcat['o'],tomcat['st'],tomcat['ou'],tomcat['l'],tomcat['c']]
# Run the PowerShell command
result = subprocess.run(command, capture_output=True, text=True)
# Print the PowerShell script output
print(result.stdout)
