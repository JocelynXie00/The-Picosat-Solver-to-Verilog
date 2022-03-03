import os
import time
t = time.time()
def read(s):
	line = s.split(' ')
	return line

def readgate(s):
	p1 = s.split('(')
	p2 = p1[1].split(')')
	p = p2[0].split(',')
	return p

def reads(s):
	s = s.split(';')
	s = s[0].split(',')
	return s



from sys import argv

if len(argv) != 4:
	print("usage python solver.py xxx.v #(steps) #(target state)")
	exit(-1)


vfile = argv[1]
k = int(argv[2])
d = {}
index = 1
cnf = []#cnf formula
link = []#link Si to NSi
initial = []
with open(vfile,'r') as f:

	while line := f.readline():
		line = read(line)
		#print(line)
		
		if len(line) == 1:
			if "<=" in line[0]:
				si = line[0].split('<')[0]
				nsi = line[0].split('<')[1]
				nsi = nsi.split('=')[1]
				nsi = nsi.split(';')[0]
				link.append([si, nsi])
			continue
		
		ins = line[0]
		content = line[1]
		
		if ins == 'input':
			for i in reads(content):
				if i != 'clock':
					d[i] = index
					index += 1
		if ins == 'output':
			for i in reads(content):
				if i not in d:
					d[i] = index
					index += 1
		if ins == 'reg':
			for i in reads(content):
				if i not in d:
					d[i] = index
					initial.append(index)
					index += 1
		if ins == 'wire':
			for i in reads(content):
				if i not in d:
					d[i] = index
					index += 1
		
			
		if ins == 'and':
			p = readgate(content)
			if p[0] in d and p[1] in d and p[2] in d:
				x = d[p[0]]
				a = d[p[1]]
				b = d[p[2]]
				cnf.append([a, -x])
				cnf.append([b, -x])
				cnf.append([-a, -b, x])
		if ins == 'not':
			p = readgate(content)
			if p[0] in d and p[1] in d:
				x = d[p[0]]
				a = d[p[1]]
				cnf.append([-a, -x])
				cnf.append([a, x])
		
		

#write into a cnf file


cnfile = vfile[:-2] + ".cnf"
n = len(d)
nums = len(argv[3])
s = "p cnf " + str(n * (k + 1)) + " "+str(nums * 2 + len(cnf) * (k + 1) + len(link) * 2 * k)
with open(cnfile,'w') as f:
	f.write(s)
	f.write('\n')

	#transition cnf formula
	for c in cnf:
		for i in range(k + 1):
			s = ""
			for j in c:
				if j > 0:
					s += str(j + n * i) + " "
				if j < 0:
					s += str(j - n * i) + " "
			s += "0\n"
			f.write(s)
	f.write("\n")
	#initial state + link + target state
	for i in range(len(link)):
		s0 = d[link[i][0]]
		ns0 = d[link[i][1]]
		#initial states
		s = str(-s0) + " 0\n"
		f.write(s)
		#target states
		if argv[3][i] == '0':
			s = str(-(s0 + k * n)) + " 0\n"
		else:
			s = str(s0 + k * n) + " 0\n"
		f.write(s)
		#link
		for j in range(k):
			s = str(-(s0 + (j + 1) * n)) + " " + str(ns0 + j * n) + " 0\n"
			f.write(s)
			s = str(s0 + (j + 1) * n) + " " + str(-(ns0 + j * n)) + " 0\n"
			f.write(s)

			
instruction = "./picosat -n " + cnfile 
os.system(instruction)
t1 = time.time()
print("time: ", t1 - t, " s")























		

