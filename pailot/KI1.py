cipher = '''lrvmnir bpr sumvbwvr jx bpr lmiwv yjeryrkbi jx qmbm wi
bpr xjvni mkd ymibrut jx irhx wi bpr riirkvr jx
ymbinlmtmipw utn qmumbr dj w ipmhh but bj rhnvwdmbr bpr
yjeryrkbi jx bpr qmbm mvvjudwko bj yt wkbrusurbmbwjk
lmird jk xjubt trmui jx ibndt
wb wi kjb mk rmit bmiq bj rashmwk rmvp yjeryrkb mkd wbi
iwokwxwvmkvr mkd ijyr ynib urymwk nkrashmwkrd bj ower m
vjyshrbr rashmkmbwjk jkr cjnhd pmer bj lr fnmhwxwrd mkd
wkiswurd bj invp mk rabrkb bpmb pr vjnhd urmvp bpr ibmbr
jx rkhwopbrkrd ywkd vmsmlhr jx urvjokwgwko ijnkdhrii
ijnkd mkd ipmsrhrii ipmsr w dj kjb drry ytirhx bpr xwkmh
mnbpjuwbt lnb yt rasruwrkvr cwbp qmbm pmi hrxb kj djnlb
bpmb bpr xjhhjcwko wi bpr sujsru msshwvmbwjk mkd
wkbrusurbmbwjk w jxxru yt bprjuwri wk bpr pjsr bpmb bpr
riirkvr jx jqwkmcmk qmumbr cwhh urymwk wkbmvb'''

import string
d = {}
for x in string.ascii_lowercase:
	d[x] = 0
for c in cipher:
	if c not in string.ascii_lowercase:
		continue
	d[c] += 1

freq = ['E','T','A','O','I','N','S','R','H','D','L','U','C','M','F','Y','W','G','P','B','V','K','X','Q','J','Z']
freq.reverse()
freq = ''.join(freq)
freq = freq.lower()

sorted_dict = sorted(d.iteritems(), key=lambda x: int(x[1]))
print freq
peta = {}
peta_r = {}
for i,x in enumerate(sorted_dict):
	d[x[0]] = i
	peta[x[0]] = freq[d[x[0]]]
	peta_r[freq[d[x[0]]]] = x[0]

def swap(a,b):
	temp = peta[a]
	peta[a] = b
	peta[peta_r[b]] = temp

	temp2 = peta_r[b]
	peta_r[b] = a
	peta_r[temp] = temp2

swap('p','h')
swap('s','p')
swap('w','i')
swap('j','o')
swap('x','f')
swap('q','k')
swap('d','d')
swap('c','w')
swap('g','z')
swap('l','b')
swap('v','c')
swap('n','u')
for x in string.ascii_lowercase:
	print x,'=', peta[x]

res = ''
print cipher
print
for c in cipher:
	if c not in string.ascii_lowercase:
		res+=c
		continue
	res += peta[c]
print res
