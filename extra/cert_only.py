import socket
import ssl
import re

def check_ssl_certificate(ip_address, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)

        # Connect to the server
        sock.connect((ip_address, port))

        # Wrap the socket with SSL
        context = ssl.create_default_context()
        with context.wrap_socket(sock, server_hostname=ip_address) as ssock:
            # Get the SSL certificate
            cert = ssock.getpeercert()

            # Check if the certificate is valid
            if cert and ('subject' in cert) and ('issuer' in cert):
                subject = dict(x[0] for x in cert['subject'])
                issuer = dict(x[0] for x in cert['issuer'])
                return {'ip_address': ip_address, 'port': port, 'cert_subject': subject, 'cert_issuer': issuer}

    except Exception as e:
        pass

def scan_ports(ip_address, start_port, end_port):
    ssl_ports = []

    for port in range(start_port, end_port+1):
        try:
            # Check if SSL certificate is present on this port
            ssl_cert = check_ssl_certificate(ip_address, port)

            # If SSL certificate is present, add it to the list of SSL ports
            if ssl_cert:
                ssl_ports.append(ssl_cert)

        except Exception as e:
            pass

    return ssl_ports

ssl_ports = scan_ports('192.168.0.1', 1, 1000)
