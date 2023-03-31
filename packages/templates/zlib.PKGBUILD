# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

pkgname=toolchain-$WF_TOOLCHAIN-zlib
pkgver=1.2.13
epoch=
pkgdesc="zlib for $WF_TOOLCHAIN"
arch=(any)
url="https://zlib.net/"
license=("zlib")
source=(
	"https://zlib.net/zlib-$pkgver.tar.gz"
)
depends=(
	toolchain-$WF_TOOLCHAIN-binutils
	toolchain-$WF_TOOLCHAIN-gcc-libs
	toolchain-$WF_TOOLCHAIN-gcc
	toolchain-$WF_TOOLCHAIN-picolibc-generic
)
groups=(toolchain-$WF_TOOLCHAIN-extra)
sha256sums=(
	'b3a24de97a8fdbc835b9833169501030b8977031bcb54b3b3ac13740f846ab30'
)
options=(!strip)

. "/wf/config/runtime-env-vars.sh"

build() {
	wf_use_toolchain $WF_TOOLCHAIN $WF_TARGET

	cd zlib-$pkgver
	CHOST=$WF_TARGET ./configure --static --prefix="$WF_TOOLCHAIN_PREFIX"
	make libz.a
}

package() {
	wf_use_toolchain $WF_TOOLCHAIN $WF_TARGET

	cd zlib-$pkgver
	DESTDIR="$pkgdir" make -j1 install
	cd "$pkgdir"
	wf_relocate_path_to_destdir
}
