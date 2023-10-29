# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

if [ "x$GCC_IS_LIBSTDCXX" = "xyes" ]; then
	pkgname=(toolchain-gcc-$GCC_TARGET-libstdcxx-picolibc)
	depends=(toolchain-gcc-$GCC_TARGET-gcc toolchain-gcc-$GCC_TARGET-picolibc-generic)
	arch=(any)
else
	pkgname=(toolchain-gcc-$GCC_TARGET-gcc toolchain-gcc-$GCC_TARGET-gcc-libs)
	depends=(runtime-gcc-libs runtime-musl toolchain-gcc-$GCC_TARGET-binutils)
	arch=("i686" "x86_64" "armv6h" "aarch64")
fi
pkgver=13.2.0
_gmpver=6.2.1
_mpfrver=4.2.0
_mpcver=1.3.1
_islver=0.26
pkgdesc="The GNU Compiler Collection"
makedepends=(runtime-musl-dev)
groups=(toolchain-gcc-$GCC_TARGET)
url="https://gcc.gnu.org"
license=("GPL-3.0-or-later")
source=("http://ftp.gnu.org/gnu/gcc/gcc-$pkgver/gcc-$pkgver.tar.xz"
        "http://gmplib.org/download/gmp/gmp-$_gmpver.tar.xz"
        "http://www.mpfr.org/mpfr-$_mpfrver/mpfr-$_mpfrver.tar.xz"
        "http://ftp.gnu.org/gnu/mpc/mpc-$_mpcver.tar.gz"
	"https://libisl.sourceforge.io/isl-$_islver.tar.xz"
	"file:///wf/patches/gcc13-poison-system-directories.patch"
	"file:///wf/patches/gcc13-clang-MJ.patch")
sha256sums=(
	'e275e76442a6067341a27f04c5c6b83d8613144004c0413528863dc6b5c743da'
	'fd4829912cddd12f84181c3451cc752be224643e87fac497b69edddadc49b4f2'
	'06a378df13501248c1b2db5aa977a2c8126ae849a9d9b7be2546fb4a9c26d993'
	'ab642492f5cf882b74aa0cb730cd410a81edcdbec895183ce930e706c1c759b8'
	'a0b5cb06d24f9fa9e77b55fabbe9a3c94a336190345c2555f9915bb38e976504'
	'SKIP'
	'SKIP'
)

. "/wf/config/runtime-env-vars.sh"

prepare() {
	mkdir -p "gcc-build"
	cd "gcc-$pkgver"

	# Not strictly necessary, but a nice-to-have.
	patch -p1 <../gcc13-poison-system-directories.patch
	patch -p1 <../gcc13-clang-MJ.patch

	# HACK: hijack RTEMS's libstdc++ crossconfig for our own purposes (which has the dynamic feature checks we want)
	sed -i "s/\*-rtems\*/*-unknown*/" libstdc++-v3/configure

	ln -s ../"gmp-$_gmpver" gmp
	ln -s ../"mpfr-$_mpfrver" mpfr
	ln -s ../"mpc-$_mpcver" mpc
	ln -s ../"isl-$_islver" isl
}

build() {
	if [ "x$GCC_IS_LIBSTDCXX" = "xyes" ]; then
		build_libstdcxx_arg="--enable-libstdcxx"
		configure_cmd=../"gcc-$pkgver"/libstdc++-v3/configure
		export PATH=/opt/wonderful/toolchain/gcc-$GCC_TARGET/bin:$PATH

		wf_disable_host_build
	else
		build_libstdcxx_arg="--disable-libstdcxx"
		configure_cmd=../"gcc-$pkgver"/configure
	fi
	cd gcc-build

	# workaround for https://gcc.gnu.org/bugzilla/show_bug.cgi?id=108300
	if [ "$WF_HOST_OS" == "windows" ]; then
		CPPFLAGS='-DWIN32_LEAN_AND_MEAN'
	fi

	$configure_cmd \
		--prefix="/opt/wonderful/toolchain/gcc-$GCC_TARGET" \
		--target=$GCC_TARGET \
		--with-pkgversion="Wonderful toolchain" \
		--with-bugurl="http://github.com/WonderfulToolchain/wonderful-packages/issues" \
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
	rm toolchain/gcc-$GCC_TARGET/lib/gcc/$GCC_TARGET/$pkgver/include-fixed/README

	# HACK: As we don't build with a C library present, limits.h
	# assumes no such library is present.

	cd "$srcdir"/gcc-"$pkgver"/gcc
	cat limitx.h glimits.h limity.h > "$pkgdir"/toolchain/gcc-$GCC_TARGET/lib/gcc/$GCC_TARGET/$pkgver/include/limits.h
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
