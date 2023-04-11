from flask import Flask, jsonify, request
from Automation import *

app = Flask(__name__)

@app.route('/api/tomcat/certificate-generation', methods=['POST'])
def Certificate_generation():
        try:
            certificate_generation_Tomcat()
            return jsonify({"Certificate successfully issued"}),200
        except Exception as e:
            return jsonify({'error': str(e)}),500

@app.route('/api/tomcat/certimport', methods=['POST'])
def Cert_import():
        try:
            cert_import()
            return ({"Certificate imported to keystore successfully"}),200     
        except Exception as e:
            return jsonify({'error': str(e)}),500
 
        
@app.route('/api/iis/renew', methods=['POST'])
def certificate_renew_IIS():
        try:
            certificate_renew_iis()
            return jsonify({"Certificate successfully renewed"}),200
        except Exception as e:
            return jsonify({'error': str(e)}),500
   

@app.route('/api/certbot', methods=['POST'])
def certbot_certificate():
        try:
            certbot_certificate()
            return jsonify({"Certificate successfully issued"}),200    
        except Exception as e:
            return jsonify({'error': str(e)}),500

        
@app.route('/api/WinAcme/tomcat', methods=['POST'])
def Winacme_certificate_Tomcat():
    try:
        winacme_certificate_tomcat()
        return jsonify({"Certificate successfully issued"}),200
    except Exception as e:
        return jsonify({'error': str(e)}),500

@app.route('/api/WinAcme/iis', methods=['POST'])
def Winacme_certificate_IIS():
    try:
        winacme_certificate_iis()
        return jsonify({"Certificate successfully issued"}),200
    except Exception as e:
        return jsonify({'error': str(e)}),500


@app.route('/api/Certbot/renew-cert', methods=['POST'])
def Certbot_certificate_renew():
    try:
        certbot_certificate_renew()
        return jsonify({"Certificate successfully renewed"}),200
    except Exception as e:
        return jsonify({'error': str(e)}),500

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)