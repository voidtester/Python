import socket
import ssl

def ssl_scan(target, ports):
    """Scan for SSL certificates on specified ports of a target host."""
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect((target, port))
            context = ssl.create_default_context()
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                cert = ssock.getpeercert()
                print(f"Port {port} - SSL certificate details:")
                for key, value in cert.items():
                    if key == 'subject':
                        print(f"Subject: {value}")                    
                    elif key == 'notBefore':
                        print(f"Not valid before: {value}")
                    elif key == 'notAfter':
                        print(f"Not valid after: {value}")
        except:
            pass

# Example usage
for ports in range(1,450):
    ssl_scan('google.com',list[ports])
