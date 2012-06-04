#########
# UTILS #
#########
# MAke the life easyer...

from string import maketrans

# Be careful : no existing file control... 
# Could be easily implemented but no need to have a fat code

def getContent(fname):
	#Read content
	f = open(fname, 'r')
	content = f.read()
	f.close()
	return content

def setContent(fname, content):
	f = open(fname, 'w')
	f.write(content)
	f.close

def goodFileName(fname, name = ""):
	s = fname + "-" + name
	trantab = maketrans( "/" , "-")
	return s.translate(trantab)

