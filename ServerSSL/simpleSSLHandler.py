import ssl
import BaseHTTPServer

from WTMH import DropboxRequestHandler

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        """The do_GET will universally handle every request (HEAD, POST, PUT, DELETE)."""
        print("%%%%%Hey, I got a message from "+str(self.client_address))

        #This is where the message from the client is handled, and gives a reply to send back to the client.
        print("%%%%%"+DropboxRequestHandler(self))
##        self.wfile.write(open("httpResponse").read()) #Sample httpResponse
        self.send_error(404,"CONNARDS")
        print("=>Request served !\n")
    
    do_HEAD   = do_GET
    do_POST   = do_GET
    do_PUT    = do_GET
    do_DELETE = do_GET

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
    httpd = BaseHTTPServer.HTTPServer(host, RequestHandler)
    print("Starting the server on "+str(host))
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=certificate, server_side=True)
    httpd.serve_forever()
