# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from pathlib import Path
import shutil
from termcolor import colored
from tqdm import tqdm

def cmd_build_bootstrap(ctx, args):
    targets = args.targets or ctx.all_known_environments
    for target, env in tqdm(ctx.environments.items()):
        if target not in targets:
            continue
        tqdm.write(colored(f"[*] Building bootstrap for {target}...", attrs=["bold"]))

        run_args = ["rm", "-r", f"/wf/build/bootstrap/*-{env.container_name}.tar.gz", ";",
                "mkdir", "-p", "/wf/build/bootstrap", "&&",
                "sudo", "pacman", "-Syu", "&&",
                "sudo", "pacman", "-S", "--noconfirm", "wf-pacman", "&&",
                "cd", "/opt/wonderful", "&&",
                "rm", "-r", "pacman/cache", "&&",
                "rm", "pacman/pacman.log", "&&",
                "tar", "czvf", f"/wf/build/bootstrap/wf-bootstrap-{env.container_name}.tar.gz", "."]
        
        result = env.run(run_args, check=True, skip_package_sync=True, as_root=True)

