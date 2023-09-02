# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from .cmd.mirror import cmd_mirror
from .environment import NativeLinuxEnvironment, NativeWindowsEnvironment, ContainerLinuxEnvironment
import addict
import argparse
import platform

ctx = addict.Dict({
    "environments": {},
    "preferred_environment": None,
    "repository_http_root": "https://wonderful.asie.pl/packages/rolling"
})

def add_environment(env, is_fastest):
    ctx.environments[env.path] = env
    if is_fastest:
        ctx.preferred_environment = env

if platform.system() == "Windows":
    if platform.machine() == "AMD64" or platform.machine() == "x86_64":
        add_environment(NativeWindowsEnvironment("x86_64"), True)
elif platform.system() == "Linux":
    add_environment(ContainerLinuxEnvironment("x86_64", "x86_64"), platform.machine() == "AMD64" or platform.machine() == "x86_64")
    add_environment(ContainerLinuxEnvironment("aarch64", "aarch64"), not (platform.machine() == "AMD64" or platform.machine() == "x86_64"))
    add_environment(ContainerLinuxEnvironment("armv6h", "arm32v6"), False)

if ctx.preferred_environment is None:
    raise Exception("unsupported platform: " + platform.system() + "/" + platform.machine())

argp = argparse.ArgumentParser(prog='pkgtool')
subparsers = argp.add_subparsers(title='subcommands', required=True,
                                 description='Valid subcommands')

argp_mirror = subparsers.add_parser('mirror', help='Synchronize a local copy of the repository.')
argp_mirror.add_argument('targets', metavar='N', type=str, nargs='*', help='Requested targets.')
argp_mirror.add_argument('-c', '--clean', dest='clean', action='store_true', help='Remove unused package files.')
argp_mirror.add_argument('-f', '--force', dest='force', action='store_true', help='Download already existing package files. Use sparingly.')
argp_mirror.set_defaults(func=cmd_mirror)

args = argp.parse_args()
args.func(ctx, args)
