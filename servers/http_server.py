"""
Simple HTTP Server helper for lab environments.
Useful for testing file downloads, web server log analysis, or exfiltration simulation in isolated VMs.
"""

import http.server
import socketserver
import os
from config import Config

class LabHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"[HTTP LAB SERVER LOG] {self.address_string()} - [{self.log_date_time_string()}] {format % args}")

def run_http_server(host: str = None, port: int = None, directory: str = None):
    host = host or Config.LAB_HTTP_HOST
    port = port or Config.LAB_HTTP_PORT
    if directory:
        os.chdir(directory)

    handler = LabHTTPRequestHandler
    with socketserver.TCPServer((host, port), handler) as httpd:
        print(f"==================================================")
        print(f"🔒 LAB HTTP SERVER RUNNING")
        print(f"Host: {host} | Port: {port}")
        print(f"Serving Directory: {os.getcwd()}")
        print(f"Press CTRL+C to stop the server.")
        print(f"==================================================")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Lab HTTP server...")
            httpd.server_close()

if __name__ == "__main__":
    run_http_server()
