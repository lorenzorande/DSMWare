######################
## PROCESS FILES    ##
######################

#Import
import crypto
import integrity
        
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
    if integrity.checkHash(fname) :
        if integrity.checkIntegrity(fname) :
            #See with custommer what he wants... for the moment :
            print "Integrity OK for : " + fname
        else : print "Integrity PROBLEM, the file " + fname + " has been modified"
    else :
        #See with custommer what he wants... for the moment :
        print "No integrity check for : " + fname
    
#####
#TEST

if __name__ == "__main__" :
    pass











####################################"
