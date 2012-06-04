#######################
## CRypto Functions  ##
#######################

# Important : Install PyCrypto
#### apt-get install PyCrypto

from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import os
from datetime import datetime
from re import sub


#######
# AES #
#######
#Based on http://codeghar.wordpress.com/2011/09/01/aes-encryption-with-python/
BLOCK_SIZE = 32 # Must be 16, 24 or 32

# Fit the BLOCK_SIZE ? => Interrupt & Pad 
INTERRUPT = u'\u0001'
PAD = u'\u0000'
def AddPadding(data, interrupt, pad, block_size):
	new_data = ''.join([data, interrupt])
	new_data_len = len(new_data)
	remaining_len = block_size - new_data_len
	to_pad_len = remaining_len % block_size
	pad_string = pad * to_pad_len
	return ''.join([new_data, pad_string])
def StripPadding(data, interrupt, pad):
	return data.rstrip(pad).rstrip(interrupt)

# Secret KEY (Length 16, 24, or 32)
SECRET_KEY = u'h1h1c34ee5f227h891bfccc2e589g62f'
# Initialization Vector (IV)
IV = u'g94g56chb531e82f'

# Cipher objects
cipher_for_encryption = AES.new(SECRET_KEY, AES.MODE_CBC, IV)
cipher_for_decryption = AES.new(SECRET_KEY, AES.MODE_CBC, IV)

def EncryptWithAES(encrypt_cipher, plaintext_data):
	plaintext_data_64 = plaintext_data
	plaintext_padded = AddPadding(plaintext_data_64, INTERRUPT, PAD, BLOCK_SIZE)
	encrypted = encrypt_cipher.encrypt(plaintext_padded)
	return b64encode(encrypted)
def DecryptWithAES(decrypt_cipher, encrypted_data):
	decoded_encrypted_data = b64decode(encrypted_data)
	decrypted_data = decrypt_cipher.decrypt(decoded_encrypted_data)
	return StripPadding(decrypted_data, INTERRUPT, PAD)

##########
# Top-level functions (pattern-like)
# Allow to change cryptoalgorithm system without changing server code

def encrypt(p):
	return EncryptWithAES(cipher_for_encryption ,p)

def decrypt(c):
	return DecryptWithAES(cipher_for_decryption ,c)

#########
#Test
if __name__ == "__main__" :
	p1 = " method: POST ; host: ('api.dropbox.com', 443) ; path: /1/oauth/request_token ; proto: HTTP/1.1 ; len(body): 168\n  Content-Length: 168\n  Accept-Encoding: identity\n  User-Agent: OfficialDropboxPythonSDK/1.4\n Host: api.dropbox.com\n  Content-type: application/x-www-form-urlencoded\n  Authorization: OAuth realm=\"\", oauth_nonce=\"28356426\", oauth_timestamp=\"1337941763\", oauth_consumer_key=\"92hbateam2dxxbk\", oauth_signature_method=\"PLAINTEXT\", oauth_version=\"1.0\", oauth_signature=\"7315tog2zjsch4l%26\"\n\nBody : oauth_nonce=28356426&oauth_timestamp=1337941763&oauth_consumer_key=92hbateam2dxxbk&oauth_signature_method=PLAINTEXT&oauth_version=1.0&oauth_signature=7315tog2zjsch4l%26\n"
	print "\n---PlainText :\n"+p1
	enc1 =  encrypt(p1)
	print "\n---CipherText:\n"+enc1
	print "\n---Deciphered : \n" + decrypt(enc1)

#########################################################################
