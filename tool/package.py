# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

import re
import tarfile

bin_desc_key = re.compile(r"^%([A-Z0-9_]+)%$")

class PackageBinaryCache:
    def __init__(self, target):
        self.__db_loc = f"build/packages/{target}/wonderful.db.tar.gz"
        self.__files_loc = f"build/packages/{target}/wonderful.files.tar.gz"
        self.packages = None

    def init_db(self, force=False):
        if self.packages is not None and not force:
            return
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
                    for key in ["depends", "makedepends", "checkdepends", "optdepends", "provides", "conflicts", "replaces"]:
                        if key in package:
                            package[key] = package[key].split("\n")
                        else:
                            package[key] = []
                    self.packages[package["name"]] = package

    def get_packages(self):
        self.init_db()
        return self.packages
