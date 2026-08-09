"""
Simple FTP Server helper for lab environments using pyftpdlib (with fallback to socket server).
"""

import os
from config import Config

def run_ftp_server(host: str = None, port: int = None, user: str = None, password: str = None):
    host = host or Config.LAB_FTP_HOST
    port = port or Config.LAB_FTP_PORT
    user = user or Config.LAB_FTP_USER
    password = password or Config.LAB_FTP_PASS

    try:
        from pyftpdlib.authorizers import DummyAuthorizer
        from pyftpdlib.handlers import FTPHandler
        from pyftpdlib.servers import FTPServer

        authorizer = DummyAuthorizer()
        authorizer.add_user(user, password, homedir=os.getcwd(), perm="elradfmwMT")
        authorizer.add_anonymous(os.getcwd(), perm="elr")

        handler = FTPHandler
        handler.authorizer = authorizer

        address = (host, port)
        server = FTPServer(address, handler)

        print(f"==================================================")
        print(f"🔒 LAB FTP SERVER RUNNING")
        print(f"Host: {host} | Port: {port}")
        print(f"User: {user} | Pass: {password}")
        print(f"Directory: {os.getcwd()}")
        print(f"Press CTRL+C to stop the server.")
        print(f"==================================================")
        server.serve_forever()

    except ImportError:
        print("[WARNING] pyftpdlib package not found. Install via 'pip install pyftpdlib' to run FTP server.")
    except KeyboardInterrupt:
        print("\nShutting down Lab FTP server...")

if __name__ == "__main__":
    run_ftp_server()
