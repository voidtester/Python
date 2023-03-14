from flask import Flask, jsonify
import configparser
import os
dir=os.getcwd()

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(dir+'\conf.ini')

tomcat=config['tomcat']
iis=config['IIS']
acme=config['ACME']

@app.route('/api/config/tomcat/setup',methods = ['GET'])
def get_setup_tomcat():
     if(request.method == 'GET'):
         result={
             "keystore":tomcat['keystore'],
             "pass":tomcat['pass'],
             "cn":tomcat['keystore'],
             "ou": tomcat['cn'],
             "o":tomcat['o'],
             "st": tomcat['st'],
             "c": tomcat['c'],
             "csr":tomcat['csr']
            }
         return jsonify(result)

@app.route('/api/config/tomcat/cert',methods = ['GET'])
def get_config_tomcat():
     if(request.method == 'GET'):
         results={
        "certificate path":{
                "Root CA":tomcat['root'],
                "intermediate CA":tomcat['intermediate'],
                "Issuing CA":tomcat['issuing']
        }
    }
         return jsonify(results)
    
@app.route('/api/config/iis',methods = ['GET'])
def get_config_iis():
     if(request.method == 'GET'):
         result={
        "hostname":iis['hostname'],
        "caname":iis['caname'], 
        "sitename":iis['sitename'],
        "certfile":iis['certfile'],

    }
         return jsonify(result)

@app.route('/api/config/acme',methods = ['GET'])
def get_config_acme():
    if(request.method == 'GET'):
        result={
        "domain":acme['domain']
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
