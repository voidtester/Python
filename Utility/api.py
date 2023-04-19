from flask import Flask, jsonify, request
from Automation import *

app = Flask(__name__)

@app.route('/api/tomcat/certificate-renew', methods=['POST'])
def Certificate_renew_tomcat():
        try:
            certificate_renew_tomcat()
            return jsonify({"Certificate renewed successfully for Tomcat"}),200
        except Exception as e:
            return jsonify({'error': str(e)}),500

@app.route('/api/IIS/certificate-renew', methods=['POST'])
def Cert_import():
        try:
            certificate_renew_iis()
            return ({"Certificate renewed successfully for IIS "}),200     
        except Exception as e:
            return jsonify({'error': str(e)}),500
 
@app.route('/api/apache/certificate-renew', methods=['POST'])
def Crt_import():
        try:
            cert_import()
            return ({"Certificate renewed successfully for Apache "}),200     
        except Exception as e:
            return jsonify({'error': str(e)}),500
     
@app.route('/api/nginx/certificate-renew', methods=['POST'])
def ert_import():
        try:
            cert_import()
            return ({"Certificate renewed successfully for Nginx "}),200     
        except Exception as e:
            return jsonify({'error': str(e)}),500
 

if __name__ == '__main__':
    app.run(debug=True)