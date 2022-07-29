#!/bin/sh
podman build -t wonderful .
podman run -it -v $(pwd):/wf wonderful bash
