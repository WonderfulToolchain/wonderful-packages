# wonderful-packages

Repository containing the build scripts and infrastructure for Wonderful's Pacman-based packaging.

## Targets

### Supported

| Target | Description | Container |
| - | - | - |
| linux/x86_64 | Linux, x86_64 | linux/x86_64 |
| linux/aarch64 | Linux, AArch64 | linux/aarch64 |
| windows/x86_64 | Windows, x86_64 | windows/x86_64 | 

### Unsupported

| Target | Description | Container |
| - | - | - |
| linux/armv6h | Linux, ARMv6+, hard float | linux/arm32v6 |
| linux/riscv64 | Linux, RISC-V | linux/riscv64 |

## Installation

The build system is not well tested outside of my own computers, so the steps may not be fully complete. Caveat emptor.

### Linux (recommended)

Arch Linux on an x86_64 or AArch64 machine is recommended.

* On Arch Linux, `python-uv`, `podman`, `qemu-user-static` and `qemu-user-static-binfmt` should be installed, probably among some others.
* On Debian, `pipx` + `pipx install uv`, `qemu-user-binfmt`, `qemu-user-static`.

Some additional configuration steps have to be undertaken:

* Make sure to install `qemu-user-static-binfmt` and not `qemu-user-binfmt`; otherwise, podman will error with `exec container process (missing dynamic library?) '/bin/sh': No such file or directory`.
* For building on non-native architectures, the QEMU static interpreter has to run with root permissions. Not doing so will lead to an `sudo: effective uid is not 0, is /usr/bin/sudo on a file system with the 'nosuid' option set or an NFS file system without root privileges?` error. On Arch Linux, this can be resolved using the following steps:
  1. Edit the following files to replace the trailing flag `F` with `FOC`, or `FP` with `FPOC`:
    * `/usr/lib/binfmt.d/qemu-arm-static.conf`
    * `/usr/lib/binfmt.d/qemu-aarch64-static.conf`
    * etc.
  2. Run `systemctl restart systemd-binfmt` to apply changes.
* For building on MSYS2 via WINE and Docker on recent CPUs, the Linux kernel has to be launched with PKU/PKRU disabled due to a Cygwin bug by passing `nopku` on its command line. See [msys2-runtime/#295](https://github.com/msys2/msys2-runtime/issues/295) for more information.

### Windows

Manual installation instructions:

1. Install the latest version of MSYS2.
2. The repository must be installed to `/wf`. While `pkgtool` is directory-agnostic, the `PKGBUILD` scripts are not.
3. Use the UCRT64 environment to work with `pkgtool`.
4. Install UCRT64 Python and SSL certificates (required for `mirror`): `pacman -S mingw-w64-ucrt-x86_64-ca-certificates mingw-w64-ucrt-x86_64-python mingw-w64-ucrt-x86_64-python-uv`.
5. Install build dependencies (this list is probably not 100% complete): `pacman -S autoconf autoconf-archive automake base-devel bison flex git libtool lld mingw-w64-ucrt-x86_64-autotools mingw-w64-ucrt-x86_64-cmake mingw-w64-ucrt-x86_64-lua-luarocks mingw-w64-ucrt-x86_64-meson mingw-w64-ucrt-x86_64-toolchain nasm ninja`.
6. Copy `misc/windows/makepkg.conf` to `/etc/makepkg.conf`.
7. To fix `luarocks` not being able to create directories, you will need to `luarocks install luafilesystem` first, while creating all the erroring directories manually. See [MINGW-packages/#12002](https://github.com/msys2/MINGW-packages/pull/12002).

Notes:

* `wf-pacman` is built with MSYS rather than UCRT64. This currently appears to require a separate, manual installation of uv via pip.
* For an unknown reason, `wf-sox` expects `/msys64/usr/share/aclocal` to have the contents of `/usr/share/aclocal`.

## Usage

### Downloading repositories

Before using `pkgtool` for the first time, one should initialize the uv-based virtual environment:

    $ uv sync

To start working with `pkgtool`, one must make mirrors of all the relevant repositories. This can be done by writing:

    $ ./pkgtool mirror -c [targets...]

If no `targets` are specified, all targets supported by your environment will be downloaded. The `-c` argument removes all outdated/unused packages.

### Building packages

Example call:

    $ ./pkgtool build wf-tools@x86_64,aarch64 target-wswan-examples 

The `@x86_64` suffix can be used to narrow down a build to specific architectures. This is useful for quicker building and testing of in-development packages.

### Upgrading core components

#### MSYS2

After upgrading MSYS2, `runtime-gcc-libs` usually has to be updated. Failure to do so will lead to failures on trying to run EXEs in user installations.

#### wf-pacman

The Linux bootstraps are effectively self-contained repackagings of a pre-installed `wf-pacman` package, allowing easy end user installation.

    $ ./pkgtool build-bootstrap [targets...]

### Additional reading

* [File system hierarchy](https://wonderful.asie.pl/wiki/doku.php?id=design:filesystem_hierarchy)

## Forking

As the Wonderful toolchain is open source, it can be forked to provide custom builds. While the licensing terms are formally binding, I would like to additionally request holding to the following guidelines when developing a fork:

- Do not call your fork "Wonderful". It's okay to refer to it informatively as a fork of the Wonderful toolchain, but it's not okay to imply that your fork *is* the Wonderful toolchain. To change the toolchain's brand name in built executables, edit `WF_NAME` in `config/runtime-env-vars.sh`.
- Make sure to document it clearly that any issues with the fork should be reported to you and/or the maintainers of the fork. To change the bug report URL used by GCC and some other programs, change `WF_BUGURL` in `config/runtime-env-vars.sh`.
- If your fork breaks compatibility with the Wonderful toolchain in **any** way (including porting to a platform or architecture not supported by the toolchain), please use a different `WONDERFUL_TOOLCHAIN` location than `/opt/wonderful`. This allows upstream to create its own version in the future without causing conflict between the two. This is achievable for the most part by changing `WF_LOCAL_PATH` in `config/runtime-env-vars.sh`, but it may require additional changes as well.

## License

Unless otherwise specified, the build scripts (`config/`, `packages/`) are licensed under Creative Commons 0. I don't see why instructions on building otherwise libre toolchains should be restricted by copyright in any way.

The Python package management tool (`tool/`) is licensed under the MIT license.

If you'd like to use these scripts and/or tools to build your own repository or toolchain, I'd appreciate it if steps were made to ensure that such toolchains are not misrepresented as my own work.
