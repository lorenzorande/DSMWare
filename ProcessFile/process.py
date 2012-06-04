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

if __name__ == "__main__" :
	fname = "toto"
	putFile(fname)
	print 'ENCYPHERED : ' +  getContent(fname)
	getFile(fname)
	print 'DECYPHERED : ' +  getContent(fname)
	









####################################"
