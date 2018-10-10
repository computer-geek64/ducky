# Sandbox.py
# Ashish D'Souza
# October 9th, 2018

from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer


authorizer = DummyAuthorizer()
authorizer.add_anonymous(".", perm="elradfmw")
handler = FTPHandler
handler.authorizer = authorizer
address = ("0.0.0.0", 21)
server = servers.FTPServer(address, handler)
server.set_reuse_addr()
server.serve_forever()
server.close()
