# SPDX-License-Identifier: CC0-1.0
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

#!/bin/sh
ROOT_DIR=$(pwd)

for os in `ls build/packages/`; do
for i in `ls build/packages/"$os"/`; do
	if [ "$i" != "x86_64" ]; then
		cp build/packages/"$os"/x86_64/*-any.pkg.* build/packages/"$os"/"$i"/
	fi

	pushd containers/x86_64
	podman build -t wonderful-x86_64 .
	podman run -i -v "$ROOT_DIR":/wf wonderful-x86_64 su -c "cd /wf/build/packages/"$os"/"$i" && ( rm wonderful.* ; repo-add wonderful.db.tar.gz *.pkg.tar* )" wfbuilder
	popd
done
done
