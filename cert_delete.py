
import subprocess
import os 
from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
conf=ConfigParser()
conf.read(conf_file)

tomcat=conf['tomcat']   
    
# Build the PowerShell command
script_path=dir+'/Powershell/cert_delete.ps1'
command = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", script_path, tomcat['keystore'],tomcat['pass']]
   
# Run the PowerShell command
result = subprocess.run(command, capture_output=True, text=True)
   
# Print the PowerShell script output
print(result.stdout)
    

