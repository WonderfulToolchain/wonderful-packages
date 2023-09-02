# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

import shutil
import urllib.request

def download_file(url, dest):
    with urllib.request.urlopen(url) as response, open(dest, 'wb') as f:
        shutil.copyfileobj(response, f)
