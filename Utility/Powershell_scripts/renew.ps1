# Define parameters

$hostname = "$arg[0]"

$CAName = "$arg[1]"

$sitename = "$arg[2]"

$certstore = "LocalMachine"

$certfile = "$arg[3]"

$csr="$arg[4]"

$certchain="$arg[5]"

$response="$arg[6]"



# Create a new certificate request using policy.inf

try {

    certreq.exe -new -q -config "$hostname\$CAName" policy.inf $csr

}

catch {

    Write-Error "Failed to create certificate request."

}

# Submit the certificate request to the CA and save the response files

try {

    certreq.exe -submit -q -config "$hostname\$CAName" $csr $certfile $certchain $response

}

catch {

    Write-Error "Failed to submit certificate request."

}

# Import certificate from file to store

try {

    $cert = Import-Certificate -FilePath $certfile -CertStoreLocation Cert:\$certstore\My

}

catch {

    Write-Error "Failed to import certificate from file."

}

# Get certificate thumbprint

$certhash = $cert.Thumbprint

# Get site from IIS

$site = Get-WebSite | Where-Object {$_.Name -eq $sitename}

# Check if site exists

if ($null -eq $site) {

    Write-Error "Site not found."

    exit

}

# Check if bindings exist

if ($null -eq $bindings) {

    Write-Error "No SSL bindings found."

    exit

}

# Load the WebAdministration module

Import-Module WebAdministration

# Get existing SSL bindings for site

$bindings = Get-WebBinding | Where-Object {$_.protocol -eq 'https' -and $_.ItemXPath.Contains($sitename)}

$bindings.AddSslCertificate($certhash, "my")
 
Write-Output "Certificate bound successfully."

Remove-Item $certfile

Remove-Item $certchain

Remove-Item $response

Remove-Item $csr