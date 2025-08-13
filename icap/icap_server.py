import socketserver
import time
import threading
import socket
import os

class ICAPHandler(socketserver.StreamRequestHandler):
    """
    A simple handler for ICAP requests.
    It responds to OPTIONS and REQMOD requests.
    Now includes X-Next-Services header for dynamic service chaining.
    """
    
    def check_service_health(self, host, port):
        """Check if a service is available by attempting to connect to it."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # 2 second timeout
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def get_next_services(self, current_service):
        """Determine next services based on current service and health checks."""
        # Get hostname to determine current service
        hostname = os.environ.get('HOSTNAME', 'icap-server')
        print(f"Current service hostname: {hostname}")
        
        # SECURITY: Only allow routing to pre-approved services
        # This whitelist should match exactly what's configured in squid.conf
        ALLOWED_SERVICES = {
            'icap-server': ['reqmod_service2'],      # Only allow routing to service2
            'icap-server2': ['reqmod_service1']      # Only allow routing to service1
        }
        
        allowed_for_host = ALLOWED_SERVICES.get(hostname, [])
        if not allowed_for_host:
            print(f"No routing allowed for hostname: {hostname}")
            return []
        
        # Check health of other services and return available ones
        available_services = []
        if hostname == 'icap-server':
            # Check if icap-server2 is healthy
            print("Checking health of icap-server2...")
            if self.check_service_health('icap-server2', 1344):
                # SECURITY: Only add if it's in our whitelist
                if 'reqmod_service2' in allowed_for_host:
                    available_services.append('reqmod_service2')
                    print("icap-server2 is healthy - adding reqmod_service2 to next services")
                else:
                    print("reqmod_service2 not in allowed list for this host")
            else:
                print("icap-server2 is not healthy - skipping")
        elif hostname == 'icap-server2':
            # Check if icap-server is healthy  
            print("Checking health of icap-server...")
            if self.check_service_health('icap-server', 1344):
                # SECURITY: Only add if it's in our whitelist
                if 'reqmod_service1' in allowed_for_host:
                    available_services.append('reqmod_service1')
                    print("icap-server is healthy - adding reqmod_service1 to next services")
                else:
                    print("reqmod_service1 not in allowed list for this host")
            else:
                print("icap-server is not healthy - skipping")
        
        # SECURITY: Log all routing decisions for audit
        print(f"SECURITY AUDIT: Host={hostname}, Allowed={allowed_for_host}, Final={available_services}")
        return available_services
    def handle(self):
        client_address = self.client_address
        print(f"Connection from {client_address}")
        try:
            # Read the request line
            request_line = self.rfile.readline().decode('utf-8').strip()
            if not request_line:
                return

            print(f"Request: {request_line}")
            method, _, _ = request_line.split()

            # Read headers until an empty line is found
            while True:
                line = self.rfile.readline().decode('utf-8').strip()
                if not line:
                    break

            if method == "OPTIONS":
                self.send_options_response()
            elif method == "REQMOD":
                print("Received REQMOD request. Checking service health and preparing response...")
                time.sleep(1)  # Reduced sleep time
                print("Responding with 204 No Content and X-Next-Services routing.")
                self.send_reqmod_no_content_response()
            elif method == "RESPMOD":
                print("Received RESPMOD request. Checking service health and preparing response...")
                time.sleep(1)  # Reduced sleep time
                print("Responding with 204 No Content and X-Next-Services routing.")
                self.send_respmod_no_content_response()
            else:
                print(f"Unsupported method: {method}")
                self.send_error_response(501, "Not Implemented")

        except Exception as e:
            print(f"Error handling request from {client_address}: {e}")
        finally:
            print(f"Closing connection from {client_address}")

    def get_date_header(self):
        """Returns the current date in the format required for HTTP headers."""
        return time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())

    def send_options_response(self):
        """Sends a 200 OK response for OPTIONS requests."""
        response = (
            "ICAP/1.0 200 OK\r\n"
            f"Date: {self.get_date_header()}\r\n"
            "Methods: REQMOD, RESPMOD\r\n"
            "Service: Python Mock ICAP Server 1.0\r\n"
            "ISTag: \"py-mock-icap-12345\"\r\n"
            "Encapsulated: null-body=0\r\n"
            "Server: Python-Mock-ICAP/1.0\r\n"
            "Connection: close\r\n\r\n"
        )
        self.wfile.write(response.encode('utf-8'))
        print("Sent OPTIONS response")

    def send_reqmod_no_content_response(self):
        """Sends a 204 No Content response, indicating no modifications were made."""
        # Get next services for dynamic routing
        next_services = self.get_next_services('reqmod')
        
        response_lines = [
            "ICAP/1.0 204 No Content",
            f"Date: {self.get_date_header()}",
            "ISTag: \"py-mock-icap-12345\"",
            "Server: Python-Mock-ICAP/1.0"
        ]
        
        # Add X-Next-Services header if there are available services
        if next_services:
            next_services_header = f"X-Next-Services: {', '.join(next_services)}"
            response_lines.append(next_services_header)
            print(f"Including X-Next-Services: {', '.join(next_services)}")
        
        response_lines.extend(["Connection: close", ""])
        response = "\r\n".join(response_lines) + "\r\n"
        
        self.wfile.write(response.encode('utf-8'))
        print("Sent REQMOD 204 response")

    def send_respmod_no_content_response(self):
        """Sends a 204 No Content response for RESPMOD, indicating no modifications were made."""
        # Get next services for dynamic routing
        next_services = self.get_next_services('respmod')
        
        response_lines = [
            "ICAP/1.0 204 No Content",
            f"Date: {self.get_date_header()}",
            "ISTag: \"py-mock-icap-12345\"",
            "Server: Python-Mock-ICAP/1.0"
        ]
        
        # Add X-Next-Services header if there are available services
        if next_services:
            next_services_header = f"X-Next-Services: {', '.join(next_services)}"
            response_lines.append(next_services_header)
            print(f"Including X-Next-Services: {', '.join(next_services)}")
        
        response_lines.extend(["Connection: close", ""])
        response = "\r\n".join(response_lines) + "\r\n"
        
        self.wfile.write(response.encode('utf-8'))
        print("Sent RESPMOD 204 response")

    def send_error_response(self, code, message):
        """Sends an error response."""
        response = (
            f"ICAP/1.0 {code} {message}\r\n"
            f"Date: {self.get_date_header()}\r\n"
            "Server: Python-Mock-ICAP/1.0\r\n"
            "Connection: close\r\n\r\n"
        )
        self.wfile.write(response.encode('utf-8'))
        print(f"Sent Error {code} response")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1344
    print(f"Starting mock ICAP server on {HOST}:{PORT}")
    
    server = ThreadedTCPServer((HOST, PORT), ICAPHandler)
    with server:
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        print(f"Server loop running in thread: {server_thread.name}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            server.shutdown()
            server.server_close()
            print("Server shut down.") 