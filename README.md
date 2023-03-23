# wonderful-packages

Repository used to build binary packages for Wonderful's Pacman repo. Somewhat internal.

## Hints

    $ ./build-package.sh packages/wf-pacman [x86_64]
    $ ./rebuild-repository.sh
    $ ./build-bootstrap.sh x86_64

## Supported architectures

| Description | Container/Shell argument | makepkg/pacman | Supported |
| - | - | - | - |
| x86_64 | x86_64 | x86_64 | Yes |
| ARMv6+, hard float | arm32v6 | armv6h | Yes |
| AArch64 | aarch64 | aarch64 | Yes |
| x86 (i686) | i686 | i686 | No |

## License

Where possible, the build scripts are licensed under Creative Commons 0, as I don't see why instructions on building libre toolchains should be restricted by copyright in any way.
However, if you'd like to use these instructions to build your own toolchain, I'd appreciate it if steps were made to ensure that such toolchains are not misrepresented as my own work.

Some scripts are sourced from external locations and may be licensed under more restrictive terms.

## Known issues

### sudo: effective uid is not 0, is /usr/bin/sudo on a file system with the 'nosuid' option set or an NFS file system without root privileges?

On Arch Linux, this can be resolved by editing the following files:

 * `/usr/lib/binfmt.d/qemu-arm-static.conf`
 * `/usr/lib/binfmt.d/qemu-aarch64-static.conf`
 * etc.

to replace the trailing flag `F` with `FOC`.
