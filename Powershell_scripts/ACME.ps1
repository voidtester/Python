# Install Certbot and its dependencies
Invoke-WebRequest https://dl.eff.org/certbot-auto -OutFile certbot-auto 
.\certbot-auto --install-only

# Set up certificate for your domain
$domain = "example.com"
$certbotArgs = "--agree-tos --email your-email@example.com -d $domain"
.\certbot-auto certonly --webroot -w "C:\inetpub\wwwroot" $certbotArgs

# Add scheduled task for automatic renewal
$taskName = "Certbot Renewal"
$taskCommand = "C:\certbot\certbot-auto renew"
$taskTrigger = New-ScheduledTaskTrigger -AtStartup -RandomDelay 00:30:00
$taskSettings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 01:00:00
$taskAction = New-ScheduledTaskAction -Execute $taskCommand
$taskPrincipal = New-ScheduledTaskPrincipal -UserID "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName $taskName -Trigger $taskTrigger -Settings $taskSettings -Action $taskAction -Principal $taskPrincipal
