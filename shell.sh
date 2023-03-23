# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

#!/bin/sh
PKGARCH=$1
ROOT_DIR=$(pwd)

pushd containers/"$PKGARCH"/
podman build -t wonderful-"$PKGARCH" .
podman run -it -v "$ROOT_DIR":/wf wonderful-"$PKGARCH" bash
popd
