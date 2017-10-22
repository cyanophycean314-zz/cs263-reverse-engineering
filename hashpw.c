/**
 * hashpw.c
 *
 First I found the name and location of the hash function via objdump.
 Then I set a breakpoint for it at gdb and hand-transcribed the instructions.
 I wrote down in a human readable way what each instruction did, then combined
 instructions that we would naturally chain together.
 I figured out that 0x8(ebp) refers to the string itself and 0xc(ebp) refers to len
 -0xc(ebp) was used to store the hash as it was being built and -0x8 was just the counter.
 In order for the function to actually run, you have to enter a valid username, so I
 looked one up in the decrypted_passwords.txt
 I wrote down the instructions while stepping through the hash function in gdb to make sure
 my code was making sense. Then I wrote the C code and put in print statements to make sure
 my code was consistent with the assembly at each iteration of the main loop. This involved
 setting a breakpoint at the end of each iteration of the hasher and checking for
 consistency. Then I tested it and it worked.
 */

#include <stdio.h>


unsigned int hashpw(const char* plaintext, int len) {
  unsigned int hash = 0;
  for (int i = 0; i < len; i++) {
    int extra = 0x100 * plaintext[i] + plaintext[i];
    hash = 2 * (hash ^ extra);
    // printf("%d: %x %x\n", i, hash, extra);
  }
  if (len >= 0) {
    hash = hash | plaintext[0];
  }
  // printf("%x\n", hash);
  hash = hash ^ 0xfeedface;
  // printf("final: %x\n", hash);
  return hash;
}
