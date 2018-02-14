inf = open('in.utf', 'r')	
outf = open('out1.utf', 'w')
lines = inf.readlines()
for line0 in lines:
	s = line0.rstrip('\n\r') + '#'
	outf.write(s)
	print(s)
	print('\n')
outf.close()
inf.close()

inf = open('out1.utf', 'r')	
outf = open('out2.utf', 'w')	
lines = inf.readlines()
for line in lines:
	line = line.replace('##','\n\n')
	line = line.replace('#',' ')	
	outf.write(line)
inf.close()
outf.close()
