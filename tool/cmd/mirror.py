# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from ..package import PackageBinaryCache
from ..util import download_file
from pathlib import Path
from termcolor import colored
from tqdm import tqdm

def clean_unused_packages(ctx, package_caches, file_list):
    print(colored("[*] Removing unused packages...", attrs=["bold"]))

    for target, package_cache in package_caches.items():
        target_path = Path(f"build/packages/{target}")
        for target_file in target_path.rglob('*'):
            if target_file.is_file() and not any([target_file.name.endswith(x) for x in [".db", ".db.tar.gz", ".files", ".files.tar.gz"]]):
                if target_file.resolve() not in file_list:
                    print(f"Removing {target_file.name}...")
                    target_file.unlink()

def cmd_mirror(ctx, args):
    targets = args.targets
    if targets is None or len(targets) == 0:
        if args.all:
            targets = ctx.all_known_environments
        else:
            targets = list(ctx.environments.keys())
    package_caches = {}

    print(colored("[*] Downloading repository databases...", attrs=["bold"]))

    for target in tqdm(targets):
        target_path = Path(f"build/packages/{target}")
        target_path.mkdir(parents=True, exist_ok=True)
        package_cache_valid = True

        for filename_dest_link in ["wonderful.db", "wonderful.files"]:
            tqdm.write(f"Downloading {filename_dest_link} for {target}...")
            filename_dest = filename_dest_link + ".tar.gz"
            path_dest = target_path / filename_dest
            path_dest_link = target_path / filename_dest_link

            path_dest.unlink(missing_ok=True)
            path_dest_link.unlink(missing_ok=True)

            try:
                download_file(f"{ctx.repository_http_root}/{target}/{filename_dest}", path_dest)
                path_dest_link.symlink_to(filename_dest, target_is_directory=False)
            except Exception as e:
                print(e)
                package_cache_valid = False

        if package_cache_valid:
            package_caches[target] = PackageBinaryCache(target)

    print(colored("[*] Building package file list...", attrs=["bold"]))
    file_list = {}
    download_file_list = {}
    
    for target, package_cache in package_caches.items():
        target_path = Path(f"build/packages/{target}")

        for package_name, package in package_cache.get_packages().items():
            if ctx.platform == "windows":
                if ":" in package['filename']:
                    print(f"Skipping {package['filename']} - contains colon on Windows")
                    continue
            url = f"{ctx.repository_http_root}/{target}/{package['filename']}"
            dest = target_path / package['filename']
            file_list[dest.resolve()] = True
            if not dest.exists() or args.force:
                download_file_list[url] = dest

    print(colored("[*] Downloading requested packages...", attrs=["bold"]))
    
    for url, dest in tqdm(download_file_list.items()):
        tqdm.write(f"Downloading {dest.name}...")
        download_file(url, dest)

    if args.clean:
        clean_unused_packages(ctx, package_caches, file_list)



