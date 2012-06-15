import tools.parser as parser
import os
import oauth.oauth as oauth

import dropbox_proxy.client_proxy as client_proxy, dropbox_proxy.rest_proxy as rest_proxy, dropbox_proxy.session_proxy as session_proxy

import processFile.process as process

backup_key = 'jebz0u950mwt6xr'
backup_secret = 'nyj544pf4b1bnhc'
backup_token = '96uys2q599w0e6r|f5iexbbbadz2cbi'



def ClientHandler(url,clientHttpHeader, readFile) :
	"""handler handling requests from a client"""
	
	path = str(url[2])

	"""identifying the client"""
	oauthParsed =parser.parseHeaders(clientHttpHeader)

	consumer_key = oauthParsed['Authorization']['oauth_consumer_key'][1:-1]
	info=ClientConsumerInfo(consumer_key,"id.conf")
	consumer_secret=info.split()[1]

	"""creating the db objects for the backup"""
	backup_sess = session_proxy.DropboxSession(backup_key, backup_secret, 'app_folder', locale=None)
	backup_sess.set_token(*backup_token.split('|'))

	"""creating a DropboxSession object for the client"""
	sess = session_proxy.DropboxSession(consumer_key, consumer_secret, 'app_folder', locale=None)
	"""load token if already exists"""
	stored_creds=info.split()[2]
	if stored_creds != "" :
		sess.set_token(*stored_creds.split('|'))



	if path.split("/")[2] == "oauth" :
		"""it is an login"""

		if path.split("/")[3] == "request_token" :
			"""step 1 of authentication"""

			response = sess.obtain_request_token_proxy()
			#repread=response.read()
			#request_token = oauth.OAuthToken.from_string(repread)

			"""storing the requested token in a file"""
			#write_creds(consumer_key, request_token, "tokentemp.conf")

			# renvoyer le message a envoyer au client
			return response

		
		if path.split("/")[3] == "access_token" : 
			"""step 2 of authentication"""

			print "step 2"
			#info=ClientConsumerInfo(consumer_key,"tokentemp.conf")
			#request_token_str="oauth_token_secret="+info.split()[2].split("|")[1]+"&oauth_token="+info.split()[2].split("|")[0]
			#request_token=oauth.OAuthToken.from_string(request_token_str)
			#new_request_token=sess.obtain_access_token_proxy(oauthParsed['oauth_timestamp'], oauthParsed['oauth_nonce'], oauthParsed['oauth_version'],request_token)

			"""storing the requested token in a file"""
			#write_creds(consumer_key, request_token, "id.conf")
		


	if path.split("/")[2] == "account" :
		"""client requested account_info""" 

		dbclient=client_proxy.DropboxClient(sess)
		url, params, headers = dbclient.request("/account/info", method='GET')
		response=rest_proxy.RESTClient.GET(url, headers,raw_response=True)

		return response



	if path.split("/")[2] == "files_put" :
		"""the client has done a put_file"""
		
		body_length=oauthParsed["Content-Length"]

		"""we first store the file"""
		"""we need to know where"""
		temp_path=str(consumer_key)+"/"+path[13:]
		to_path=path[13:]

		"""creating folder if it does not exist"""
		try :
			os.makedirs(os.path.split(temp_path)[0])

		except OSError:
			pass

		"""write readFile in a file"""
		with open(temp_path,"wb") as f :
			line = readFile.read(int(body_length))
			f.write(line)
		f.close()


		"""encryption of the file"""
		process.putFile(temp_path) 
		

		"""sending the encrypted file to dropbox"""
		with open(temp_path, "rb") as from_file :
			dbclient=client_proxy.DropboxClient(sess)
			response=dbclient.put_file(to_path,from_file)

		with open(temp_path, "rb") as from_file :
			"""send to the backup dropbox account"""
			backup_to_path='sandbox/'+temp_path

			backup_dbclient=client_proxy.DropboxClient(backup_sess)
			backup_dbclient.put_file(backup_to_path,from_file)

		"""destroying the temp file"""
		try :
			os.remove(temp_path)

		except OSError:
			pass

		return response


	if path.split("/")[2] == "files" :
		"""the client has done a get_file"""

		"""first get the file from dropbox"""
		from_path=path[9:]

		dbclient=client_proxy.DropboxClient(sess)
		dbresponse=dbclient.get_file(from_path)
		
		"""write the file locally"""
		local_path=str(consumer_key)+"/"+from_path

		try :
			os.makedirs(os.path.split(local_path)[0])
		except OSError:
			pass

		with open(local_path,"wb") as f :
			f.write(dbresponse.read())

		"""then check integrity and unencrytion"""
		process.getFile(local_path)

		"""finally send it to the client"""




