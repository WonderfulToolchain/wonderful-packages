# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

#!/bin/sh
PKGARCH=$1
ROOT_DIR=$(pwd)

podman build -t wonderful-"$PKGARCH" -f containers/"$PKGARCH"/Containerfile .
podman run -it -v "$ROOT_DIR":/wf wonderful-"$PKGARCH" bash
