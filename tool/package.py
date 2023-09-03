# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from pathlib import Path
import re
import subprocess
import tarfile

def resolve_package_path(name, target):
    target_parts = target.split("/")
    package_path = Path("packages") / name
    for candidate_path in [package_path, package_path / target_parts[0], package_path / "other", package_path / "any"]:
        if (candidate_path / "PKGBUILD").exists():
            return candidate_path
    return None

# Binary (.db.tar.gz) package metadata cache.

bin_desc_key = re.compile(r"^%([A-Z0-9_]+)%$")

def postprocess_package_keys(package, extra_keys=[]):
    for key in extra_keys + ["arch", "groups", "depends", "makedepends", "checkdepends", "optdepends", "provides", "conflicts", "replaces"]:
        if key in package:
            package[key] = package[key].split("\n")
        else:
            package[key] = []

class PackageBinaryCache:
    def __init__(self, target):
        self.__db_loc = f"build/packages/{target}/wonderful.db.tar.gz"
        self.__files_loc = f"build/packages/{target}/wonderful.files.tar.gz"
        self.clear()

    def init_db(self, force=False):
        if self.packages is not None and not force:
            return True
        if not Path(self.__db_loc).exists():
            return False
        self.packages = {}
        with tarfile.open(self.__db_loc, "r") as db_tar:
            for file in db_tar.getmembers():
                if file.isreg() and file.name.endswith("desc"):
                    f = db_tar.extractfile(file)
                    package = {}
                    current_key = None
                    for rawline in f:
                        line = rawline.decode("utf-8").strip()
                        key_match = bin_desc_key.match(line)
                        if key_match is not None:
                            current_key = key_match.group(1).lower()
                        elif len(line) > 0:
                            if current_key not in package:
                                package[current_key] = line
                            else:
                                package[current_key] = package[current_key] + "\n" + line
                    postprocess_package_keys(package)
                    self.packages[package["name"]] = package
        return True

    def clear(self):
        self.packages = None

    def get_package_names(self):
        if not self.init_db():
            return []
        return self.packages.keys()

    def get_package_by_name(self, name):
        self.init_db()
        return self.packages[name]

    def get_packages(self):
        if not self.init_db():
            return {}
        return self.packages

# Source (PKGBUILD) package metadata cache.

class PackageSourceCache:
    def __init__(self, env):
        self.env = env
        self.clear()

    def clear(self):
        self.packages = {}
        self.package_names = None
 
    def get_package_names(self):
        if self.package_names is None:
            self.package_names = list([p.name for p in filter(lambda p: p.is_dir(), Path("packages").glob("*"))])
        return self.package_names

    def get_package_by_path(self, name, path):
        if path not in self.packages:
            result = self.env.run(["cd", str(self.env.root / str(path)), "&&", "makepkg", "--printsrcinfo"], check=True, stdout=subprocess.PIPE, skip_package_sync=True)
            package = {}
            for line in result.stdout.decode('utf-8').splitlines():
                parts = list([l.strip() for l in line.strip().split("=", maxsplit=1)])
                if len(parts) == 2:
                    if parts[0] not in package:
                        package[parts[0]] = parts[1]
                    else:
                        package[parts[0]] = package[parts[0]] + "\n" + parts[1]
            # TODO: Support pkgnames != pkgbases.
            if "pkgbase" in package:
                package["name"] = package["pkgbase"]
                del package["pkgbase"]
            if "pkgname" in package:
                package["names"] = package["pkgname"]
                del package["pkgname"]
            if "pkgver" in package:
                package["version"] = package["pkgver"]
                del package["pkgver"]
            else:
                package["version"] = ""
            if "pkgrel" in package:
                package["version"] += "-" + package["pkgrel"]
                del package["pkgrel"]
            if "pkgdesc" in package:
                package["desc"] = package["pkgdesc"]
                del package["pkgdesc"]

            postprocess_package_keys(package, extra_keys=["names"])
            self.packages[path] = package
        return self.packages[path]

    def get_package_by_name(self, name, target):
        return self.get_package_by_path(name, resolve_package_path(name, target))
