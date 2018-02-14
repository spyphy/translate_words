#https://pythonspot.com/nltk-stemming/

from get_transcript import *
import time
import sys

CREATE_DICT = False # create dictionary of 1000 words
MIN_WORD_LEN = 3  # usually =3
MINCOUNT = 10

def check_ascii(word):
	for x in word:
		if ord(x) > 122 or ord(x) < 39 or ord(x) in range(48,65):
			return False	
	return True

def concatenate_files(filenames, out_file):
	with open(out_file, 'w') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					outfile.write(line)

def text_from_file(filename):
	text = ""
	with open(filename) as infile:
		for line in infile:
			text += line
	return text

# delete E with ".."
def del_e(s):
	e = chr(1105) 
	E = chr(1025)
	if e in s: 
		s = s.replace(e, '\\"' + chr(1077))
	if E in s: 
		s = s.replace(E, '\\"' + chr(1045))
	return s

# NLTK

import nltk

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
pStem = PorterStemmer()

from nltk.stem.lancaster import LancasterStemmer
lanStem = LancasterStemmer()

from nltk.stem.snowball import EnglishStemmer
snoStem = EnglishStemmer()

from nltk.stem import WordNetLemmatizer
wnlStem = WordNetLemmatizer()

def stem(w):
	return [wnlStem.lemmatize(w), pStem.stem(w), lanStem.stem(w), snoStem.stem(w)]
 	
wsj = nltk.corpus.treebank.tagged_words(tagset='universal')
word_tag_fd = nltk.FreqDist(wsj)
#verbs = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1]=='VERB'][0:100]

words_adj = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'ADJ'][0:100]
words_adv = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'ADV'][0:100]
words_noun = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'NOUN'][0:800]
words_verb = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'VERB'][0:100]

#words1 = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] in {'ADJ','ADV','NOUN','VERB'}][0:300]
words_prt = [wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] in {'ADP','PRON','CONJ','DET','PRT','.'}]

if False:
	print('\n\n')
	print(words_adj)
	print('\n\n')
	print(words_adv)
	print('\n\n')
	print(words_noun)
	print('\n\n')
	print(words_verb)
	print('\n\n')
	print(words_prt)
	print('\n\n')

common_universal = words_adj + words_adv + words_noun + words_verb + words_prt

#f1 = open('common_universal.utf', 'w')
#for word in common_universal:
#	word = word.strip('"\'.,,:;-!?'+chr(8212))	
#	if not word.islower(): continue
#	f1.write(word + '\n')
#f1.close()


# load list of common words:

def load_list_from_file(filename):
	ls = list()	
	with open(filename) as f:
		for line in f:
			w = line.strip('\n\r').lower()
			ls.append(w)
	return ls

	#inf = open(filename,'r')
	#lines = inf.readlines()
	#for line0 in lines:
	#	w = line0.strip('\n\r').lower()
	#	ls.append(w)
	#	return ls


common_1000 = load_list_from_file('list_1000.txt')
common_exclude = load_list_from_file('list_exclude.txt')
common_names = load_list_from_file('list_names.txt')

print('size common_universal = ' + str(len(common_universal)))
print('size common_1000 = ' + str(len(common_1000)))
print('size common_exclude = ' + str(len(common_exclude)))
print('size common_names = ' + str(len(common_names)))


# load dictionary:


def add_to_dict_from_file(dict_en_ru, infile):
	with open(infile) as f:	
		for line in f.readlines():	
			line = line.rstrip('\n\r')
			if len(line)<2: continue
			line = line.replace('\t', '   ')
			m = line.split(' - ')
			m0 = m[0].strip(' ')
			m1 = m[1].strip(' ')
			if not m0 in dict_en_ru:
				dict_en_ru[m0] = m1

dict_en_ru = dict()

add_to_dict_from_file(dict_en_ru, 'dict_5000.utf')
add_to_dict_from_file(dict_en_ru, 'dict_8000.utf') # bad dict

print('hello world - ' + dict_en_ru['hello'] + ' ' +  dict_en_ru['world'] )


import sys
if False:
	sys.exit()

#from PyDictionary import PyDictionary
#pydict = PyDictionary()

#import goslate
#gs = goslate.Goslate()
from googletrans import Translator
translator = Translator()

processed_words = set()

inf = open('in.utf','r')
outf = open('outf.utf','w')
outf_sc = open('outf_sc.utf','w')
outf_tex = open('outf_tex.utf','w')
#out_txt = open('out.txt','w')
#out_tex = open('out.tex','w')

# add to begin of out files
html_begin = text_from_file('_html_begin.utf')
html_end  = text_from_file('_html_end.utf')
tex_begin = text_from_file('_tex_begin.utf')
tex_end  = text_from_file('_tex_end.utf')

outf.write(html_begin)
outf_sc.write(html_begin)
outf_tex.write(tex_begin)

# LISTS of words
count = 0
list_for_trans = []
prev_list_1 = []  # previous
prev_list_2 = []  # previous
prev_list_3 = []  # previous
prev_list_4 = []  # previous
out_text = ""

common = common_universal + common_exclude + common_names + common_1000 # for exclude
if CREATE_DICT: common = common_1000 + common_exclude

lines = inf.readlines()

