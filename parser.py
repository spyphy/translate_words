# for python3
from lxml.html import parse 

def get_transcription(word):

	url = 'http://dictionary.cambridge.org/dictionary/english/' + word
	print(url)
	par = parse(url)
	page = par.getroot()
	tree = page.cssselect("span.ipa")
	for r in tree:
		print(r.text)
		
	return "-"

print('check transcription: ' + get_transcription("dreamily"))
print('check transcription: ' + get_transcription("hello"))
