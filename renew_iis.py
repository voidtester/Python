import subprocess
import os 
from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
conf=ConfigParser()
conf.read(conf_file)


iis=conf['IIS']


script_path=dir+"/Powershell_scripts/renew.ps1"    
# Build the PowerShell command
command = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", script_path, iis['hostname'], iis['CAName'],iis['sitename'],iis['certfile']]

# Run the PowerShell command
result = subprocess.run(command, capture_output=True, text=True)

# Print the PowerShell script output
print(result.stdout)





  
