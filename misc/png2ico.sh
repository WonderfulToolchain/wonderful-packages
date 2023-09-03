#!/bin/bash
magick convert "$1" \
	-filter Point \
	\( -clone 0 -resize 64x64 \) \
	\( -clone 0 -resize 96x96 \) \
	\( -clone 0 -resize 128x128 \) \
	\( -clone 0 -resize 256x256 \) \
	-colors 256 "$2"
