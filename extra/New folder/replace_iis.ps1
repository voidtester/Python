#Load the configuration file
$currentDirectory = Get-Location | Select-Object -ExpandProperty Path
$subdirectory = "conf.ini"
$confpath = Join-Path -Path $currentDirectory -ChildPath $subdirectory

$config = Get-Content -Path $confpath -Raw | ConvertFrom-StringData

# Define parameters

$hostname = $config.IIS.hostname

$CAName = $config.IIS.caname

$sitename = $config.IIS.sitename

$certstore = "LocalMachine"

$certfile = $config.IIS.certfile

# Create a new certificate request using policy.inf

try {

    certreq.exe -new -q -config "$hostname\$CAName" policy.inf c:\temp\request.csr

}

catch {

    Write-Error "Failed to create certificate request."

}

# Submit the certificate request to the CA and save the response files

try {

    certreq.exe -submit -q -config "$hostname\$CAName" c:\temp\request.csr $certfile c:\temp\cert.p7b c:\temp\response.ful

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

Remove-Item c:\temp\cert.p7b

Remove-Item c:\temp\response.ful

Remove-Item c:\temp\request.csr