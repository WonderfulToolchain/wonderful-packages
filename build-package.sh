#!/bin/sh
PKGNAME=${1##*/}
podman build -t wonderful .
podman run -i -v $(pwd):/wf wonderful su -c "cd /wf/packages/$PKGNAME && sudo pacman -Syu && makepkg -C --clean --syncdeps --force --noconfirm --skippgpcheck $PKGNAME" wfbuilder
