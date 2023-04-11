import os
import requests

# Set the API token, record name, and record value
api_token = 'YOUR_API_TOKEN'

record_name = '_acme-challenge.' + os.environ['CERTBOT_DOMAIN']
record_value = os.environ['CERTBOT_VALIDATION']
zone_name = os.environ['www.example.com'].split('.', 1)[1]

# Get the zone ID
zone_url = f'https://api.cloudflare.com/client/v4/zones?name={zone_name}'
zone_response = requests.get(zone_url, headers={'Authorization': f'Bearer {api_token}'})
zone_data = zone_response.json()['result'][0]
zone_id = zone_data['id']

# Create the TXT record
record_url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
record_params = {
    'name': record_name,
    'type': 'TXT',
    'content': record_value,
    'ttl': 3600
}
record_response = requests.post(record_url, headers={'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'}, json=record_params)
record_data = record_response.json()

# Print the result
print(record_data)
