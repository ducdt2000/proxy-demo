from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

class MockHTTPHandler(BaseHTTPRequestHandler):
    """
    A simple HTTP handler that logs request details.
    """
    def do_GET(self):
        self.log_request_details()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Mock Server</title></head>")
        self.wfile.write(b"<body><p>Request received successfully.</p></body></html>")

    def do_POST(self):
        self.log_request_details()
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        print("\n--- POST Body ---")
        print(post_data.decode('utf-8'))
        print("-------------------")
        
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><head><title>Mock Server</title></head>")
        self.wfile.write(b"<body><p>POST request received successfully.</p></body></html>")

    def log_request_details(self):
        print("\n--- New Request ---")
        print(f"Time: {self.log_date_time_string()}")
        print(f"Request Line: {self.requestline}")
        print("Headers:")
        for header, value in self.headers.items():
            print(f"  {header}: {value}")
        print("-------------------")
        
    def log_message(self, format, *args):
        # Suppress the default logging to stdout
        return

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 8000
    print(f"Starting mock HTTP server on {HOST}:{PORT}")
    
    server = HTTPServer((HOST, PORT), MockHTTPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        print("Server shut down.") 