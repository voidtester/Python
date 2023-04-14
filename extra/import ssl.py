import ssl
ip="169.254.0.1"
for ip in ips_to_scan:
    for port in range(65536):
        try:
            yield ssl.get_server_certificate((ip, port,))
        except:
            pass
