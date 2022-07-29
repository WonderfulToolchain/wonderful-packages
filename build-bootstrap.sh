#!/bin/sh
PKGNAME=${1##*/}
podman build -t wonderful .
podman run -i -v $(pwd):/wf wonderful \
su -c "rm -r /wf/build/bootstrap ; mkdir -p /wf/build/bootstrap && sudo pacman -Syu && sudo pacman -S --noconfirm wf-pacman && cd /opt/wonderful && rm -r pacman/cache && rm pacman/pacman.log && tar czvf /wf/build/bootstrap/wf-bootstrap-x86_64.tar.gz ."
