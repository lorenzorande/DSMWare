import os, random, struct
from Crypto.Cipher import AES

'''
 Folowing code based on :
http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
 We've made personnal improvement 
 Our previous version of AES_cypher_file (which was very personnal) had problems to handle specific characters, we had to change for a binary AES to avoid this type of pb
'''

def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.

    """
    if not out_filename:
        out_filename = in_filename + ".enc"
    #Create a specific Initialisation Vector for each file : the cypher is much more robust
    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    cypher = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            #Write original length and IV for decyphering
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)
                outfile.write(cypher.encrypt(chunk))
    #Manage files
    os.rename(out_filename, in_filename)

def decrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        #Retrieve original length and IV
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        cypher = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(cypher.decrypt(chunk))

            outfile.truncate(origsize)
    #Manage files
    os.rename(out_filename, in_filename)

###############################################################
