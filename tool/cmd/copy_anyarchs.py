# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from ..package import PackageBinaryCache
from pathlib import Path
from termcolor import colored
from tqdm import tqdm
import shutil

def cmd_copy_anyarchs(ctx, args):
    dest_targets = args.targets
    src_target = dest_targets.pop(0)
    src_package_cache = PackageBinaryCache(src_target)

    print(colored("[*] Copying requested packages...", attrs=["bold"]))
    
    src_target_path = Path(f"build/packages/{src_target}")
    for target in dest_targets:
        target_path = Path(f"build/packages/{target}")

        env = ctx.preferred_environment
        run_args = ["cd", str(env.root / str(target_path)), "&&", "repo-add"]
        if not args.keep:
            run_args.append("-R")
        run_args.append("wonderful.db.tar.gz")

        for package_name, package in src_package_cache.get_packages().items():
            if package['arch'][0] != "any":
                continue
            if ":" in package['filename']:
                print(f"Skipping {package['filename']} - contains colon on Windows")
                continue
            src = src_target_path / package['filename']
            dest = target_path / package['filename']
            if dest.exists():
                continue
            shutil.copy(src, dest)
            run_args.append(package['filename'])

        result = env.run(run_args, check=True, skip_package_sync=True)
            



