# for python3
import urllib.request
 

def get_transcript(s):
	k = s.find('ipa')
	s = s[k+3+2:]
	level = 0
	i = 0
	out = ''
	while level >= 0 and i < len(s):
		x = s[i]
		if x == '>': level -= 1
		elif x == '<': level += 1
		else:
			if level == 0:
				if x=='/': break
				else: out += x	
		i += 1
	#print('out: ' + out)
	out = out.strip(' ')
	return out

 
def get_transcription(word):

	fp = urllib.request.urlopen('http://dictionary.cambridge.org/dictionary/english/' + word)
	mybytes = fp.read()
	html = mybytes.decode("utf8")
	fp.close()
	
	pronun = 'uk'
	if pronun == 'uk': findstr = 'listen to British English pronunciation'
	elif pronun == 'us': findstr = 'listen to American pronunciation'

	k = html.find(findstr)
	if k==-1: return ""

	str1 = html[k+len(findstr) : k+len(findstr)+600] # >=500, <=700 
	#print(str1)
	transcription = get_transcript(str1)

	return transcription

print('check transcription dreamily: ' + get_transcription("dreamily"))
print('check transcription world: ' + get_transcription("world"))
print('check transcription rattle: ' + get_transcription("rattle"))