print('len(lines) = ' + str(len(lines)))

for i in range(0, len(lines)):	
		
	line0 = lines[i]
	out_text += line0
	arr = line0.strip('\n\r').split()
	
	# filter: delete all Names (words with the first Capital letter, except after point)
	arr_new = []
	for i in range(0, len(arr)):
		if len(arr[i]) <= MIN_WORD_LEN: continue
		if not check_ascii(arr[i]): continue
		if arr[i].isdigit(): continue
		if any(x in arr[i] for x in ["n't", "'ve", "'m", "'re", "'ll" , "'s"]): continue
		
		if i==0 or arr[i].islower() or arr[i-1][len(arr[i-1])-1] == '.': 
			arr_new.append(arr[i])
	
	for w in arr_new: print(w)
	#sys.exit()
	
	for word in arr_new:		
		word = word.strip('"\'.,,:;-!?'+chr(8212)) # 8212 - long dash
		word = word.lower()
		w = word.lower()		# w - all lower
		
		if len(w) <= MIN_WORD_LEN: continue
		if not check_ascii(w): continue
		if w.isdigit(): continue
		if w in list_for_trans: continue
		if w in prev_list_1: continue
		if w in prev_list_2: continue
		if w in prev_list_3: continue
		if w in prev_list_4: continue
		if w in common: continue
	
		test = False
		for x in stem(w):
			if x in common: test = True
			if x in list_for_trans: test = True
			if x in prev_list_1: test = True
			if x in prev_list_2: test = True
			if x in prev_list_3: test = True
			if x in prev_list_4: test = True
		
		if test:
			continue
	
		#print('word {0} has been added to list'.format(word))
		list_for_trans.append(word)   # add to list
	
	
	if len(list_for_trans) >= MINCOUNT or i==len(lines)-1:   # write WORDS out
		
		print('write WORDS out')
		
		outf_tex.write("\\begin{spacing}{1.0} { \\large \n\n ")  # to TEX size of font
		
		for word in list_for_trans:						
			
			lower_word = word.lower()
			inword = word
			
			flag = False
			
			if word in dict_en_ru:  # CAPITAL
				translated_word = dict_en_ru[word].lower() # to lower								
				flag = True
				print('- translated from dict_en_ru: '  + word + ' - ' + translated_word)
				inword = word

			else:
				stems = stem(lower_word)
				for x in stems:
					if x in dict_en_ru:
						translated_word = dict_en_ru[x]						
						print('- translated from dict_en_ru + stems: ' + word + ' --> ' + x + ' - ' + translated_word)
						inword = x
						flag = True
						break
								
			if not flag: # if flag=False then translate by Google
				try: 
					#translated_word = gs.translate(w, 'ru')   # pydict.translate(w, 'ru')
					translated_word = translator.translate(word, src='en', dest='ru').text
					translated_word = translated_word.strip('.,,:;-!?')
					translated_word = translated_word.lower() # to LOWER
					
					if translated_word == word:  # if can not translated
						flag = False
					else:	
						flag = True
						inword = word
						dict_en_ru[word] = translated_word # add to our dictionary
						print('- translated from Google: ' + word + ' - ' + translated_word)
						time.sleep(1)
						#translated_word = 'test'				
				except:
					translated_word = '-----'
					flag = False
					print('!Exception: Some error with translation. Wain 1 min')
					time.sleep(10)
			
			if flag:  # if was translated	successfully
				
				try: 
					sc = get_transcription(inword)  # transcription
				except:
					sc = ""
					print('error: can not get transcription.')
						
				print("{0} - [{1}] - {2}".format(inword, sc, translated_word))
				outf.write("<b> {0} </b>  -  <i> {1} </i>\n".format(inword, translated_word))

				if sc:
					outf_sc.write("<b> {0} </b>  - <sc> [{1}] </sc> -  <i> {2} </i>\n".format(inword, sc, translated_word)) # for HTML
					outf_tex.write("{\\bf " + inword + " } [" + sc + "] ~ --- \\emph{ " + del_e(translated_word) + " }\n\r")  # for TEX
				else:
					outf_sc.write("<b> {0} </b>  -  <i> {1} </i>\n".format(inword, translated_word))  # for HTML
					outf_tex.write("{\\bf " + inword + " } --- \\emph{ " + del_e(translated_word) + " }\n\r")  # for TEX
					
		if not CREATE_DICT:
			print(out_text)
			outf.write("\n<br>\n\n" + out_text + "\n<br>\n\n")
			outf_sc.write("\n<br>\n\n" + out_text + "\n<br>\n\n")
			outf_tex.write("} \\end{spacing} \\vspace{6mm} \n\n {\\Large \n\n " + out_text  + " \n\n } \\vspace{6mm} \n\n")  # to TEX
		
		prev_list_4 = prev_list_3
		prev_list_3 = prev_list_2
		prev_list_2 = prev_list_1
		prev_list_1 = list_for_trans
		list_for_trans = []
		out_text = ""
		
		#print("{0} : {1}".format(word, pStem.stem(word)))

# add to the end of out files		
outf.write(html_end)
outf_sc.write(html_end)
outf_tex.write(tex_end)		
		
inf.close()
outf.close()
outf_tex.close()
outf_sc.close()