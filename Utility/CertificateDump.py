import subprocess
import csv
from datetime import datetime, timedelta
from classes.db import get_value
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
Collection_Name = "Reports"

try:
    # Connect to the MongoDB server
    client = MongoClient(f"mongodb://{mongo['IP']}:27017/")
    database = client["CertSecure"]
    collection = database[Collection_Name]
except:
    print('Error, could not connect to DB!')


def CertificateDump(dump_interval, CAConfig, ip_address):
    insert_log(ip_address, 'debug', 'Take Certificate Dump',
               f'CertificateDump() function invoked with input '
               f'parameters - {dump_interval}, {CAConfig}, {ip_address}')
    try:
        try:
            # Run certutil command and capture output
            command = f'certutil -config "{CAConfig}" -view -out SerialNumber,DistinguishedName,EMail,DeviceSerialNumber,CommonName,Country,Organization,OrgUnit,Locality,State,NotBefore,NotAfter,CertificateHash,CertificateTemplate,PublicKeyLength,PublicKeyAlgorithm,Request.RevokedWhen,Request.RevokedReason,Request.EndorsementKeyHash,Request.EndorsementKeyHash,Request.Disposition,Request.DispositionMessage -Restrict "Disposition>=20" csv'
            output = subprocess.check_output(command, shell=True)
            insert_log(ip_address, 'debug', 'Take Certificate Dump',
                       f'Certutil Command Executed for CA - {CAConfig}')
        except Exception as e:
            insert_log(ip_address, 'debug', 'Take Certificate Dump', 'Error in Certutil Command Execution')
            insert_log(ip_address, 'error', 'Take Certificate Dump', f'Error in Certutil Command with error message - {str(e)}')
            return str(e)

        # Parse output into list of dictionaries
        reader = csv.DictReader(output.decode('utf-8').splitlines())
        certificates = list(reader)

        # Convert string fields to appropriate format
        for cert in certificates:
            if cert['Serial Number'] == 'EMPTY':
                continue
            cert['Serial Number'] = cert['Serial Number'].strip()
            
            cert['DistinguishedName'] = cert['Issued Distinguished Name'].strip()
            cert['EMail'] = cert['Issued Email Address'].strip()
            cert['DeviceSerialNumber'] = cert['Issued Device Serial Number'].strip()
            cert['CommonName'] = cert['Issued Common Name'].strip()
            cert['Country'] = cert['Issued Country/Region'].strip()
            cert['Organization'] = cert['Issued Organization'].strip()
            cert['OrgUnit'] = cert['Issued Organization Unit'].strip()
            cert['Locality'] = cert['Issued City'].strip()
            cert['State'] = cert['Issued State'].strip()
            cert['NotBefore'] = datetime.strptime(cert['Certificate Effective Date'], '%m/%d/%Y %I:%M %p')
            cert['NotAfter'] = datetime.strptime(cert['Certificate Expiration Date'], '%m/%d/%Y %I:%M %p')
            cert['CertificateHash'] = cert['Certificate Hash'].strip()
            cert['CertificateTemplate'] = cert['Certificate Template'].strip()
            cert['Request.RevokedWhen'] = cert['Revocation Date'].strip()
            cert['Request.RevokedReason'] = cert['Revocation Reason'].strip()
            cert['Request.EndorsementKeyHash'] = cert['Endorsement Key Hash'].strip()
            cert['Request.Disposition'] = cert['Request Disposition'].strip()
            cert['Request.DispositionMessage'] = cert['Request Disposition Message'].strip()
            cert['Public key Length'] = cert['Public Key Length'].strip()
            cert['Public Key Algorithm'] = cert['Public Key Algorithm'].strip()

        reports_data = {}
        try:
            # Insert or update certificates in MongoDB
            for cert in certificates:
                ca_config = CAConfig
                if ca_config not in reports_data:
                    reports_data[CAConfig] = {'Certificates': [], 'dump_time': datetime.utcnow(),
                                              'dump_interval': dump_interval}
                if cert['Serial Number'] == 'EMPTY':
                    continue
                reports_data[ca_config]['Certificates'].append({
                    'serial_number': cert['Serial Number'],
                    'distinguished_name': cert['DistinguishedName'],
                    'issued_email_address': cert['EMail'],
                    'issued_device_serial_number': cert['DeviceSerialNumber'],
                    'common_name': cert['CommonName'],
                    'country': cert['Country'],
                    'organization': cert['Organization'],
                    'organization_unit': cert['OrgUnit'],
                    'city': cert['Locality'],
                    'state': cert['State'],
                    'certificate_effective_date': cert['NotBefore'],
                    'certificate_expiration_date': cert['NotAfter'],
                    'certificate_hash': cert['CertificateHash'],
                    'certificate_template': cert['CertificateTemplate'],
                    'public_key_length': cert['Public Key Length'],
                    'public_key_algorithm': cert['Public Key Algorithm'],
                    'revocation_date': cert['Request.RevokedWhen'],
                    'revocation_reason': cert['Request.RevokedReason'],
                    'endorsement_key_hash': cert['Request.EndorsementKeyHash'],
                    'request_disposition': cert['Request.Disposition'],
                    'request_disposition_message': cert['Request.DispositionMessage'],
                })
            insert_log(ip_address, 'debug', 'Take Certificate Dump', f'Keys Formatted into proper format coming from the '
                                                                     f'certutil command')
        except Exception as e:
            insert_log(ip_address, 'debug', 'Take Certificate Dump', f'Exception in keys formatting - {str(e)}')

        # Insert each CA name and its associated list of certificates into the Reports collection as a single document
        for ca_config, data in reports_data.items():
            collection.update_one(
                {'CAConfig': ca_config},
                {'$addToSet': {'Certificates': {'$each': data['Certificates']}},
                 '$set': {'dump_time': data['dump_time'], 'dump_interval': data['dump_interval']}},
                upsert=True
            )
        insert_log(ip_address, 'success', 'Certificate Dump', f'Certificate Dump Taken Successfully for CAConfig - {CAConfig}')
        insert_log(ip_address, 'info', 'Certificate Dump', f'Certificate Dump Taken for CA - {CAConfig}')
        return
    except Exception as e:
        insert_log(ip_address, 'error', 'Take Certificate Dump', f'Error in CertificateDump() function with error message - {str(e)}')


