# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2024

if [ "x$GCC_IS_LIBSTDCXX" = "xyes" ]; then
	pkgname=(toolchain-gcc-$GCC_TARGET-libstdcxx-picolibc)
	depends=(toolchain-gcc-$GCC_TARGET-gcc toolchain-gcc-$GCC_TARGET-picolibc-generic)
	arch=(any)
else
	pkgname=(toolchain-gcc-$GCC_TARGET-gcc toolchain-gcc-$GCC_TARGET-gcc-libs)
	depends=(runtime-gcc-libs runtime-musl toolchain-gcc-$GCC_TARGET-binutils)
	arch=("x86_64" "aarch64")
fi
_pkgver=15.2.1
_gmpver=6.3.0
_mpfrver=4.2.2
_mpcver=1.3.1
_islver=0.27
pkgdesc="The GNU Compiler Collection"
makedepends=(runtime-musl-dev)
groups=(toolchain-gcc-$GCC_TARGET)
url="https://gcc.gnu.org"
license=("GPL-3.0-or-later")
source=("gcc::git+https://github.com/WonderfulToolchain/gcc#branch=wonderful/gcc-15"
        "http://gmplib.org/download/gmp/gmp-$_gmpver.tar.xz"
        "http://www.mpfr.org/mpfr-$_mpfrver/mpfr-$_mpfrver.tar.xz"
        "http://ftp.gnu.org/gnu/mpc/mpc-$_mpcver.tar.gz"
	"https://libisl.sourceforge.io/isl-$_islver.tar.xz"
)
sha256sums=(
	'SKIP'
	'a3c2b80201b89e68616f4ad30bc66aee4927c3ce50e33929ca819d5c43538898'
	'b67ba0383ef7e8a8563734e2e889ef5ec3c3b898a01d00fa0a6869ad81c6ce01'
	'ab642492f5cf882b74aa0cb730cd410a81edcdbec895183ce930e706c1c759b8'
	'6d8babb59e7b672e8cb7870e874f3f7b813b6e00e6af3f8b04f7579965643d5c'
)

. "/wf/config/runtime-env-vars.sh"

GIT_REPO_DIR=gcc
. "../templates/git-pkgver.PKGBUILD"

prepare() {
	mkdir -p "gcc-build"
	cd gcc

	ln -s ../"gmp-$_gmpver" gmp
	ln -s ../"mpfr-$_mpfrver" mpfr
	ln -s ../"mpc-$_mpcver" mpc
	ln -s ../"isl-$_islver" isl
}

build() {
	export PATH=$WF_PATH/toolchain/gcc-$GCC_TARGET/bin:$PATH

	if [ "x$GCC_IS_LIBSTDCXX" = "xyes" ]; then
		build_libstdcxx_arg="--enable-libstdcxx"
		configure_cmd=../gcc/libstdc++-v3/configure

		wf_disable_host_build
	else
		build_libstdcxx_arg="--disable-libstdcxx"
		configure_cmd=../gcc/configure
	fi
	cd gcc-build

	# workaround for https://gcc.gnu.org/bugzilla/show_bug.cgi?id=108300
	if [ "$WF_HOST_OS" == "windows" ]; then
		CPPFLAGS='-DWIN32_LEAN_AND_MEAN'
	fi

	# TODO: It's strange that --with-gnu-as/--with-gnu-ld is required for cross-compilation.
	# I'd assume it would automatically check the target assembler/linker. I wonder what the issue is.
	$configure_cmd \
		--prefix="$WF_PATH/toolchain/gcc-$GCC_TARGET" \
		--target=$GCC_TARGET \
		--with-pkgversion="$WF_NAME" \
		--with-bugurl="$WF_BUGURL" \
		--with-stage1-ldflags="$WF_RUNTIME_LDFLAGS" \
		--without-headers \
		--enable-plugins \
		--enable-poison-system-directories \
		--disable-bootstrap \
		--disable-gcov \
		--disable-nls \
		--disable-shared \
		--disable-werror \
		--disable-libquadmath \
		--disable-libssp \
		--disable-libstdcxx-pch \
		--disable-libstdcxx-threads \
		--disable-libstdcxx-verbose \
		--disable-libunwind-exceptions \
		--disable-threads \
		--with-gnu-as \
		--with-gnu-ld \
		--with-isl \
		$build_libstdcxx_arg \
		"${GCC_EXTRA_ARGS[@]}"

	make
}

package_toolchain-gcc-template-gcc() {
	cd gcc-build
	make DESTDIR="$pkgdir" install-gcc install-libcc1
	cd "$pkgdir"
	wf_relocate_path_to_destdir

	rm toolchain/gcc-$GCC_TARGET/share/info/dir
	rm toolchain/gcc-$GCC_TARGET/lib/gcc/$GCC_TARGET/$_pkgver/include-fixed/README

	# HACK: As we don't build with a C library present, limits.h
	# assumes no such library is present.

	cd "$srcdir"/gcc/gcc
	cat limitx.h glimits.h limity.h > "$pkgdir"/toolchain/gcc-$GCC_TARGET/lib/gcc/$GCC_TARGET/$_pkgver/include/limits.h
}

package_toolchain-gcc-template-gcc-libs() {
	pkgdesc="GCC-provided libraries"
	depends=("toolchain-gcc-$GCC_TARGET-binutils" "toolchain-gcc-$GCC_TARGET-gcc")
	options=(!strip)

	cd gcc-build
	make DESTDIR="$pkgdir" install-target-libgcc
	cd "$pkgdir"
	wf_relocate_path_to_destdir

	# HACK: Avoid conflict with -gcc package.
	rm toolchain/gcc-$GCC_TARGET/lib/gcc/$GCC_TARGET/*/include/unwind.h
}

package_toolchain-gcc-template-libstdcxx-picolibc() {
	pkgdesc="GCC-provided libstdc++, compiled for use with picolibc"
	options=(!strip)

	cd gcc-build
	make DESTDIR="$pkgdir" install
	cd "$pkgdir"
	wf_relocate_path_to_destdir
	rm -r toolchain/gcc-$GCC_TARGET/lib/*.py || true
	rm -r toolchain/gcc-$GCC_TARGET/share || true

	mkdir toolchain/gcc-$GCC_TARGET/$GCC_TARGET
	mv toolchain/gcc-$GCC_TARGET/include toolchain/gcc-$GCC_TARGET/$GCC_TARGET/
	mv toolchain/gcc-$GCC_TARGET/lib toolchain/gcc-$GCC_TARGET/$GCC_TARGET/
}
