# If you change the OS version here, make sure to bump up and rebuild runtime-gcc-libs.
# If the musl version changes drastically, it may also be a good idea to review runtime-musl.
FROM alpine:3.16
# Install packages:
# - compiler/make/etc. [build-base]
# - tools for building/installing packages [fakeroot git pacman pacman-makepkg curl xz zstd sudo cmake patchelf pkgconf]
# - ffmpeg build dependencies [nasm]
# - binutils build dependencies [texinfo]
# - binutils-ia16 build dependencies [bison, flex]
# - pacman build dependencies [meson]
RUN apk add --no-cache build-base fakeroot git pacman pacman-makepkg curl xz zstd sudo cmake patchelf pkgconf nasm texinfo bison flex meson linux-headers
# Install packages:
# - pacman static library dependencies
# RUN apk add --no-cache curl-dev libarchive-dev gpgme-dev openssl1.1-compat-dev acl-static expat-static xz-dev zstd-static lz4-static
# Configure pacman/makepkg
RUN mkdir -p /opt/wonderful/pacman/db
COPY config/makepkg.conf config/pacman.conf /etc
# Add build user
RUN adduser -D wfbuilder
RUN sh -c 'echo "wfbuilder ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/wfbuilder && chmod 0440 /etc/sudoers.d/wfbuilder'
