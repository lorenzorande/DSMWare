#######################
## CRypto Functions  ##
#######################

import cryptoAES

########
# Parameters

SECRET_KEY = u'h1h1c34ee5f227h891bfccc2e589g62f'

##########
# 2 Top-level functions (pattern-like)
# Allow to change cryptoalgorithm system without changing server code

cypherCode = cryptoAES.AESCypher(SECRET_KEY)

def encrypt(p):
	return cypherCode.encrypt(p)

def decrypt(c):
	return cypherCode.decrypt(c)


#########
#Test
if __name__ == "__main__" :
	p1 = " method: POST ; host: ('api.dropbox.com', 443) ; path: /1/oauth/request_token ; proto: HTTP/1.1 ; len(body): 168\n  Content-Length: 168\n  Accept-Encoding: identity\n  User-Agent: OfficialDropboxPythonSDK/1.4\n Host: api.dropbox.com\n  Content-type: application/x-www-form-urlencoded\n  Authorization: OAuth realm=\"\", oauth_nonce=\"28356426\", oauth_timestamp=\"1337941763\", oauth_consumer_key=\"92hbateam2dxxbk\", oauth_signature_method=\"PLAINTEXT\", oauth_version=\"1.0\", oauth_signature=\"7315tog2zjsch4l%26\"\n\nBody : oauth_nonce=28356426&oauth_timestamp=1337941763&oauth_consumer_key=92hbateam2dxxbk&oauth_signature_method=PLAINTEXT&oauth_version=1.0&oauth_signature=7315tog2zjsch4l%26\n"
	print "\n---PlainText :\n"+p1
	enc1 =  encrypt(p1)
	print "\n---CipherText:\n"+enc1
	print "\n---Deciphered : \n" + decrypt(enc1)

#########################################################################
