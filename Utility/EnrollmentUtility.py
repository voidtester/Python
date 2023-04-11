from configparser import ConfigParser
from pymongo import MongoClient
from classes.logging import insert_log

# Read the configuration file
conf = ConfigParser()
conf.read('conf.ini')

# Get the MongoDB configuration from the configuration file
mongo = conf['Mongo']

# Valiables
client = None
database = None
Collection_Name = "EnrolledCertificates"

try:
    # Connect to the MongoDB server
    client = MongoClient(f"mongodb://{mongo['IP']}:27017/")
    database = client["CertSecureManager"]
    collection = database[Collection_Name]
except:
    print('Error, could not connect to DB!')


def dump_new_certificates_data(certificate_template, CAConfig, csr_content, email, san_attributes, notes, ip_address):
    insert_log(ip_address, 'debug', 'Dump Newly Enrolled Certificate Data into Database',
               f'dump_new_certificates_data() function invoked with input parameters - '
               f'{certificate_template}, {CAConfig}, {csr_content}, {email}, {san_attributes}, {notes}, {ip_address}')
    try:
        certificate_data = {
            'type': 'Certificate',
            'CAConfig': CAConfig,
            'certificate_template': certificate_template,
            'csr_content': csr_content,
            'email': email,
            'san_attributes': san_attributes,
            'notes': notes
        }
        result = collection.insert_one(certificate_data)
        if result.acknowledged:
            insert_log(ip_address, 'success', 'Dump Newly Enrolled Certificate Data into Database',
                       'Enrolled Certificate Metadata stored successfully in database')
            return {'Message': 'Data inserted successfully!'}
        else:
            insert_log(ip_address, 'debug', 'Dump Newly Enrolled Certificate Data into Database',
                       'Error dumping newly enrolled Certificate metadata in database')
            return {'Message': 'Insert operation failed.'}
    except Exception as e:
        insert_log(ip_address, 'error', 'Dump Newly Enrolled Certificate Data into Database',
                   f'Error in dump_new_certificates_data() function with error message - {str(e)}')
        return {'Error': str(e)}


def dump_new_csr_data(key_length, common_name, organization, organization_unit,
                      city, state, country_code, email, san_attributes, ip_address):
    insert_log(ip_address, 'debug', 'Dump Generated CSR Data into Database',
               f'dump_new_csr_data() function invoked with input parameters - {key_length}, {common_name}, {organization}, {organization_unit}, {city}, {state}, {country_code}, {email}, {san_attributes}, {ip_address}')
    try:
        csr_data = {
            'type': 'CSR',
            'key_length': key_length,
            'common_name': common_name,
            'organization': organization,
            'organization_unit': organization_unit,
            'city': city,
            'state': state,
            'country_code': country_code,
            'email': email,
            'san_attributes': san_attributes
        }
        result = collection.insert_one(csr_data)
        if result.acknowledged:
            insert_log(ip_address, 'success', 'Dump Generated CSR Data into Database',
                       'Newly Generated CSR Data dumped successfully into database')
            return {'Message': 'Data inserted successfully!'}
        else:
            insert_log(ip_address, 'debug', 'Dump Generated CSR Data into Database',
                       'Error dumping new CSR data in database')
            return {'Message': 'Insert operation failed.'}
    except Exception as e:
        insert_log(ip_address, 'error', 'Dump Generated CSR Data into Database',
                   f'Error in dump_new_csr_data() function with error message - {str(e)}')
        return {'Error': str(e)}
