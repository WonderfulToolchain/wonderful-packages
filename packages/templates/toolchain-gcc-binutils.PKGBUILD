# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

pkgname=toolchain-gcc-$GCC_TARGET-binutils
pkgver=2.45.1
epoch=
pkgdesc="GNU binary utilities"
arch=("x86_64" "aarch64")
url="http://www.gnu.org/software/binutils"
license=("GPL-3.0-or-later")
source=("http://ftp.gnu.org/gnu/binutils/binutils-$pkgver.tar.xz")
depends=(runtime-gcc-libs runtime-musl)
makedepends=(runtime-musl-dev)
groups=(toolchain-gcc-$GCC_TARGET)
sha256sums=('5fe101e6fe9d18fdec95962d81ed670fdee5f37e3f48f0bef87bddf862513aa5')

. "/wf/config/runtime-env-vars.sh"

prepare() {
	mkdir -p "binutils-$pkgver-build"
}

build() {
	cd "binutils-$pkgver"-build
	../"binutils-$pkgver"/configure \
		--prefix="$WF_PATH"/toolchain/gcc-$GCC_TARGET \
		--target=$GCC_TARGET \
		--with-bugurl="$WF_BUGURL" \
		--without-zstd \
		--enable-64-bit-bfd \
		--enable-colored-disassembly \
		--enable-gold=no \
		--enable-ld=default \
		--enable-lto \
		--enable-plugins \
		--enable-threads \
		--disable-gdb \
		--disable-gprof \
		--disable-libdecnumber \
		--disable-nls \
		--disable-shared \
		--disable-sim \
		--disable-warn-rwx-segments \
		--disable-werror \
		--with-float=soft \
		"${GCC_EXTRA_ARGS[@]}"
	make configure-host
	make LDFLAGS="$WF_RUNTIME_LDFLAGS"
}

package() {
	cd "binutils-$pkgver"-build
	make DESTDIR="$pkgdir" install
	cd "$pkgdir"
	wf_relocate_path_to_destdir
	rm toolchain/gcc-$GCC_TARGET/share/info/dir
}
