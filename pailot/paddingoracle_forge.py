from pwn import *

context.log_level = 'warn'

def xor(s1, s2):
    return ''.join(chr(ord(x) ^ ord(y)) for x, y in zip(s1, s2))

def str_replace(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

target = [
    '{"username": "gu',
    'est", "expires":',
    ' "2030-01-07", "',
    'is_admin":  "tru',
    'e"}'+'\x0d'*13
]

iv = 'This is an IV456'

block = [
    iv,
    '0'*16,
    '0'*16,
    '0'*16,
    '0'*16,
    'A'*16
]
for n_block in range(len(block)-2,-1,-1):
    for i in range(16):
        print 'Guessing [{}]-byte'.format(15-i)
        for j in range(0,256):
            block[n_block] = str_replace(block[n_block], 15-i, chr(j))

            ciphertext = (block[n_block]+block[n_block+1]).encode('hex')

            r = remote('2018shell2.picoctf.com',6246)

            r.recvuntil('What is your cookie?\n')
            r.sendline(ciphertext)
            response = r.recv()

            if response.find('invalid padding') == -1:
                for k in range(i+1):
                    if i == 15:
                        break
                    new_val = chr(ord(block[n_block][15-k]) ^ (i+1) ^ (i+2))
                    block[n_block] = str_replace(block[n_block], 15-k, new_val)
                print 'FOUND valid ciphertext:', ciphertext
                break

        print 'Moving to previous bytes...'

    print 'Flipping to desired plaintext...'
    block[n_block] = xor(block[n_block], '\x10'*16)
    block[n_block] = xor(block[n_block], target[n_block])

print 'Final ciphertext:', ''.join(block).encode('hex')
