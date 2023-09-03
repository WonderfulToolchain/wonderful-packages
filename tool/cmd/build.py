# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from .mirror import clean_unused_packages
from ..package import PackageBinaryCache, PackageSourceCache, resolve_package_path
from pathlib import Path
import re
import shutil
from termcolor import colored
from tqdm import tqdm

def build_package(name, targets):
    pass

def parse_package_reference(name, all_targets):
    if "@" in name:
        name, named_targets = name.split("@")
        filtered_targets = []
        for target in all_targets:
            if target in named_targets:
                filtered_targets.append(target)
                continue
            if any([subtarget in named_targets for subtarget in target.split("/")]):
                filtered_targets.append(target)
                continue
        return name, filtered_targets
    else:
        return name, all_targets

def cmd_build(ctx, args):
    all_targets = list(ctx.environments.keys())
    package_caches = {}
    package_pairs = []
    source_cache = PackageSourceCache(ctx.preferred_environment)
    repo_updates = {}

    tqdm.write(colored(f"[*] Preparing...", attrs=["bold"]))
    for target in all_targets:
        package_caches[target] = PackageBinaryCache(target)
        if package_caches[target].init_db():
            repo_updates[target] = []

    for name, targets in tqdm([parse_package_reference(package, all_targets) for package in args.packages]):
        if name not in source_cache.get_package_names():
            tqdm.write(colored(f"[*] {package} not found for {target}, skipping...", attrs=["bold"]))
            continue
        srcinfo = source_cache.get_package_by_name(name, targets[0])
        if "any" in srcinfo["arch"]:
            package_pairs.append((name, "any"))
        else:
            for target in targets:
                package_pairs.append((name, target))

    for package, target in tqdm(package_pairs):
        tqdm.write(colored(f"[*] Building {package} for {target}...", attrs=["bold"]))
        env = ctx.preferred_environment if target == "any" else ctx.environments[target]
        result = env.run(["cd", str(env.root / str(resolve_package_path(package, env.path))), "&&", "makepkg", "-C", "--clean", "--syncdeps", "--force", "--noconfirm", "--skippgpcheck", package], check=True)
        package_names = source_cache.get_package_by_name(package, target)["names"]

        for package_name in package_names:
            repo_updates[env.path].append(package_name)
        if target == "any":
            # This is a little broken - it will copy all "any-files" that begin with the same prefix.
            tqdm.write("Propagating any-package...")
            src_dir = Path(f"build/packages/{env.path}")
            for package_name in package_names:
                for target in ctx.all_known_environments:
                    if target == env.path:
                        continue
                    if target not in repo_updates:
                        continue
                    repo_updates[target].append(package_name)
                    dest_dir = Path(f"build/packages/{target}")
                    dest_dir.mkdir(parents=True, exist_ok=True)
                    matcher = re.compile(f"^{package_name}-[0-9]")
                    for src_file in src_dir.glob("*"):
                        if src_file.is_file() and matcher.match(src_file.name) and "-any.pkg.tar." in src_file.name:
                            tqdm.write("-> " + str(dest_dir / src_file.name))
                            shutil.copy(src_file, dest_dir / src_file.name)

    for target, packages in tqdm(filter(lambda x: len(x[1]) > 0, repo_updates.items())):
        target_dir = Path(f"build/packages/{target}")
        if not (target_dir / "wonderful.db.tar.gz").exists():
            tqdm.write(colored(f"[*] Repository not found for {target}, skipping...", attrs=["bold"]))
            continue
        tqdm.write(colored(f"[*] Updating repository for {target}...", attrs=["bold"]))
        env = ctx.preferred_environment

        old_filenames = list([p["filename"] for p in package_caches[target].get_packages().values()])

        run_args = ["cd", str(env.root / str(target_dir)), "&&", "repo-add"]
        if not args.keep:
            run_args.append("-R")
        run_args.append("wonderful.db.tar.gz")
        added_files = {}
        for package in packages:
            # At any given point, there's going to be either one matching package file (re-building same package)
            # or multiple (upgrading package).
            # This assumption is a little broken - currently, it will match all files that begin with the same prefix.
            matching_filenames = []
            matcher = re.compile(f"^{package}-[0-9]")
            for target_file in target_dir.glob("*"):
                if target_file.is_file() and matcher.match(target_file.name):
                    matching_filenames.append(target_file.name)
            if len(matching_filenames) > 1:
                matching_filenames = list(filter(lambda x: x not in old_filenames, matching_filenames))
            for fn in matching_filenames:
                if fn not in added_files:
                    run_args.append(fn)
                    added_files[fn] = True
        result = env.run(run_args, check=True, skip_package_sync=True)
