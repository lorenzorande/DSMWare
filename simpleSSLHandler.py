"""
Usage : python simpleSSLHandler.py <PEM file> [port number the server will listen]
This is the HTTPS server which will receive the connections from the client, and dispatch them to the DropboxRequestHandler
We need a PEM certificate file that is either signed by an authority in dropbox's trusted_cert.crt, or that is directly in the trusted_cert.crt.
"""
import ssl
import BaseHTTPServer
import urlparse
import threading
from SocketServer import ThreadingMixIn

import sessionHandler.credentialManager 

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """The do_GET will universally handle every request (HEAD, POST, PUT, DELETE)."""
        print("%%%%% Hello, I am "+threading.currentThread().getName())
        print("%%%%% I got a message from "+str(self.client_address))
        url = urlparse.urlparse(self.path, 'http')
        print("%%%%% The URL is : " + str(url))

        #This is where the message from the client is handled, and gives a reply to send back to the client.
        #print("%%%%% Response : "+DropboxRequestHandler(str(self.headers), self.rfile))

        response = credentialManager.ClientHandler(url,str(self.headers))

	print "object response fetched"

        self.send_HTTPResponse(response)
        print("=>Request served !\n")
    
    do_HEAD   = do_GET
    do_POST   = do_GET
    do_PUT    = do_GET
    do_DELETE = do_GET
    
    def send_HTTPResponse(self, response):
        """This method will convert most of the HTTPResponse response and send it back to the client"""
        self.send_response(response.status, response.reason)
        for header in response.getheaders():
            self.send_header(header[0],header[1])
        self.end_headers()
        self.wfile.write(response.read())
        self.wfile.close()
        

class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """This is an HTTPServer, with threading enabled"""
    pass

if __name__ == "__main__":
    import os
    import sys
    
    if len(sys.argv) < 2 or len(sys.argv) > 3 or not os.path.exists(sys.argv[1]):
        sys.exit('Usage: %s <pem> [port number=4443]' % os.path.basename(__file__))

    if len(sys.argv) == 2:
        host=('localhost', 4443)
    else:
        host=('localhost', int(sys.argv[2]))
    certificate=sys.argv[1]
    httpd = ThreadedHTTPServer(host, RequestHandler)
    print("Starting the server on "+str(host))
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certificate, server_side=True)
    httpd.serve_forever()