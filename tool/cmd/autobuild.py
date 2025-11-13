# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from .build import cmd_build
from pathlib import Path
from termcolor import colored
from tqdm import tqdm
from types import SimpleNamespace
import os, subprocess, sys

def is_valid_package(pkgname):
    return (Path("packages") / pkgname / "PKGBUILD").exists()

def rev_get_current():
    result = subprocess.run(["git", "rev-parse", "HEAD"], check=True, stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8").strip()

def rev_get_changed_files(commit_from, commit_to):
    result = subprocess.run(["git", "log", "--name-only", "--pretty=", commit_from + ".." + commit_to], check=True, stdout=subprocess.PIPE)
    return [x.strip() for x in result.stdout.decode("utf-8").split("\n")]

def cmd_autobuild(ctx, args):
    autobuild_rev_file = Path("autobuild.rev")

    def rev_get_previous():
        with open(autobuild_rev_file, "r") as f:
            return f.read().strip()

    def rev_update():
        with open(autobuild_rev_file, "w") as f:
            f.write(rev_get_current())

    if not autobuild_rev_file.exists():
        print(colored("[*] Initializing new autobuild instance...", attrs=["bold"]))
        rev_update()
        return
    
    print(colored("[*] Checking for changes...", attrs=["bold"]))
    previous_rev = rev_get_previous()
    current_rev = rev_get_current()
    if previous_rev == current_rev:
        print("No changes found.")
        sys.exit(55)
        return

    changed_packages = [x.split("/")[1] for x in filter(lambda x: x.startswith("packages/"), rev_get_changed_files(previous_rev, current_rev))]
    visited_packages = set()
    unique_changed_packages = [x for x in changed_packages if x not in visited_packages and not visited_packages.add(x) and is_valid_package(x)]
    print(colored(f"[*] Found {len(unique_changed_packages)} changed packages.", attrs=["bold"]))

    if not args.skip:
        cmd_build(ctx, SimpleNamespace({"packages": unique_changed_packages, "force": False, "keep": False}))
     
    print(colored(f"[*] Building complete!", attrs=["bold"]))    
    rev_update()


