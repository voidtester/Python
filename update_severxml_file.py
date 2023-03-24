import os 
from configparser import ConfigParser
dir=os.getcwd()
conf_file=dir+"\conf.ini"
conf=ConfigParser()
conf.read(conf_file)

tomcat=conf['tomcat']
import xml.etree.ElementTree as ET

# parse the server.xml file
tree = ET.parse('G:\server_copy.xml')
root = tree.getroot()

# find the Service element with name="Catalina"
service_elem = root.find("./Service[@name='Catalina']")

# create the Connector element
connector_elem = ET.Element('Connector')
connector_elem.set('port', '8443')
connector_elem.set('protocol', 'HTTP/1.1')
connector_elem.set('connectionTimeout', '20000')
connector_elem.set('redirectPort', '8443')
connector_elem.set('SSLEnabled', 'true')
connector_elem.set('scheme', 'https')
connector_elem.set('secure', 'true')
connector_elem.set('sslProtocol', 'TLS')
connector_elem.set('keystoreFile', tomcat['keystore'])
connector_elem.set('keystorePass', tomcat['pass'])

# insert the new Connector element before the first Engine element
inserted = False
for service_child in service_elem:
    if service_child.tag == 'Engine':
        service_elem.insert(list(service_elem).index(service_child), connector_elem)
        inserted = True
        break

if not inserted:
    service_elem.append(connector_elem)

# write the updated server.xml file

tree.write('G:\server_copy1.xml')