import BaseHTTPServer
import urlparse

def DropboxRequestHandler(headerString, rfile):
    """This method will read the request, perform various operations, and return a string that will be send back to the client"""
    print("----------------------------------")
    print(headerString)    
    return "Everything went fine in the DropboxRequestHandler.\n"

