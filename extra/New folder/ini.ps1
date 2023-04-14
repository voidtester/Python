if (-not(Get-Module -Name PSCX)) {
    Import-Module PSCX
}

$currentDirectory = Get-Location | Select-Object -ExpandProperty Path
$subdirectory = "Powershell\renew.ps1"
$path = Join-Path -Path $currentDirectory -ChildPath $subdirectory
 $path
# Read the contents of the INI file
$config = Get-IniContent -Path $path
