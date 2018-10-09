# Sandbox.py
# Ashish D'Souza
# October 9th, 2018

from pyftpdlib import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


authorizer = DummyAuthorizer()
authorizer.add_user("user", "123456", "/home/username, pwerm="elradfmw)
authorizer.add_anonymous("/root", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("192.168.0.199", 1026), handler)
server.serve_forever()
