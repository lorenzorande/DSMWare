DSMWare
=======

Eurecom 2012's DSMWare Project (Dropbox proxy)

The goal of this project is to establish a transparent proxy on top of the official Dropbox client (except for the certificates), that will convert the request and offer additional functionalities.

Structure : 

  -Server file, configuration files, certificates

  -Modified client API for ease of installation
  
  *client : Python CLI client for dropbox, for ease of testing.
  
  *dropbox : Dropbox API's files, for reference
  
  *dropbox_proxy : Modified API, with additional informations for the server
  
  *sessionHandler : contains the classes and method that will handle the clients and interacts with the original Dropbox server
  
  *processFile : House to the functions that will operate on the files that are exchanged during the session, including hash algorithm and DES encryption.
  
  *tools : various files that are now obsolete or not needed at this point.