# key = "(gak nambah point yaa :v)"
# key1 = "ketemu pesan rahasia nih "
# key2 = [16692,15655,23896,15756,9047,24219,5408,22848,17473,17135,17460,8910,6624,23484,17460,23608,22310,9660,24255,14647,6144,10780,16275,19656,2880]
# flag = ''
# print len(key1)
# 
# for i in range(25):
# 	flag += chr((key2[i])/ord(key1[i]) - ord(key[i]))
# 	
# print flag

# m4th

from z3 import *

v8 = []

for i in range(5):
	for j in range(10):
		v8.append(5*j+i)
print (v8)

s = Solver()
bv = [Int(i) for i in range(50)]
s.add(bv[2] == 102)
s.add(bv[5] == 101)
s.add(bv[12] == 51)
s.add(bv[13] == 104)
s.add(bv[14] == 76)
s.add(bv[17] == 85)
s.add(bv[18] == 105)
s.add(bv[24] == 48)
s.add(bv[27] == 114)
s.add(bv[28] == 49)
s.add(bv[29] == 70)
s.add(bv[31] == 108)
s.add(bv[34] == 112)
s.add(bv[39] == 117)
s.add(bv[41] == 89)
s.add(bv[49] == 78)

val = [873,806,749,800,795]

for i in range(len(val)):
	s.add(bv[40+i] + bv[35+i] + bv[30+i] + bv[25+i] + bv[20+i] + bv[15+i] + bv[10+i] + bv[5+i] + bv[0+i] + bv[45+i] == val[i])

s.add(And(bv[0] == bv[6], bv[6] == bv[32]))
s.add(And(bv[10] == bv[16], bv[16] == bv[42]))
s.add(And(bv[3] == bv[20], bv[20] == bv[26]))
s.add(And(bv[13] == bv[30], bv[30] == bv[36]))
s.add(bv[4]==bv[8])
s.add(bv[8]==bv[19])
s.add(bv[19]==bv[21])
s.add(bv[21]==bv[22])
s.add(bv[22]==bv[23])
s.add(bv[23]==bv[35])
s.add(bv[35]==bv[40])
s.add(bv[40]==bv[45])
s.add(bv[45]==bv[46])
s.add(And(bv[1] == bv[28], bv[28] == bv[33]))
s.add(And(bv[7] == bv[9], bv[9] == bv[11]))
s.add(bv[11] == bv[43])
s.add(And(bv[12] == bv[37], bv[37] == bv[44]))
s.add(bv[5] == bv[25])
s.add(bv[15] == bv[47])
s.add(bv[38] == bv[48])

arr = [6006,4067,7038,7980,9025,5151,4081,2756,8455,5035,6084,4399,2601,10816,7220,7728,2548,6545,11340,9880,5880,4655,10830,7980,4848]
for i in range(len(arr)):
	s.add(bv[i]*bv[49-i] == arr[i])
arr = [3071071080,2075331335,1110954624,3042175500,3456936000,3317413680,4746373632,4893178680,1188400980,4031521650]
for i in range(len(arr)):
	s.add(bv[5*i]*bv[5*i+1]*bv[5*i+2]*bv[5*i+3]*bv[5*i+4] == arr[i])

if str(s.check()) == 'sat':
	model = s.model()
	fff = [0 for i in range(50)]
	for i in range(50):
	    index = eval(str(model[i])[2:])
	    fff[index] = eval(str(model[model[i]]))
	acak2 = (''.join([chr(x) for x in fff]))
	flek = ['' for i in range(50)]
	for i in range(50):
		flek[v8[i]] = acak2[i]
	print(''.join(flek))
else:
	print ('unsat!!!!')
