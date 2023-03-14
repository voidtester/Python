# Check if input arguments are provided
if ($args.Count -lt 2) {
    Write-Error "Please provide keystore path and password as input arguments."
    exit
}

# Assign input arguments to variables
$keystore = $args[0]
$pass = $args[1]

# Check if keystore and password are not empty
if ([string]::IsNullOrEmpty($keystore) -or [string]::IsNullOrEmpty($pass)) {
    Write-Error "Keystore path and password cannot be empty."
    exit
}

# Set paths for certificates
$root = $args[2]
$issuing = $args[3]
$intermediate = $args[4]
# Check if certificates exist
if (![string]::IsNullOrEmpty($root) -and -not (Test-Path $root -PathType Leaf)) {
    Write-Error "Root certificate file does not exist at path: $root"
    exit
}

if (![string]::IsNullOrEmpty($issuing) -and -not (Test-Path $issuing -PathType Leaf)) {
    Write-Error "Issuing certificate file does not exist at path: $issuing"
    exit
}

if (![string]::IsNullOrEmpty($intermediate) -and -not (Test-Path $intermediate -PathType Leaf)) {
    Write-Error "Intermediate certificate file does not exist at path: $intermediate"
    exit
}

# Import certificates if they exist
$keytool = "$Env:JAVA_HOME\bin\keytool.exe"

if (![string]::IsNullOrEmpty($root)) {
    & $keytool -import -trustcacerts -alias rootca -keystore $keystore -file $root -storepass $pass
}

if (![string]::IsNullOrEmpty($issuing)) {
    & $keytool -import -trustcacerts -alias issuingca -keystore $keystore -file $issuing -storepass $pass
}

if (![string]::IsNullOrEmpty($intermediate)) {
    & $keytool -import -trustcacerts -alias intermediateca -keystore $keystore -file $intermediate -storepass $pass
}

# List of imported certificates 
& $keytool -list -keystore $keystore -storepass $pass

pause
