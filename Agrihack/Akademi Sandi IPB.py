#!/usr/bin/python
from Crypto.Cipher import AES
import sys

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def header():
	print "-"*25
	print " Akademi Sandi IPB (ASI)"
	print " Pesan rahasia no.1337"
	print "-"*25

def padding_pesan(pesan_rahasia):
	pesan_rahasia = pesan_rahasia + 'T'
	while (len(pesan_rahasia)%16) != 0:
		pesan_rahasia = pesan_rahasia + 'F'
	return pesan_rahasia

def pesan():
	print "Pesan berikut sangatlah rahasia,\nanda adalah agen terpilih.\nsimpan dan jangan bocorkan informasi ini!\n"

def enkripsi_pesan(id_agen):
	pesan = open('flag', 'r').read().strip()
	kunci = open('key', 'r').read().strip()
	pesan_rahasia = 'Pesan Rahasia no.1337 -> '+id_agen+': '+pesan
	pesan_rahasia = padding_pesan(pesan_rahasia)

	cipher = AES.new(kunci,AES.MODE_ECB)
	ciphertext = cipher.encrypt(pesan_rahasia).encode('hex')
	return ciphertext

def main():
	id_agen = raw_input("Silahkan masukkan ID agen: ")
	ciphertext = enkripsi_pesan(id_agen)
	header()
	pesan()
	print ciphertext + '\n'
	lagi = raw_input("Terima pesan rahasia lagi? Y/N\n")
	if(lagi=='Y'): main()

def init(payload):
	whole = enkripsi_pesan(payload)
	enc = ['' for i in range(len(whole)/32)]
	for i in range(len(whole)):
		enc[i//32] += whole[i]
	return enc

main()

base = 'aaaaaaaaaaaa: agrihack{aaaaa'
payload = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa: agrihack{aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
dist = (len(payload) - len(base))//32 + 1
col = 22 + (len(payload) - len(base))/2
print 'col =', col, 'dist =',dist

while payload[:9] != 'agrihack{':
	enc = init(payload)
	n = len(enc)
	#for i in range(len(enc)):
		#print enc[i]
	for i in range(n-1, -1, -1):
		print i
		if enc[i] == enc[i-dist]:
			break
			
	guess = ' '
	payload = payload[1:]
	payload = payload[:col] + guess + payload[col+1:]
	enc = init(payload)
	
	while enc[i] != enc[i-dist]:
		# print payload
		guess = chr(ord(guess) + 1)
		payload = payload[:col] + guess + payload[col+1:]
		enc = init(payload)
	
	print payload


