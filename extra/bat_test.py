import subprocess
import os
dir=os.getcwd()
bat_path= dir +'batch_files_tomcat/'
print(bat_path)
subprocess.call([r'dir\batch_files_tomcat\keystore.bat',])