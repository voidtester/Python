$keystore = $args[0]
$pass = $args[1]

$keytool = "$Env:JAVA_HOME\bin\keytool.exe"

& $keytool -delete -alias rootca -keystore $keystore -storepass $pass
& $keytool -delete -alias issuingca -keystore $keystore -storepass $pass
& $keytool -delete -alias intermediateca -keystore $keystore -storepass $pass

