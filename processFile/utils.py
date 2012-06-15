#########
# UTILS #
#########
# MAke the life easyer...

from string import maketrans

# Be careful : no existing file control... 
# Could be easily implemented but no need to have a fat code

#It's for text (and not for bin

def getContent(fname):
	#Read content
	with open(fname, 'r') as f :
		content = f.read()
	return content

def setContent(fname, content):
	with open(fname, 'w') as f :
		f.write(content)


def goodFileName(fname, name = ""):
	s = fname + "-" + name
	trantab = maketrans( "/" , "-")
	return s.translate(trantab)

