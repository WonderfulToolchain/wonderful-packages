# SPDX-License-Identifier: Zlib
#
# Copyright (c) 2023 Antonio Niño Díaz
# Copyright (c) 2023 Adrian "asie" Siekierka

# Base image with common build tools
# ==================================

FROM ubuntu:24.04 AS wonderful-base

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ca-certificates git make nodejs

RUN mkdir -p /opt/wonderful/
ADD https://wonderful.asie.pl/bootstrap/wf-bootstrap-x86_64.tar.gz /opt/wonderful/
RUN cd /opt/wonderful/ && \
    tar xzvf wf-bootstrap-x86_64.tar.gz && \
    rm wf-bootstrap-x86_64.tar.gz

ENV PATH /opt/wonderful/bin:$PATH

# TODO: This is a workaround for pacman that generates the file /etc/mtab. Maybe
# there is a better way to fix it.
RUN cd etc && \
    ln -sf ../proc/self/mounts mtab

RUN wf-pacman -Syu --noconfirm && \
    wf-pacman -S --noconfirm wonderful-base wf-tools

# Targets
# =======

FROM wonderful-base AS wonderful-wswan

ENV PATH /opt/wonderful/toolchain/gcc-ia16-elf/bin:$PATH

RUN wf-pacman -Syu --noconfirm && \
    wf-pacman -S --noconfirm target-wswan wf-lzsa wf-superfamiconv
