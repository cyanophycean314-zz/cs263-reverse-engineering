/**
 * crackpw.c
 *
 Given a certain hash, this program will read the rockyou-top-25000.txt and hash
 each given password. If they match, that's great and it'll return. Otherwise, sad.
 */

#include "hashpw.h"  // so that you can call hashpw()
#include "stdio.h"   // for fscanf
#include "string.h"  // for strlen

/**
 * Given a hash, tries to generate a cleartext ASCII password that hashes to
 * the same value.
 *
 * If successful, returns the length of the cracked password and stores the
 * cracked password in "dest". If unsuccessful, returns 0.
 */
int crackpw(char dest[256], unsigned int hash) {
  char password[256];
  FILE * pw_file = fopen("data/rockyou-top-25000.txt", "r");
  int pws_tested = 0;
  while(1) {
    int num = fscanf(pw_file, "%s", password);
    if (num != 1) {
      return 0; // Unsuccessful crack
    }
    // printf("Read %d: %s\n", pws_tested, password);
    int pw_len = strlen(password);
    if (hashpw(password, pw_len) == hash) {
      strncpy(dest, password, pw_len);
      printf("%d\n", pws_tested);
      return pw_len;
    }
    pws_tested++;
  }

  return 0;
}
