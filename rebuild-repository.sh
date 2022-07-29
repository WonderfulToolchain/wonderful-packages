#!/bin/sh
podman build -t wonderful .
podman run -i -v $(pwd):/wf wonderful su -c "cd /wf/build/packages && ( rm wonderful.* ; repo-add wonderful.db.tar.gz *.pkg.tar* )" wfbuilder
