# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

pkgname=toolchain-$WF_TOOLCHAIN-libpng16
pkgver=1.6.48
epoch=
pkgdesc="libpng for $WF_TOOLCHAIN"
arch=(any)
url=""
license=("libpng")
source=(
	"https://download.sourceforge.net/libpng/libpng-$pkgver.tar.xz"
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
	'46fd06ff37db1db64c0dc288d78a3f5efd23ad9ac41561193f983e20937ece03'
)
options=(!strip)

. "/wf/config/runtime-env-vars.sh"

build() {
	wf_use_toolchain $WF_TOOLCHAIN $WF_TARGET

	cd libpng-$pkgver
	CPPFLAGS="$LIBPNG_COMPILE_FLAGS" \
	./configure --prefix="$WF_TOOLCHAIN_PREFIX" --host=$WF_TARGET \
		--disable-shared --enable-static \
		--disable-tests --disable-tools
	make
}

package() {
	wf_use_toolchain $WF_TOOLCHAIN $WF_TARGET

	cd libpng-$pkgver
	DESTDIR="$pkgdir" make -j1 install
	cd "$pkgdir"
	wf_relocate_path_to_destdir
}
