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

import sessionHandler.credentialManager as credentialManager

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    server_version='nginx/1.0.14'#We want to simulate the dropbox server as well as possible
    protocol_version='HTTP/1.1'

    def do_GET(self):
        """The do_GET will universally handle every request (HEAD, POST, PUT, DELETE)."""
        
        print("%%%%% Hello, I am " + threading.currentThread().getName())
        print("%%%%% I got a message from " + str(self.client_address))
        url = urlparse.urlparse(self.path, 'http')
        print("%%%%% The URL is : " + str(url))

        response = credentialManager.ClientHandler(url,str(self.headers),self.rfile)
        print "object response fetched"
        self.send_HTTPResponse(response)
        print("=>Request served !\n")
    
    do_HEAD   = do_GET
    do_POST   = do_GET
    do_PUT    = do_GET
    do_DELETE = do_GET
    
    def send_HTTPResponse(self, response):
        """This method convert most of the HTTPResponse to strings and send them to the client"""
        #TODO:Find a way to make send the content back to the client
        bufferedBody=response.read()
        print("<-------Status, reason : " + str(response.status) + "," + str(response.reason))
        print("<-------Headers : "+str(response.getheaders()))
        print("<-------Body size : "+str(len(bufferedBody)))
        print("<-------Body : "+str(bufferedBody))
        self.send_response(response.status, response.reason)
        for header in response.getheaders():
            self.send_header(header[0],header[1])
        self.end_headers()
        if bufferedBody != '':
            self.wfile.write(str(len(bufferedBody))+"\r\n")#Send the size of the chunk
            self.wfile.write(bufferedBody.strip()+"\r\n")#Send the body of the chunk
        else:
            self.wfile.write("\r\n")#Write an empty line if there is no body
        self.wfile.write("0\r\n\r\n")#Write a chunk of size 0, ending the transmission (supposedly, but the client is left hanging).
        self.wfile.flush()
        self.wfile.close()
        

class ThreadedHTTPServer(ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """This is an HTTPServer, with threading enabled"""
    pass

if __name__ == "__main__":
    import os
    import sys
    
    try:
        certificate=sys.argv[1]
        if len(sys.argv) == 2:
            host=('localhost', 4443)
        else:
            host=('localhost', int(sys.argv[2]))
    except Exception, e:
        print(e)
        sys.exit('Usage: %s <pem> [port number]' % os.path.basename(__file__))


    httpd = ThreadedHTTPServer(host, RequestHandler)
    print("Starting the server on "+str(host))
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certificate, server_side=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nThe server has shut down.")
        exit() 



