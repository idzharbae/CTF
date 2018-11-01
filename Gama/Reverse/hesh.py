from z3.z3 import *
from pwn import *

# HATI-HATI MENGIRIM WHITESPACE!!1!1


#p = process('./hasssh')
p = remote('asgama.web.id' ,40500)
# p = process('./test')
print p.recvuntil('!\n')
xxx = 0
while True:
	s = Solver()
	try:
		
		rec = p.recvline()
		if len(rec) > 5:
			print rec
			print p.recv()
			print p.recv()
			print p.recv()
			print p.recv()
		#print 'got', repr(rec)
		angka = int(rec.strip())
		if angka == 0:
			p.sendline('ngasal')
			continue
		xxx += 1
		#print xxx, angka
		for LEN in range(2,33):
			s.reset()
			bv = [Int(i) for i in range(LEN)]
			for i in range(LEN):
				s.add(bv[i] != ord(' '))
				s.add(bv[i] != ord('\n'))
				s.add(bv[i] != ord('\t'))
				s.add(bv[i] != ord('\r'))
				s.add(bv[i] != ord('\v'))
				s.add(bv[i] != ord('\f'))
				s.add(Or(And(bv[i] > 0, bv[i] < 8), And(bv[i] > 31, bv[i] < 127)))
			s.add( ( Sum([bv[i] for i in range(LEN-1)]) * bv[LEN-1])  == angka)
			if str(s.check()) == 'sat':
				model = s.model()
				fff = [0 for i in range(LEN)]
				for i in range(LEN):
					index = eval(str(model[i])[2:])
					fff[index] = eval(str(model[model[i]]))
				ans = (''.join([chr(x) for x in fff]))
				p.sendline(ans)
				xx = 0
				for i in range(len(ans)-1):
					xx += ord(ans[i])
				xx *= ord(ans[len(ans)-1])
				if xx != angka:
					print angka,"!=",xx
					continue
				print xxx,angka,"==",xx,'len=',len(ans),repr(ans)
				#print xx, len(ans)
				
				break
	except:
		print 'exception'
		print p.recv()
		print p.recv()
		print p.recv()
		print p.recv()
print p.recv()
print p.recv()
print p.recv()
print p.recv()
print p.recv()
