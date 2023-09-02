# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

#!/bin/sh
ROOT_DIR=$(pwd)

for i in `ls build/packages/linux/`; do
	if [ "$i" != "x86_64" ]; then
		cp build/packages/linux/x86_64/*-any.pkg.* build/packages/linux/"$i"/
	fi

	pushd containers/x86_64
	podman build -t wonderful-x86_64 .
	podman run -i -v "$ROOT_DIR":/wf wonderful-x86_64 su -c "cd /wf/build/packages/linux/"$i" && ( rm wonderful.* ; repo-add wonderful.db.tar.gz *.pkg.tar* )" wfbuilder
	popd
done
