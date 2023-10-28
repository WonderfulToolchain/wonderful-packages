// SPDX-License-Identifier: CC0-1.0
// SPDX-FileContributor: Adrian "asie" Siekierka, 2023

#include <stddef.h>

/* Minimal, non-functional crt0 used as a workaround for C compiler tests in
 * Autoconf. Platforms are expected to provide their own crt0/linkscript.
 */

int main(int argc, char *argv[]);
void _start(void) { main(0, (void*)0); }

/* As we expect platforms to come with their own implementation of sbrk()
 * and etc., put stub implementations here to match.
 */

void *sbrk(ptrdiff_t incr) { return NULL; }
unsigned int __aeabi_read_tp(void) { return 0; }
