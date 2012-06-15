#!/bin/python
"""This is an attempt to recreate a server with the same interface as mainServer.py, but without using HTTPBaseServer."""
from __future__ import print_function

import socket
import ssl
import time

class Client():
    """This class will handle a socket and interpret its content"""
    
    def __init__(self, sock):
            self.sock = sock
            data = self.sock.recv(200)
            print("%%%My client is " + str(self.sock.getpeername()) + ".")
            self.sock.setblocking(False)
            print(data,end='')
            while True: 
                try:
                    dataTmp = self.sock.recv(10)
                    data += dataTmp
                    print(dataTmp, end='')
                except socket.error, e:
                    if e.errno != 11:
                        raise(e)
                    else:
                        break
            print("%%%My client said : " + data)


            #TODO : traitement des donnees, parsage
            self.sock.close()


class Server():
    """This class will run the binded socket and create Client objects to handle the requests"""
    
    clientList = [] #May be used to make sure that there are no more active sockets on shutdown

    def __init__(self, cert_file, port = 4443):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock = ssl.wrap_socket(self.sock, certfile = cert_file, server_side = True)
        self.sock.bind( ("localhost",port) )
        self.sock.listen(5)
        print("%%%Server is setup on port " + str(port) + "." )

    def serve_forever(self):
        try:
            while True:
                self.clientList.append(Client(self.sock.accept()[0]))
        except KeyboardInterrupt:
            server.sock.close()
            print("\nKILL received, quitting gracefuly. Send another KILL to forcequit.")
            for client in server.clientList: #Make sure that we don't leave any client hanging.
                try: client.sock.close()
                except Exception, e: continue
            exit()


if __name__ == '__main__':
    import sys

    try:
        cert_file = sys.argv[1]
        port = int(sys.argv[2])
    except Exception, e:
        print(e)
        print("Usage : %s cert_file.pem port"%(sys.argv[0]))
        exit()

    try:
        server = Server(cert_file, port)
    except Exception, e:
        print(e)
        print("The selected port is already in use.")
        exit()
    server.serve_forever()

