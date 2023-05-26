import subprocess 
# create fresh keystore for tomcat server (ACME)
keystore = "echo {passw} | keytool -genkey -v -keyalg RSA -alias tomcat -keystore {key} -storepass {passw} -dname CN={common},OU={unit},O={org},L={local},ST={state},C={country}".format(
    key="/opt/keystore.jks", passw="password", common="test", unit="IT",
    org="Encon", local="Texas", state="Dallas", country="US")

try:
    subprocess.run(keystore, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(e)

# import the certificate to keystore
    imp = f'echo "yes" | keytool -import -trustcacerts -alias tomcat -keystore "/opt/keystore.jks" -storepass "password" -file "/opt//opt/SSL.cer"'
    try:
        subprocess.run(imp, shell=True, check=True)
    except subprocess.CalledProcessError:
        print("Certificate not found")
    