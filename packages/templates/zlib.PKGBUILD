# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

pkgname=toolchain-$WF_TOOLCHAIN-zlib
pkgver=1.3
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
	'ff0ba4c292013dbc27530b3a81e1f9a813cd39de01ca5e0f8bf355702efa593e'
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
