import BaseHTTPServer
import urlparse

def DropboxRequestHandler(request):
    """This method will read the request, perform various operations, and return a string that will be send back to the client"""
    print("===>The URL is (non parsed then parsed) :")
    url = urlparse.urlparse(request.path, 'http')
    print(url.geturl())
    print(url)
    print("===>Command :")
    print(request.command)
    print("===>Headers :")
    print(request.headers)
    print("===>Dir(request) : ")
    print(dir(request))
    print("===>request.__class__ : ")
    print(request.__class__)
    print("----------------------------------")
    
    return "Everything went fine in the DropboxRequestHandler.\n"

