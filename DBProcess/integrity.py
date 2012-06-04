#############
# Integrity #
#############
'''
Module to check the integrity of files

Based on a hash of all the "body" of the file

Pattern-like, but be carefull to not change the hash function without re-compute all the hashes : it would lead to problems, because no more hashes will match

The files are currently saved to avoid to lose the hash table if the prog crashes. It will consumme resources, but it's safer.
'''

#Import section
import os.path
import pickle
import hashlib
import threading #in case...

from utils import getContent

### Initialisation


### Preferences
HASH_PATH = "./hash_file" #here path of the hash stockage file

### Global variables
#Lock in case...
dict_lock = threading.Lock()

# Initialisation
if not os.path.exists(HASH_PATH)
    HASH_DICT = {} #Create dict
    saveHash()
else :
    f = open(HASH_PATH, 'r')    
    HASH_DICT = pickle.load(f)
    f.close()

### "Public" functions
def checkHash(fname):
    '''
    Check if a hash is known for this file
    '''
    ans = (fname in HASH_DICT.keys() )
    return ans  


def checkIntegrity(fname):
    '''
    Check if the hash of the file match with the previous saved one
    '''
    if not checkHash(fname) : 
        return false
    else :
        return computeHash(fname) == HASH_DICT[fname]

def addHash(fname):
    '''
    Add hash of the file "fname", if it exists already it will be replaced
    '''
    newHash = computeHash(fname)
    dict_lock.acquire()
    HASH_DICT[fname] = newHash #not computed here pour avoid long blocking time 
    saveHash() #lock avoid in same time concurrent access in the save file
    dict_lock.release()


###  "Private" Functions

def computeHash(fname):
    '''
    Pattern-like
    '''
    content = getContent(fname)
    #Hash
    hf = hashlib.md5() #Possibility to change hash function
    hf.update(content)
    h = hf.digest()
    return h

def saveHash():
    '''
    Save the HASH_DICT
    Build to avoid crashes
    '''
    f = open(HASH_PATH, 'w')
    pickle.dump(HASH_DICT, f)
    f.close()

######
#TEST#

if __name__ == "__main__"
    s = "vcgbanevbmioncaxnc fyivzbcoapivenzpc*nvteo:lnc478/e5t1bv684186\n\r\tbvznvcbzzbcbebbce   ezc zrvcze cz e8861841811014018+++5-==-"
    print computeHash(s)
    

###########################"
