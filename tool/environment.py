# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from .package import PackageBinaryCache
import os
import shlex
import subprocess
from tqdm import tqdm

class Environment:
    def __init__(self, os, arch):
        self.os = os
        self.arch = arch
        self.path = f"{os}/{arch}"
        self.package_cache = PackageBinaryCache(self.path)

class UnsupportedEnvironment(Environment):
    def __init__(self, os, arch):
        super().__init__(os, arch)

    def run(self, args, **kwargs):
        raise Exception(f"unsupported os/arch: {os}/{arch}")

class NativeWindowsEnvironment(Environment):
    def __init__(self, arch):
        super().__init__("windows", arch)

    def run(self, args, **kwargs):
        return subprocess.run(args, **kwargs)
        
class NativeLinuxEnvironment(Environment):
    def __init__(self, arch):
        super().__init__("linux", arch)

    def run(self, args, **kwargs):
        return subprocess.run(args, user="wfbuilder", **kwargs)
        
class ContainerLinuxEnvironment(Environment):
    def __init__(self, arch, container_name):
        super().__init__("linux", arch)
        self.container_name = container_name
        self.container_built = False

    def run(self, args, **kwargs):
        if not self.container_built:
            # run synchronously
            tqdm.write(f"Updating {self.container_name} container...")
            subprocess.run(f"podman build -t wonderful-{self.container_name} .", shell=True, check=True,
                stdout=subprocess.DEVNULL,
                cwd=f"containers/{self.container_name}")
            self.container_built = True
        cwd = os.getcwd()
        cmd = " ".join(args)
        cmd = "su -c '" + cmd + "'"
        if not ("as_root" in kwargs and kwargs["as_root"]):
            cmd = cmd + " wfbuilder"
        if not ("skip_package_sync" in kwargs and kwargs["skip_package_sync"]):
            cmd = "pacman -Syu && " + cmd
        for key in ["skip_package_sync", "as_root"]:
            if key in kwargs:
                del kwargs[key]
        return subprocess.run(["podman", "run", "-i", "-v", f"{cwd}:/wf", f"wonderful-{self.container_name}", "sh", "-c", cmd], **kwargs)
