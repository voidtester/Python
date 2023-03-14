import subprocess
import os 
from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
conf=ConfigParser()
conf.read(conf_file)

tomcat=conf['tomcat']

# Build the PowerShell command
script_path=dir+'/Powershell_scripts/cert_import.ps1'
print(script_path)

command = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", script_path, tomcat['keystore'],tomcat['pass'],tomcat['root'],tomcat['issuing'],tomcat['intermediate']]
# Run the PowerShell command
result = subprocess.run(command, capture_output=True, text=True)
# Print the PowerShell script output
print(result.stdout)

