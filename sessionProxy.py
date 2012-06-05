import tools.parser as parser
import os
import oauth.oauth as oauth

from dropbox import client, rest, session

""" a partir du message d'authentification du client, creer un objet dropboxsession"""



def ClientConsumerInfo(consumer_key,idconfigfile) :
	"""fonction pour trouver consumer_secret dans le fichier de conf"""

	with f=open(idconfigfile,"r")
		line = f.readline()
			
		while line != "" and line.split()[0] != consumer_key:
			line = f.readline()
			
		if line == "" :
			#consumer_key n est pas ds le fichier 
			#consumer_secret sera 000000000000000 par defaut et dropbox enverra un message d erreur
			return 000000000000000

		else :
			return line


def write_creds(consumer_key, token, TOKEN_FILE):
	with f = open(TOKEN_FILE, 'r')
		with g = open("temp", 'w')
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
			#Rename and replace
			os.rename("temp",TOKEN_FILE)
	



def ClientHandler(clientHttpMessage) :
	"""handler gerant les requetes venant du client ou du serveur dropbox"""
	
	# il faut connaitre host et path pour savoir le type de requete
	httpParsed = parser.parseHttp(clientHttpMessage)
	host = httpParsed['host']
	path = httpParsed['path']

	######### a voir si vraiment utile ########
	# gestion de l authentification
	"""UTILE UNIQUEMENT TANT QUE OATH_TOKEN_SECRET N EST PAS CONNU DU PROXY, ie si le client n'a jamais fait login"""
	oathParsed =parser.parseOath(clientHttpMessage)

	consumer_key = oathParsed['oauth_consumer_key'] # on identifie le client
	consumer_secret=ClientConsumerInfo(consumer_key,"id.conf").split()[1]
	sess = session.DropboxSession(consumer_key, consumer_secret, 'app_folder', locale=None)


	if path.split("/")[2] == "oauth" :
	# il s agit d un message d authentification

		if path.split("/")[3] == "request_token" :
		# client en est a etape 1 de l authentification (il a fait login)

			# transmission transparente de la requete a l aide du parsage de clientHttpMessage	
			request_token = sess.obtain_request_token_proxy(oathParsed['oauth_timestamp'], oathParsed['oauth_nonce'], oathParsed['oauth_version'])

			# retransmettre le request_token au client (transmission transparente)
			#TODO

			# stocker request_tocken dans le fichier de conf contenant les non-authorized token
			write_creds(consumer_key, request_token, "tokentemp.conf")
		
		if path.split("/")[3] == "access_token" :
			# client en est a etape 2 de l authentification
			#transmission transparente de la requete a l aide du parsage de clientHttpMessage
			#reconstruire en premier le token pour utiliser l'api (pas sur que ce soit utile)
			info=ClientConsumerInfo(consumer_key,"tokentemp.conf")
			request_token_str="oauth_token_secret="+info.split()[2].split("|")[1]+"&oauth_token="+info.split()[2].split("|")[0]
			request_token=oauth.OAuthToken.from_string(request_token_str)
			new_request_token=sess.obtain_access_token_proxy(oathParsed['oauth_timestamp'], oathParsed['oauth_nonce'], oathParsed['oauth_version'],request_token)

				
				
			#transmission transparente de la reponse a l aide du parsage de clientHttpMessage
			#TODO

			# stocker request_tocken dans le fichier de conf contenant les non-authorized token
			write_creds(consumer_key, request_token, "id.conf")
		

	#fin authentification
	#########################

if __name__ == "__main__" :
	req1 = " method: POST ; host: ('api.dropbox.com', 443) ; path: /1/oauth/request_token ; proto: HTTP/1.1 ; len(body): 168\n  Content-Length: 168\n  Accept-Encoding: identity\n  User-Agent: OfficialDropboxPythonSDK/1.4\n Host: api.dropbox.com\n  Content-type: application/x-www-form-urlencoded\n  Authorization: OAuth realm=\"\", oauth_nonce=\"28356426\", oauth_timestamp=\"1337941763\", oauth_consumer_key=\"6y443oxnwt7q32y\", oauth_signature_method=\"PLAINTEXT\", oauth_version=\"1.0\", oauth_signature=\"7315tog2zjsch4l%26\"\n\nBody : oauth_nonce=28356426&oauth_timestamp=1337941763&oauth_consumer_key=6y443oxnwt7q32y&oauth_signature_method=PLAINTEXT&oauth_version=1.0&oauth_signature=7315tog2zjsch4l%26\n"
	

	req2 = " method: POST ; host: ('api.dropbox.com', 443) ; path: /1/oauth/access_token ; proto: HTTP/1.1 ; len(body): 168\n  Content-Length: 168\n  Accept-Encoding: identity\n  User-Agent: OfficialDropboxPythonSDK/1.4\n Host: api.dropbox.com\n  Content-type: application/x-www-form-urlencoded\n  Authorization: OAuth realm=\"\", oauth_nonce=\"28356426\", oauth_timestamp=\"1337941763\", oauth_consumer_key=\"6y443oxnwt7q32y\", oauth_signature_method=\"PLAINTEXT\", oauth_version=\"1.0\", oauth_signature=\"7315tog2zjsch4l%26\"\n\nBody : oauth_nonce=28356426&oauth_timestamp=1337941763&oauth_consumer_key=6y443oxnwt7q32y&oauth_signature_method=PLAINTEXT&oauth_version=1.0&oauth_signature=7315tog2zjsch4l%26\n"
	

	ClientHandler(req2)
	#ParseToken("oauth_token_secret=8uqp21zswnsdpc6&oauth_token=5h3btpags2znxgm")
	
