from flask import Flask, jsonify
from Automation import *

app = Flask(__name__)


@app.route('/')
def root():
        return "Welcome to Root directory"
        
@app.route('/api/tomcat/certificate-renew')
def Certificate_renew_tomcat():
        try:
            certificate_renew_tomcat()
            return {"Certificate renewed successfully for Tomcat"}
        except Exception as e:
            return jsonify({'error': str(e)})
@app.route('/api/IIS/certificate-renew')
def IIS():
        try:
            certificate_renew_iis()
            return ({"Certificate renewed successfully for IIS "})     
        except Exception as e:
            return jsonify({'error': str(e)})

@app.route('/api/apache/certificate-renew')
def apche():
        try:
            certificate_renew_apache()
            return ({"Certificate renewed successfully for Apache "})  
        except Exception as e:
            return jsonify({'error': str(e)})
     
@app.route('/api/nginx/certificate-renew')
def nginx():
        try:
            certificate_renew_nginx()
            return ({"Certificate renewed successfully for Nginx "})     
        except Exception as e:
            return jsonify({'error': str(e)})
 

if __name__ == '__main__':
    app.run(debug=True)