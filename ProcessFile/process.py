######################
## PROCESS FILES    ##
######################

#Import
import crypto
import integrity

from utils import getContent
		
#Global variables


# "Public" function
def putFile(fname):
	'''
	Processing a file before uploading it	
	'''
	#Integritiy
	integrity.addHash(fname)
	#Be Careful : integrity perform before crypto : so getFile must have this two function in reverse order

	#Crypto
	crypto.encryptFile(fname) #add encryption

def getFile(fname):
	'''
	Processing a file after downloading it
	'''
	#Crypto
	crypto.decryptFile(fname) #Remove encryption

	#Integrity
		#See with custommer what he wants... for the moment just print the different results:
	if integrity.checkHash(fname) :
		if integrity.checkIntegrity(fname) :
			print "Integrity OK for : " + fname
		else : print "Integrity PROBLEM, the file " + fname + " has been modified"
	else :
		print "No integrity check for : " + fname
	
#####
#TEST
from  cryptoFile import encrypt_file, decrypt_file
import random

if __name__ == "__main__" :
	key =  "0xCEC5F2F668669FF1FAF2FFBF1FFFDF"
	print "START"
	print getContent("fdlys")
	encrypt_file(key, "fdlys")
	print "----------------------------------"
	print getContent("fdlys")
	print "-----------------------------------------------------"
	decrypt_file(key, "fdlys")
	#getFile("fdlys")
	print getContent("fdlys")












####################################"
