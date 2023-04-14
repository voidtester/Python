#Thumbprint using powershell 
import subprocess

def add_ssl_cert_to_binding(certfile, certstore, sitename):
    try:
        # Import certificate from file to store
        result = subprocess.run(["powershell", "-Command", f"$cert = Import-Certificate -FilePath '{certfile}' -CertStoreLocation Cert:\\{certstore}\\My; $cert.Thumbprint"], capture_output=True, text=True, check=True)
        cert_thumbprint = result.stdout.strip()

        # Get site from IIS
        result = subprocess.run(["powershell", "-Command", f"$site = Get-WebSite | Where-Object {{ $_.Name -eq '{sitename}' }}; if ($null -eq $site) {{ Write-Error 'Site not found.'; exit }}"], capture_output=True, text=True, check=True)

        # Get existing SSL bindings for site
        result = subprocess.run(["powershell", "-Command", f"$bindings = Get-WebBinding | Where-Object {{ $_.protocol -eq 'https' -and $_.ItemXPath.Contains('{sitename}') }}; if ($null -eq $bindings) {{ Write-Error 'No SSL bindings found.'; exit }}"], capture_output=True, text=True, check=True)

        # Add certificate to SSL binding
        result = subprocess.run(["powershell", "-Command", f"$bindings | ForEach-Object {{ $_.AddSslCertificate({cert_thumbprint}, '{certstore}') }}"], capture_output=True, text=True, check=True)

        return "Certificate bound successfully."

    except subprocess.CalledProcessError as e:
        return f"Failed to import certificate from file or add certificate to SSL binding: {e.stderr}"



########################################################
import win32com.client

def add_ssl_certificate(sitename, certhash, certstore):
    # Connect to IIS
    iis = win32com.client.Dispatch("IISNamespace")

    # Get site from IIS
    site = iis.GetObject("IIS://localhost/W3SVC/{}".format(sitename))

    # Check if site exists
    if not site:
        raise ValueError("Site not found.")

    # Get bindings for site
    bindings = site.ServerBindings

    # Check if bindings exist
    if not bindings:
        raise ValueError("No bindings found.")

    # Add SSL certificate to binding
    for binding in bindings:
        if binding.Protocol.lower() == "https":
            binding.SslCertificateHash = certhash
            binding.SslCertificateStoreName = certstore
            binding.SetInfo()

    print("Certificate bound successfully.")
    
##########################################################################################################################
#new approach for powershell script


def bind_certificate_to_iis_site(certstore, certfile, sitename):
    # define the PowerShell script as a formatted string
    script = '''# Import certificate from file to store

    try {{
        $cert = Import-Certificate -FilePath "{certfile}" -CertStoreLocation 'Cert:\{certstore}\My'
    }}
    catch {{
        Write-Error "Failed to import certificate from file."
    }}

    # Get certificate thumbprint
    $certhash = $cert.Thumbprint

    # Get site from IIS
    $site = Get-WebSite | Where-Object {{$_.Name -eq "{sitename}"}}

    # Check if site exists
    if ($null -eq $site) {{
        Write-Error "Site not found."
        exit
    }}

    # Check if bindings exist
    if ($null -eq $bindings) {{
        Write-Error "No SSL bindings found."
        exit
    }}

    # Load the WebAdministration module
    Import-Module WebAdministration

    # Get existing SSL bindings for site
    $bindings = Get-WebBinding | Where-Object {{$_.protocol -eq 'https' -and $_.ItemXPath.Contains("{sitename}")}}
    $bindings.AddSslCertificate($certhash, "my")

    Write-Output "Certificate bound successfully."
    '''

    # format the script with the values
    formatted_script = script.format(certstore=certstore, certfile=certfile, sitename=sitename)

    # run the script using subprocess.run()
    result = subprocess.run(["powershell", "-Command", formatted_script], capture_output=True)

    # check if the PowerShell script ran successfully
    if result.returncode != 0:
        raise Exception("Error: PowerShell script returned a non-zero exit code.")

    # return the output of the script as a string
    return result.stdout.decode("utf-8")
