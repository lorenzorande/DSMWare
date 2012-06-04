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
from  utils import setContent, getContent

### Initialisation


### Preferences
CRYPTO_PATH = "./crypto_file" #here path of the crypto stockage file

### Global variables
#Lock in case...
set_lock = threading.Lock()

# Initialisation
if not os.path.exists(CRYPTO_PATH)
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
    content = getContent(fname)
    m = cryptoAlgo.encrypt(content) #Crypto
    setContent(fname, m) #replace
    set_lock.acquire()
    CRYPTO_SET.add(fname) #not computed here pour avoid long blocking time 
    saveCrypto() #lock avoid in same time concurrent access in the save file
    set_lock.release()

def decryptFile(fname):
    '''
    Replace content of the file by plaintext
    '''
    content = utils.getContent(fname)
    m = cryptoAlgo.decrypt(content) 
    setContent(fname, m)


###  "Private" Functions

def saveCrypto():
    '''
    Save the CRYPTO_SET
    Build to avoid crashes
    '''
    f = open(CRYPTO_PATH, 'w')
    pickle.dump(CRYPTO_SET, f)
    f.close()

######
#TEST#

if __name__ == "__main__"
    s = "vcgbanevbmioncaxnc fyivzbcoapivenzpc*nvteo:lnc478/e5t1bv684186\n\r\tbvznvcbzzbcbebbce   ezc zrvcze cz e8861841811014018+++5-==-"
    print computeCrypto(s)
    

###########################"
