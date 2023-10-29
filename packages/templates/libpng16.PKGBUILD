# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

pkgname=toolchain-$WF_TOOLCHAIN-libpng16
pkgver=1.6.40
epoch=
pkgdesc="libpng for $WF_TOOLCHAIN"
arch=(any)
url=""
license=("libpng")
source=(
	"https://download.sourceforge.net/libpng/libpng-$pkgver.tar.xz"
	"file:///wf/patches/libpng-1.6.34-disable-tests.patch"
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
	'535b479b2467ff231a3ec6d92a525906fb8ef27978be4f66dbe05d3f3a01b3a1'
	'SKIP'
)
options=(!strip)

. "/wf/config/runtime-env-vars.sh"

prepare() {
	# ???
	tar xf libpng-$pkgver.tar

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
