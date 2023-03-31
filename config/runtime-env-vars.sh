#!/bin/sh

# wf-pacman sees $WF_PATH as $WF_DESTDIR
WF_PATH="/opt/wonderful"
WF_DESTDIR="/"

WF_RUNTIME_LDFLAGS="-Wl,-rpath,$WF_PATH/lib -Wl,--dynamic-linker=$WF_PATH/lib/ld-musl-$CARCH.so.1"

WF_RUNTIME_INCLUDES="-I$WF_PATH/include"
WF_RUNTIME_LDFLAGS="$WF_RUNTIME_LDFLAGS -L$WF_PATH/lib"

wf_relocate_path_to_destdir() {
	if [ -d opt/wonderful ]; then
		mv opt _opt
		mv _opt/wonderful/* .
		rm -rf _opt
	fi
}

wf_runtime_patchelf() {
	patchelf --set-rpath "$WF_PATH/lib" "$1"
	# Setting an interpreter is supported only on executables.
	# For libraries, ignore the failure.
	patchelf --set-interpreter "$WF_PATH/lib/ld-musl-$CARCH.so.1" "$1" || true
}

wf_use_toolchain() {
	export WF_TOOLCHAIN_PREFIX="$WF_PATH/toolchain/$1/$2"
	export PATH="$WF_PATH/toolchain/$1/bin":$PATH
}
