# Set the API token and zone name
$ApiToken = 'YOUR_API_TOKEN'

#Domain name 
$ZoneName = 'YOUR_ZONE_NAME'

# Function to create a DNS record
function New-DnsRecord($RecordName, $RecordValue)
{
    # Get the zone ID
    $ZoneId = (Invoke-RestMethod -Headers @{Authorization=('Bearer ' + $ApiToken)}) | Where-Object {$_.name -eq $ZoneName} | Select-Object -ExpandProperty id

    # Create the DNS record
    $RecordParams = @{
        name = $RecordName
        type = 'TXT'
        ttl = 3600
        content = $RecordValue
    }

    $RecordUrl = "https://api.cloudflare.com/client/v4/zones/$ZoneId/dns_records"
    Invoke-RestMethod -Uri $RecordUrl -Method POST -Headers @{Authorization=('Bearer ' + $ApiToken)} -ContentType 'application/json' -Body ($RecordParams | ConvertTo-Json)
}

# Function to delete a DNS record
function Remove-DnsRecord($RecordName)
{
    # Get the zone ID
    $ZoneId = (Invoke-RestMethod -Headers @{Authorization=('Bearer ' + $ApiToken)}) | Where-Object {$_.name -eq $ZoneName} | Select-Object -ExpandProperty id

    # Get the DNS record ID
    $RecordUrl = "https://api.cloudflare.com/client/v4/zones/$ZoneId/dns_records?name=$RecordName&type=TXT"
    $RecordId = (Invoke-RestMethod -Uri $RecordUrl -Method GET -Headers @{Authorization=('Bearer ' + $ApiToken)}) | Select-Object -ExpandProperty result | Select-Object -ExpandProperty id

    # Delete the DNS record
    $RecordUrl = "https://api.cloudflare.com/client/v4/zones/$ZoneId/dns_records/$RecordId"
    Invoke-RestMethod -Uri $RecordUrl -Method DELETE -Headers @{Authorization=('Bearer ' + $ApiToken)}
}

# Example usage
Create-DnsRecord '_acme-challenge.example.com' 'random_value'
Remove-DnsRecord '_acme-challenge.example.com'