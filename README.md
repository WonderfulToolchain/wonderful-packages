# wonderful-packages

## Supported architectures

| Description | Container/Shell argument | makepkg/pacman | Supported |
| - | - | - | - |
| x86_64 | x86_64 | x86_64 | Yes |
| ARMv6+, hard float | arm32v6 | armv6h | Yes |
| AArch64 | aarch64 | aarch64 | Yes |
| x86 (i686) | i686 | i686 | No |

## Known issues

### sudo: effective uid is not 0, is /usr/bin/sudo on a file system with the 'nosuid' option set or an NFS file system without root privileges?

On Arch Linux, this can be resolved by editing the following files:

 * `/usr/lib/binfmt.d/qemu-arm-static.conf`
 * `/usr/lib/binfmt.d/qemu-aarch64-static.conf`
 * etc.

to replace the trailing flag `F` with `FOC`.
