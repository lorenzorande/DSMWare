####################
# Crypto (handler) #
####################
'''
Module to manage crypto of files.

'''
#Import section
import os.path
import pickle
import threading #in case...
#module perso
import cryptoAlgo

### Initialisation
SECRET_KEY =  "0xCEC5F2F668669FF1FAF2FFBF1FFFDF" #16 bytes (AES key)


### Preferences
CRYPTO_PATH = "./crypto_file" #here path of the crypto stockage file

### Global variables
#Lock in case...
set_lock = threading.Lock()

###  "Private" Functions

def saveCrypto():
	'''
	Save the CRYPTO_SET
	Build to avoid crashes
	'''
	f = open(CRYPTO_PATH, 'w')
	pickle.dump(CRYPTO_SET, f)
	f.close()

# Initialisation
if not os.path.exists(CRYPTO_PATH):
	CRYPTO_SET = set() #Create dict
	saveCrypto()
else :
	f = open(CRYPTO_PATH, 'r')	
	CRYPTO_SET = pickle.load(f)
	f.close()

### "Public" functions
def checkCrypto(fname):
	'''
	Check if a crypto is known for this file
	'''
	ans = (fname in CRYPTO_SET )
	return ans 	

def encryptFile(fname):
	'''
	Add crypto of the file "fname"
	Replace content of the file by cipher text
	'''
	cryptoAlgo.encrypt_file(SECRET_KEY, fname) #Crypto
	set_lock.acquire()
	CRYPTO_SET.add(fname) #not computed here pour avoid long blocking time 
	saveCrypto() #lock avoid in same time concurrent access in the save file
	set_lock.release()

def decryptFile(fname):
	'''
	Replace content of the file by plaintext
	'''
	cryptoAlgo.decrypt_file(SECRET_KEY, fname) 



######
#TEST#

if __name__ == "__main__":
	s = "vcgbanevbmioncaxnc fyivzbcoapivenzpc*nvteo:lnc478/e5t1bv684186\n\r\tbvznvcbzzbcbebbce   ezc zrvcze cz e8861841811014018+++5-==-"
	

###########################"
