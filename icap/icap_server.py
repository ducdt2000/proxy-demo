import socketserver
import time
import threading

class ICAPHandler(socketserver.StreamRequestHandler):
    """
    A simple handler for ICAP requests.
    It responds to OPTIONS and REQMOD requests.
    """
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
                print("Received REQMOD request. Sleeping for 2 seconds...")
                time.sleep(2)
                print("Woke up. Responding with 204 No Content.")
                self.send_reqmod_no_content_response()
            elif method == "RESPMOD":
                print("Received RESPMOD request. Sleeping for 2 seconds...")
                time.sleep(2)
                print("Woke up. Responding with 204 No Content.")
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
        response = (
            "ICAP/1.0 204 No Content\r\n"
            f"Date: {self.get_date_header()}\r\n"
            "ISTag: \"py-mock-icap-12345\"\r\n"
            "Server: Python-Mock-ICAP/1.0\r\n"
            "Connection: close\r\n\r\n"
        )
        self.wfile.write(response.encode('utf-8'))
        print("Sent REQMOD 204 response")

    def send_respmod_no_content_response(self):
        """Sends a 204 No Content response for RESPMOD, indicating no modifications were made."""
        response = (
            "ICAP/1.0 204 No Content\r\n"
            f"Date: {self.get_date_header()}\r\n"
            "ISTag: \"py-mock-icap-12345\"\r\n"
            "Server: Python-Mock-ICAP/1.0\r\n"
            "Connection: close\r\n\r\n"
        )
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