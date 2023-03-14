from flask import Flask, jsonify ,request
import subprocess
import configparser
import os
dir = os.getcwd()
config = configparser.ConfigParser()
config.read(dir+'\conf.ini')

tomcat = config['tomcat']
iis = config['IIS']
acme = config['ACME']

app = Flask(__name__)

@app.route('/api/tomcat/csr', methods=['GET'])
def get_setup_tomcat():
    if (request.method == 'GET'):
        keystore="keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(key=tomcat['keystore'], passw=tomcat['pass'],common=tomcat['cn'],unit=tomcat['ou'],org=tomcat['o'],local=tomcat['l'],state=tomcat['st'],country=tomcat['c'])

        print(keystore)
        #os.system(keystore_command)

        csr="keytool -certreq -alias tomcat -keyalg RSA -file {csrfile} -keystore {key} -storepass {passw}".format(csrfile=tomcat['csr'], key=tomcat['keystore'],passw=tomcat['pass'])
        print(csr) 
        #os.system(csr)
    return ""


@app.route('/api/tomcat/certimport', methods=['GET'])
def cert_import():
    if (request.method == 'GET'):
        rca="keytool -import -trustcacerts -alias rootca -keystore {key} -storepass {passw} -file {rootca}".format(key=tomcat['kesytore'],passw=tomcat['pass'],rootca=tomcat['root'])
        ica="keytool -import -trustcacerts -alias issuingca -keystore {key} -storepass {passw} -file {issuingca}".format(key=tomcat['keystore'],passw=tomcat['pass'],issuingca=tomcat['issuing']) 
        intca="keytool -import -trustcacerts -alias intermediateca -keystore {key} -storepass {passw} -file {intermediateca}".format(key=tomcat['kesytore'],passw=tomcat['pass'],intermediateca=tomcat['intermediate'])
        print(rca)
        print(ica)
        print(intca)   
    return ""


@app.route('/api/iis/renew', methods=['GET'])
def get_config_iis():
    script_path=dir+"/Powershell_scripts/renew.ps1"    
    # Build the PowerShell command
    command = ["powershell.exe", "-ExecutionPolicy", "Unrestricted", script_path, iis['hostname'], iis['CAName'],iis['sitename'],iis['certfile']]

    # Run the PowerShell command
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the PowerShell script output
    print(result.stdout)

    return jsonify(result)


@app.route('/api/config/acme', methods=['GET'])
def get_config_acme():
    if (request.method == 'GET'):
        result = {
            "domain": acme['domain']
        }
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
