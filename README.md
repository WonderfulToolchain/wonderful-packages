# wonderful-packages

Repository containing the build scripts and infrastructure for Wonderful's Pacman-based packaging.

## Supported targets

Listed from most to least supported.

| Target | Description | Container |
| - | - | - |
| linux/x86_64 | Linux, x86_64 | x86_64 |
| linux/aarch64 | Linux, AArch64 | aarch64 |
| linux/armv6h | Linux, ARMv6+, hard float | arm32v6 |
| windows/x86_64 | Windows, x86_64 | N/A | 

## Guide

As the packaging system is intended for internal use only, the list of tested setups is highly specific:

* For Linux development, Arch Linux on an x86_64 or AArch64 machine is recommended. `python-poetry`, `podman`, `qemu-user-static` and `qemu-user-static-binfmt` should be installed, probably among some others.
* For Windows development, MSYS2 should be installed. Unlike Linux, development is not containerized; as such, all packages' build dependencies must be installed by the user. Windows-specific instructions are provided at the end of the guide.

### Downloading repositories

Before using `pkgtool` for the first time, one should initialize the Poetry-based virtual environment:

    $ poetry install

To start working with `pkgtool`, one must make mirrors of all the relevant repositories. This can be done by writing:

    $ ./pkgtool mirror -c [targets...]

If no `targets` are specified, all targets supported by your environment will be downloaded. The `-c` argument removes all outdated/unused packages.

### Building packages

Example call:

    $ ./pkgtool build wf-tools@x86_64,aarch64 target-wswan-examples 

### Building Linux bootstraps

The Linux bootstraps are effectively self-contained repackagings of a pre-installed `wf-pacman` package, allowing easy end user installation.

    $ ./pkgtool build-bootstrap [targets...]

### Installation details

#### Windows

Installation instructions:

1. The repository must be installed to `/wf`. While `pkgtool` is directory-agnostic, the `PKGBUILD` scripts are not.
2. Use the UCRT64 environment to work with `pkgtool`.
3. Install UCRT64 Python and SSL certificates (required for `mirror`): `pacman -S mingw-w64-ucrt-x86_64-ca-certificates mingw-w64-ucrt-x86_64-python mingw-w64-ucrt-x86_64-python-poetry`.
4. Install build dependencies (this list is probably not 100% complete): `pacman -S autoconf auitoconf-archive automake base-devel bison flex git libtool lld mingw-w64-ucrt-x86_64-autotools mingw-w64-ucrt-x86_64-cmake mingw-w64-ucrt-x86_64-lua-luarocks mingw-w64-ucrt-x86_64-meson mingw-w64-ucrt-x86_64-toolchain nasm ninja`.
5. Copy `misc/windows/makepkg.conf` to `/etc/makepkg.conf`.
6. To fix `luarocks` not being able to create directories, you will need to `luarocks install luafilesystem` first, while creating all the erroring directories manually. See [MINGW-packages/#12002](https://github.com/msys2/MINGW-packages/pull/12002).

Notes:

* `wf-pacman` is built with MSYS rather than UCRT64. This currently appears to require a separate, manual installation of Poetry via pip.
* For an unknown reason, `wf-sox` expects `/msys64/usr/share/aclocal` to have the contents of `/usr/share/aclocal`.

## Known issues

### sudo: effective uid is not 0, is /usr/bin/sudo on a file system with the 'nosuid' option set or an NFS file system without root privileges?

On Arch Linux, this can be resolved using the following steps:

1. Edit the following files to replace the trailing flag `F` with `FOC`, or `FP` with `FPOC`:
  * `/usr/lib/binfmt.d/qemu-arm-static.conf`
  * `/usr/lib/binfmt.d/qemu-aarch64-static.conf`
  * etc.
2. Run `systemctl restart systemd-binfmt` to apply changes.

## License

Unless otherwise specified, the build scripts (`config/`, `packages/`) are licensed under Creative Commons 0. I don't see why instructions on building otherwise libre toolchains should be restricted by copyright in any way.

The Python package management tool (`tool/`) is licensed under the MIT license.

If you'd like to use these scripts and/or tools to build your own repository or toolchain, I'd appreciate it if steps were made to ensure that such toolchains are not misrepresented as my own work.
