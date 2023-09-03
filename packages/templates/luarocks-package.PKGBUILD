# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

build_luarocks() {
	if [ "$WF_HOST_OS" == "windows" ]; then
		# TODO: Use toolchain-provided Lua build.
		luarocks \
			make --tree=./build "$pkgrock".rockspec
	else
		luarocks-5.4 \
			LDFLAGS="$WF_RUNTIME_LDFLAGS" \
			LUA_INCDIR="$WF_PATH"/include \
			LUA_LIBDIR="$WF_PATH"/lib/lua/5.4 \
			make --tree=./build "$pkgrock".rockspec
	fi
}
