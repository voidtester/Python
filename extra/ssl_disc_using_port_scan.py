import socket
import ssl
import datetime

port_range = range(442,445)

class ssl_check():
    
    def __init__(self, hostname):
        for port in port_range:
            try:
                # Create a TCP socket and connect to the target host/port
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)  # Set a timeout of 5 seconds
                sock.connect((hostname, port))

                # Wrap the socket with an SSL context
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
                    # Get the SSL certificate from the server and print its details
                    cert = ssock.getpeercert()
            
                    print(f'Found SSL certificate on port {port}:')
                    subject = dict(x[0] for x in cert['subject'])
                    common_name = subject.get('commonName', None)
                    print(f'  Common Name: {common_name}')
                    Exp_ON=datetime.datetime.strptime(cert['notAfter'], ssl_date_fmt)
                    Days_Remaining= Exp_ON - datetime.datetime.utcnow()
                    print("Expires ON:- %s\nRemaining:- %s" %(Exp_ON,Days_Remaining))
                    print()

            except (socket.timeout, ConnectionRefusedError):
                # Ignore timeout and connection refused errors
                pass
            finally:
                # Always close the socket when done
                sock.close()

domains = ['google.com', 'yahoo.com','instagram.com']

# I am using map function to iterate through the list.
list(map(ssl_check, domains))