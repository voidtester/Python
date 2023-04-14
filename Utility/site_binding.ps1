$sitename = "$arg[0]" 
 
$certstore = "LocalMachine" 
 
$certfile="$arg[1]" 
 
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
 
 
# Get Import-Module WebAdministrationexisting SSL bindings for site 
 
$bindings = Get-WebBinding | Where-Object {$_.protocol -eq 'https' -and $_.ItemXPath.Contains($sitename)} 
 
$bindings.AddSslCertificate($certhash, "my") 
  
Write-Output "Certificate bound successfully."