def ClientConsumerInfo(consumer_key,idconfigfile) :
	"""function which finds consumer_secret in the conf file"""

	with open(idconfigfile,"r") as f :
		line = f.readline()
			
		while line != "" and line.split()[0] != consumer_key:
			line = f.readline()
			
		if line == "" :
			"""if consumer_key is not in the file, return a default consumer_secret""" 
			return 000000000000000

		else :
			return line


def write_creds(consumer_key, token, TOKEN_FILE):
	with open(TOKEN_FILE, 'r') as f :
		with open("temp", 'w') as g :
			line = f.readline()
			while line != "" and line.split()[0] != consumer_key:
				g.write(line)
				line = f.readline()

			if line.split()[0] == consumer_key:
				g.write(line.split()[0]+" "+line.split()[1]+" "+"|".join([token.key, token.secret]))

			line = f.readline()
			while line != "" :
				g.write(line)
				line = f.readline()
			os.rename("temp",TOKEN_FILE)




if __name__ == "__main__" :
	"""samples de requetes pour les tests"""
	req1 = " method: POST ; host: ('api.dropbox.com', 443) ; path: /1/oauth/request_token ; proto: HTTP/1.1 ; len(body): 168\n  Content-Length: 168\n  Accept-Encoding: identity\n  User-Agent: OfficialDropboxPythonSDK/1.4\n Host: api.dropbox.com\n  Content-type: application/x-www-form-urlencoded\n  Authorization: OAuth realm=\"\", oauth_nonce=\"28356426\", oauth_timestamp=\"1337941763\", oauth_consumer_key=\"6y443oxnwt7q32y\", oauth_signature_method=\"PLAINTEXT\", oauth_version=\"1.0\", oauth_signature=\"7315tog2zjsch4l%26\"\n\nBody : oauth_nonce=28356426&oauth_timestamp=1337941763&oauth_consumer_key=6y443oxnwt7q32y&oauth_signature_method=PLAINTEXT&oauth_version=1.0&oauth_signature=7315tog2zjsch4l%26\n"
	

	req2 = " method: POST ; host: ('api.dropbox.com', 443) ; path: /1/oauth/access_token ; proto: HTTP/1.1 ; len(body): 168\n  Content-Length: 168\n  Accept-Encoding: identity\n  User-Agent: OfficialDropboxPythonSDK/1.4\n Host: api.dropbox.com\n  Content-type: application/x-www-form-urlencoded\n  Authorization: OAuth realm=\"\", oauth_nonce=\"28356426\", oauth_timestamp=\"1337941763\", oauth_consumer_key=\"6y443oxnwt7q32y\", oauth_signature_method=\"PLAINTEXT\", oauth_version=\"1.0\", oauth_signature=\"7315tog2zjsch4l%26\"\n\nBody : oauth_nonce=28356426&oauth_timestamp=1337941763&oauth_consumer_key=6y443oxnwt7q32y&oauth_signature_method=PLAINTEXT&oauth_version=1.0&oauth_signature=7315tog2zjsch4l%26\n"
	

	#ClientHandler(req2)
	#ParseToken("oauth_token_secret=8uqp21zswnsdpc6&oauth_token=5h3btpags2znxgm")
	
