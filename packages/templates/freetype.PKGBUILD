# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

pkgname=toolchain-$WF_TOOLCHAIN-freetype
pkgver=2.13.3
epoch=
pkgdesc="freetype for $WF_TOOLCHAIN"
arch=(any)
url="https://freetype.org/"
license=("FTL")
source=(
	"https://download.savannah.gnu.org/releases/freetype/freetype-$pkgver.tar.xz"
	"freetype-2.13.0-smaller.patch"
)
depends=(
	toolchain-$WF_TOOLCHAIN-binutils
	toolchain-$WF_TOOLCHAIN-gcc-libs
	toolchain-$WF_TOOLCHAIN-gcc
	toolchain-$WF_TOOLCHAIN-picolibc-generic
)
groups=(toolchain-$WF_TOOLCHAIN-extra)
sha256sums=(
	'0550350666d427c74daeb85d5ac7bb353acba5f76956395995311a9c6f063289'
	'SKIP'
)
options=(!strip)

. "/wf/config/runtime-env-vars.sh"

prepare() {
	cd freetype-$pkgver
	patch -p1 <../freetype-2.13.0-smaller.patch
}

build() {
	wf_use_toolchain $WF_TOOLCHAIN $WF_TARGET

	cd freetype-$pkgver
	./configure --prefix="$WF_TOOLCHAIN_PREFIX" --host=$WF_TARGET --disable-shared --enable-static \
		--with-zlib=no --with-bzip2=no --with-png=no
	make
}

package() {
	wf_use_toolchain $WF_TOOLCHAIN $WF_TARGET

	cd freetype-$pkgver
	DESTDIR="$pkgdir" make -j1 install
	cd "$pkgdir"
	wf_relocate_path_to_destdir
}
