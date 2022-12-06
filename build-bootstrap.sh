#!/bin/sh
PKGARCH=$1
ROOT_DIR=$(pwd)

pushd containers/"$PKGARCH"/
podman build -t wonderful-"$PKGARCH" .
podman run -i -v "$ROOT_DIR":/wf wonderful-"$PKGARCH" \
su -c "rm -r /wf/build/bootstrap/*-"$PKGARCH".tar.gz ; mkdir -p /wf/build/bootstrap && sudo pacman -Syu && sudo pacman -S --noconfirm wf-pacman && cd /opt/wonderful && rm -r pacman/cache && rm pacman/pacman.log && tar czvf /wf/build/bootstrap/wf-bootstrap-"$PKGARCH".tar.gz ."
popd