def check_and_take_dump(CAConfig, ip_address):
    insert_log(ip_address, 'debug', 'Check and take dump', f'check_and_take_dump() function invoked with input '
                                                           f'parameters - {CAConfig},{ip_address}')
    try:
        doc = collection.find_one({'CAConfig': CAConfig})
        dump_interval_hours = doc['dump_interval']
        dump_time = datetime.fromisoformat(str(doc['dump_time']))

        # Check if enough time has elapsed since the last dump
        time_since_dump = datetime.utcnow() - dump_time
        last_dump = timedelta(hours=dump_interval_hours)
        if time_since_dump >= last_dump:
            # Enough time has elapsed, so run the CertificateDump function
            CertificateDump(dump_interval_hours, CAConfig, ip_address)
            insert_log(ip_address, 'success', 'Check and take dump',
                       f'Dump taken successfully for CA - {CAConfig}')
        else:
            insert_log(ip_address, 'debug', 'Check and take dump',
                       f'Dump not taken as last dump was taken f{dump_interval_hours} hours ago for CA - {CAConfig}')
            return
    except:
        CertificateDump(dump_interval=3, CAConfig=CAConfig, ip_address=ip_address)
        insert_log(ip_address, 'debug', 'Check and take dump',
                   f'No Dump Exist for CA - {CAConfig}, so Fresh Dump taken with dump intervals set to 3 hours')
        insert_log(ip_address, 'success', 'Check and take dump',
                   f'No Dump Exist for CA - {CAConfig}, so Fresh Dump taken with dump intervals set to 3 hours')


def update_dump_interval_function(CAConfig, dump_interval, ip_address):
    insert_log(ip_address, 'debug', 'Update dump interval',
               f'update_dump_interval_function() function invoked with input '
               f'parameters - {CAConfig}, {dump_interval},{ip_address}')
    try:
        # Update the document matching the provided CAName with the new dump_interval value
        collection.update_one({"CAConfig": CAConfig}, {"$set": {"dump_interval": dump_interval}})
        insert_log(ip_address, 'success', 'Update dump interval',
                   f'Dump Intervals Updated to {dump_interval} hours for CA - {CAConfig}')
        return dict(Message=f"Dump interval updated to {dump_interval} for CA {CAConfig}")
    except Exception as e:
        insert_log(ip_address, 'error', 'Update dump interval',
                   f'Error in update_dump_interval_function() with Error Message - {str(e)}')
        return dict(Error_Message=str(e))


def get_dump_interval_function(CAConfig, ip_address):
    insert_log(ip_address, 'debug', 'Get dump interval',
               f'get_dump_interval_function() function invoked with input '
               f'parameters - {CAConfig}, {ip_address}')
    try:
        # Find the CA document in the database
        ca_doc = collection.find_one({"CAConfig": CAConfig})
        # If the CA document is found, return the dump intervals
        if ca_doc:
            insert_log(ip_address, 'success', 'Get dump interval',
                       f'Dump Intervals Data Returned Successfully for CA - {CAConfig}')
            return {
                "CAConfig": CAConfig,
                "DumpIntervals": ca_doc["dump_interval"]
            }
        else:
            insert_log(ip_address, 'debug', 'Get dump interval',
                       f'No CA found with CAConfig - {CAConfig}')
            insert_log(ip_address, 'error', 'Get dump interval',
                       f'No CA found with CAConfig - {CAConfig}')
            return dict(Error_Message=f"No CA found with name {CAConfig}")
    except Exception as e:
        insert_log(ip_address, 'error', 'Get dump interval',
                   f'Error in get_dump_interval_function() with Error Message - {str(e)}')
        return dict(Error_Message=str(e))


def get_all_ca_names(ip_address):
    insert_log(ip_address, 'debug', 'Get All CA Names',
               f'get_all_ca_names() function invoked with input '
               f'parameter - {ip_address}')
    try:
        # Retrieve all unique CAName values from the collection
        ca_configs = get_value('CAConfig')
        insert_log(ip_address, 'success', 'Get All CA Names',
                   f'A list containing all available CA Configurations returned successfully')
        return ca_configs
    except Exception as e:
        insert_log(ip_address, 'error', 'Get All CA Names',
                   f'Error in get_all_ca_names() function with error message -{str(e)}')
        return {
            'Error_Message': str(e)
        }
