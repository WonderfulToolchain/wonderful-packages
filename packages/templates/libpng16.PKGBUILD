# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

pkgname=toolchain-$WF_TOOLCHAIN-libpng16
pkgver=1.6.39
epoch=
pkgdesc="libpng for $WF_TOOLCHAIN"
arch=(any)
url=""
license=("libpng")
source=(
	"https://download.sourceforge.net/libpng/libpng-$pkgver.tar.xz"
	"libpng-1.6.34-disable-tests.patch"
)
depends=(
	toolchain-$WF_TOOLCHAIN-binutils
	toolchain-$WF_TOOLCHAIN-gcc-libs
	toolchain-$WF_TOOLCHAIN-gcc
	toolchain-$WF_TOOLCHAIN-picolibc-generic
	toolchain-$WF_TOOLCHAIN-zlib
)
groups=(toolchain-$WF_TOOLCHAIN-extra)
sha256sums=(
	'1f4696ce70b4ee5f85f1e1623dc1229b210029fa4b7aee573df3e2ba7b036937'
	'SKIP'
)
options=(!strip)

. "/wf/config/runtime-env-vars.sh"

prepare() {
	cd libpng-$pkgver
	patch -p1 <../libpng-1.6.34-disable-tests.patch
	autoreconf -i
}

build() {
	wf_use_toolchain $WF_TOOLCHAIN $WF_TARGET

	cd libpng-$pkgver
	./configure --prefix="$WF_TOOLCHAIN_PREFIX" --host=$WF_TARGET --disable-shared --enable-static
	make
}

package() {
	wf_use_toolchain $WF_TOOLCHAIN $WF_TARGET

	cd libpng-$pkgver
	DESTDIR="$pkgdir" make -j1 install
	cd "$pkgdir"
	wf_relocate_path_to_destdir
}
