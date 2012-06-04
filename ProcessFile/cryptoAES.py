
#######
# AES #
#######
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

class AESCypher:
	def __init__ (self, secret_key):
		# Secret KEY (Length 16, 24, or 32)
		self.SECRET_KEY = secret_key
		# Initialization Vector (IV)
		self.IV = u'g94g56chb531e82f'

		# Cipher objects
		self.CIPHER = AES.new(self.SECRET_KEY, AES.MODE_CBC, self.IV)

		## AES parameters
		self.BLOCK_SIZE = 32 # Must be 16, 24 or 32
		# Fit the BLOCK_SIZE ? => Interrupt & Pad 
		self.INTERRUPT = u'\u0001'
		self.PAD = u'\u0000'

	#Refresh : to have same cypher code
	def refresh(self):
		self.CIPHER = AES.new(self.SECRET_KEY, AES.MODE_CBC, self.IV)

	
	#Encryptfunctions

	def encrypt(self, plaintext_data):
		self.refresh()
		plaintext_padded = self.AddPadding(plaintext_data, self.INTERRUPT, self.PAD, self.BLOCK_SIZE)
		encrypted = self.CIPHER.encrypt(plaintext_padded)
		return b64encode(encrypted)
		#return encrypted

	def decrypt(self, encrypted_data):
		self.refresh()
		decoded_encrypted_data = b64decode(encrypted_data)
		#decoded_encrypted_data = encrypted_data
		decrypted_data = self.CIPHER.decrypt(decoded_encrypted_data)
		return self.StripPadding(decrypted_data, self.INTERRUPT, self.PAD)

	#Padding functions
	def AddPadding(self, data, interrupt, pad, block_size):
		new_data = data + interrupt
		new_data_len = len(new_data)
		remaining_len = block_size - new_data_len
		to_pad_len = remaining_len % block_size
		pad_string = pad * to_pad_len
		return new_data + pad_string

	def StripPadding(self, data, interrupt, pad):
		return data.rstrip(pad).rstrip(interrupt)

#end - AES
##########

