# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from .package import PackageBinaryCache
import os
from pathlib import Path
import shlex
import subprocess
from tqdm import tqdm

def clean_custom_keys(kwargs):
    for key in ["skip_package_sync", "as_root"]:
        if key in kwargs:
            del kwargs[key]

class Environment:
    def __init__(self, os, arch, root):
        self.os = os
        self.arch = arch
        self.root = Path(root)
        self.path = f"{os}/{arch}"
        self.package_cache = PackageBinaryCache(self.path)

class UnsupportedEnvironment(Environment):
    def __init__(self, os, arch):
        super().__init__(os, arch, "")

    def run(self, args, **kwargs):
        raise Exception(f"unsupported os/arch: {os}/{arch}")

class NativeWindowsEnvironment(Environment):
    def __init__(self, arch):
        super().__init__("windows", arch, os.getcwd())

    def run(self, args, **kwargs):
        # kwargs["shell"] = True
        clean_custom_keys(kwargs)
        return subprocess.run(["sh", "-c", " ".join(args)], **kwargs)
        
class NativeLinuxEnvironment(Environment):
    def __init__(self, arch):
        super().__init__("linux", arch, os.getcwd())

    def run(self, args, **kwargs):
        clean_custom_keys(kwargs)
        return subprocess.run(args, user="wfbuilder", **kwargs)
        
class ContainerEnvironment(Environment):
    def __init__(self, os, arch, container_name, user, shell, pacman):
        super().__init__(os, arch, "/wf")
        self.container_name = container_name
        self.container_built = False
        self.user = user
        self.shell = shell
        self.pacman = pacman

    def run(self, args, **kwargs):
        if not self.container_built:
            # run synchronously
            tqdm.write(f"Updating {self.container_name} container...")
            arch = self.arch
            if arch.startswith("arm"):
                arch = "arm"
            subprocess.run(f"podman build --arch {arch} -t wonderful-{self.container_name} -f containers/{self.container_name}/Containerfile .", shell=True, check=True,
                stdout=subprocess.DEVNULL)
            self.container_built = True
        cwd = os.getcwd()
        cmd = " ".join(args)
        if self.user is not None:
            cmd = "su -c '" + cmd + "'"
            if not ("as_root" in kwargs and kwargs["as_root"]):
                cmd = cmd + " " + self.user
        if not ("skip_package_sync" in kwargs and kwargs["skip_package_sync"]):
            cmd = self.pacman + " -Syu && " + cmd
        clean_custom_keys(kwargs)
        return subprocess.run(["podman", "run", "-i", "-v", f"{cwd}:/wf", f"wonderful-{self.container_name}", self.shell, "-c", cmd], **kwargs)

class ContainerLinuxEnvironment(ContainerEnvironment):
    def __init__(self, arch, container_name):
        super().__init__("linux", arch, container_name, "wfbuilder", "sh", "pacman")

class ContainerWindowsEnvironment(ContainerEnvironment):
    def __init__(self, arch, container_name):
        super().__init__("windows", arch, container_name, None, "msys2", "/opt/wonderful/bin/wf-pacman.exe")
