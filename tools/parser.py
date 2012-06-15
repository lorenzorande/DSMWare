"""## PARSER FUNCTION  ##
This file provides various functions to parse the messages from the client.
The patterns are compiled during importation
"""

import re

#Pre-compile patterns
# !!! body(len) => len
p_top_cli = re.compile("\s*method: (?P<method>\S*) ; host: (?P<host>[(]\S*\s*\d+[)]) ; path: (?P<path>\S*) ; proto: (?P<proto>\S*) ; len\(body\): (?P<len>\d+)\s*\n")
p_top_srv =  re.compile("\s*code: (?P<code>[^;]*) ; proto: (?P<proto>\S*) ; len\(body\): (?P<len>\d+)\s*\n")

p_glob = re.compile("\s*(\S*)\s*:\s+(.*)\n")

def parseHttp( string_httprequest):
	'''
	Parse Http request and return a dict with all the values extracted for each field
	Be carefull: 
	!!!  body(len) => len
	'''
	#String request 
	request = string_httprequest

	#Init dict
	d = {} 

	#Top protocol Header parsing
	m_top = p_top_cli.search(request)
	if not m_top : 
		m_top = p_top_srv.search(request)
		#if not m_top : return d #return {} if error
	if m_top :
		d = dict(m_top.groupdict() ,**d)
		request = request[m_top.end(0)+1 :]

	#All fields :	
	d = dict( dict(p_glob.findall(request)), **d)
	#Attention : si body comprend des \n je suis bais

	#Return dict
	return d
		
def parseOauth(httpString) :
	'''
	Parses httpString return a dict with oauth_consumer_key oauth_timestamp oauth_nonce oauth_version as keys which were in the Body
	'''

	parsed = parseHttp(httpString)
	toparse = parsed['Body']
	toparse += '&'
	newparsed=dict(p_oath.findall(toparse))
	return newparsed

def parseToken(request_token) :
	'''
	Parses and extract the token
	'''
	p_oath = re.compile("\s*([^&=]*)=([^&=]*)&")
	request_token += '&'
	newparsed=dict(p_oath.findall(request_token))
	return newparsed

def parseHeaders(httpString):
	'''
	Parses Headers, retrieve all oath parameters from "Authorization" field
	Return Dict
	'''
	p_authorization = re.compile("\s*([^=]*)=([^,]*),")
	parsed = parseHttp(httpString)
	toparse = parsed["Authorization"]
	toparse += ','	
	parsed["Authorization"] = dict(p_authorization.findall(toparse))
	return parsed

def parseQuota(s):
	'''
	Parse quota string and retrieve quota and normal in a dict
	'''
	d = {}
	p_quota  = re.compile("\"quota\":\s*(?P<quota>\d+)")
	p_normal = re.compile("\"normal\":\s*(?P<normal>\d+)")
	m_quota  = p_quota.search(s) 
	m_normal = p_normal.search(s)

	if m_quota and m_normal:
		d = dict(m_quota.groupdict() ,**d)
		d = dict(m_normal.groupdict() ,**d)
		
	else :
		print "Error dans parseQuota"

	return d



if __name__ == "__main__" :
	req1 = " method: POST ; host: ('api.dropbox.com', 443) ; path: /1/oauth/request_token ; proto: HTTP/1.1 ; len(body): 168\n  Content-Length: 168\n  Accept-Encoding: identity\n  User-Agent: OfficialDropboxPythonSDK/1.4\n Host: api.dropbox.com\n  Content-type: application/x-www-form-urlencoded\n  Authorization: OAuth realm=\"\", oauth_nonce=\"28356426\", oauth_timestamp=\"1337941763\", oauth_consumer_key=\"92hbateam2dxxbk\", oauth_signature_method=\"PLAINTEXT\", oauth_version=\"1.0\", oauth_signature=\"7315tog2zjsch4l%26\"\n\nBody : oauth_nonce=28356426&oauth_timestamp=1337941763&oauth_consumer_key=92hbateam2dxxbk&oauth_signature_method=PLAINTEXT&oauth_version=1.0&oauth_signature=7315tog2zjsch4l%26\n"
	req2 = 'code: 200 (OK) ; proto: HTTP/1.1 ; len(body): 1907\n	content-length: 1633\n  cache-control: no-cache\n  Server: nginx/1.0.14\n  Connection: keep-alive\n  pragma: no-cache\n  x-dropbox-metadata: {"revision": 496, "rev": "1f000d55a7d", "thumb_exists": true, "bytes": 12202, "modified": "Wed, 13 Oct 2010 06:14:41 +0000", "client_mtime": "Tue, 07 Sep 2010 15:49:23 +0000", "path": "/Divers/n1407180127_1960.jpg", "is_dir": false, "icon": "page_white_picture", "root": "dropbox", "mime_type": "image/jpeg", "size": "11.9 KB"}\n  Date: Fri, 25 May 2012 10:32:01 GMT\n  Content-Type: image/jpeg\n'


	req3 = "Host: localhost\nAccept-Encoding: identity\nContent-Length: 168\nContent-type: application/x-www-form-urlencoded\nAuthorization: OAuth realm=\"\", oauth_nonce=\"50400732\", oauth_timestamp=\"1339052247\", oauth_consumer_key=\"6y443oxnwt7q32y\", oauth_signature_method=\"PLAINTEXT\", oauth_version=\"1.0\", oauth_signature=\"tgouotgz6h4j7qo%26\"\nUser-Agent: OfficialDropboxPythonSDK/1.4"


	print req3
	print parseHeaders(req3)

#########################################################################
#Archives (first version with a complete parsing)
'''
p_content = re.compile("\s*Content-Length: (?P<Content_Length>.*)\n")
p_encoding = re.compile("\s*Accept-Encoding: (?P<Accept_Encoding>.*)\n")
p_ua = re.compile("\s*User-Agent: (?P<User_Agent>.*)\n")
p_host = re.compile("\s*Host: (?P<Host>.*)\n")
p_type = re.compile("\s*Content-type: (?P<Content_type>.*)\n")
p_auth = re.compile("\s*Authorization: OAuth (.*)\n")
p_oath = re.compile('(\w+)[=] ?"(\S+)"?')
#p_body = re.compile('\s*Body\s*:\s*(.*)')
'''
##########################################################################
