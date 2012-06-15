DSMWare
=======

***Eurecom 2012's DSMWare Project (Dropbox proxy)***

The goal of this project is to establish a transparent proxy on top of the official Dropbox client (except for the certificates), that will convert the req'uest and offer additional functionalities. We also have a slightly modified client to allow for easier testing.

**Usage** : $ python ./mainServer.py cert.pem [port number]

____cert.pem : PEM certificate that will be used for SSL communications with the client. (Note : The certificate key has to be added to the trusted-cert.crt in the Dropbox API. The file "mycert.pem" will work with the python egg and client provided.
  
____port number : Defaults to 4443. If you would rather use 443, you will need to launch the script with administrator privileges and change the values in the Dropbox API's egg "session.py" or "rest.py" (you can also change the host there).
  
**Test procedure** : Launch the server. Then start the client/cli_client.py, and issue a command. You will see the debug information on the server, and, depending on the command, sometimes on the client.



**Structure** 

  -Server file, configuration files, certificates

  -Modified client API for ease of installation
  
  *client : Python CLI client for dropbox, for ease of testing.
  
  *dropbox : Dropbox API's files, for reference
  
  *dropbox_proxy : Modified API, with additional informations for the server
  
  *sessionHandler : contains the classes and method that will handle the clients and interacts with the original Dropbox server
  
  *processFile : House to the functions that will operate on the files that are exchanged during the session, including hash algorithm and DES encryption.
  
  *tools : various files that are now obsolete or not needed at this point.