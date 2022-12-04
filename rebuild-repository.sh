#!/bin/sh
podman build -t wonderful-x86_64 .
podman run -i -v $(pwd):/wf wonderful-x86_64 su -c "cd /wf/build/packages && ( rm wonderful.* ; repo-add wonderful.db.tar.gz *.pkg.tar* )" wfbuilder
