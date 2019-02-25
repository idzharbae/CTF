#include <stdio.h>
#include <stdlib.h>

//compile with gcc -o oob oob.c
//this binary is for learning about out of bound vuln to get a shell

int main()
{
  char buff[128];
  puts("Kirim kesan pesan anda : ");
  gets(buff);
  puts("Terima kasih :)");
 return 0;
}