$keystore = $args[0]
$pass = $args[1]
$csr = $args[2]
$cn = $args[3]
$o = $args[4]
$st = $args[5]
$ou = $args[6]
$l = $args[7]
$c = $args[8]

$keytool = "$Env:JAVA_HOME\bin\keytool.exe"

& $keytool -genkey -v -keyalg RSA -alias tomcat -keystore $keystore -storepass $pass -dname "CN=$cn,OU=$ou,O=$o,L=$l,ST=$st,C=$c"
& $keytool -certreq -alias tomcat -keyalg RSA -file $csr -keystore $keystore -storepass $pass