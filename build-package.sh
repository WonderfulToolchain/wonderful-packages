#!/bin/bash

PKGNAME=${1##*/}
shift
ROOT_DIR=$(pwd)

build_package() {
	PKGARCH="$1"
	pushd containers/"$PKGARCH"/
	podman build -t wonderful-"$PKGARCH" .
	podman build -t wonderful .
	podman run -i -v "$ROOT_DIR":/wf wonderful-"$PKGARCH" sh -c 'pacman -Syu && su -c "cd /wf/packages/'$PKGNAME' && makepkg -C --clean --syncdeps --force --noconfirm --skippgpcheck '$PKGNAME'" wfbuilder'
	popd
}

if [[ z"$1" == "z" || z"$1" == "zall" ]]; then
	if grep -q "arch=(any)" packages/$PKGNAME/PKGBUILD; then
		build_package x86_64
	else
		for i in i686 x86_64 arm32v6 aarch64; do
			build_package "$i"
		done
	fi
else
	while (( "$#" )); do
		build_package "$1"
		shift
	done
fi
