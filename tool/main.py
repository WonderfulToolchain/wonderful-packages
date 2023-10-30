# SPDX-License-Identifier: MIT
#
# SPDX-FileContributor: Adrian "asie" Siekierka, 2023

from .cmd.build import cmd_build
from .cmd.build_bootstrap import cmd_build_bootstrap
from .cmd.copy_anyarchs import cmd_copy_anyarchs
from .cmd.mirror import cmd_mirror
from .environment import NativeLinuxEnvironment, NativeWindowsEnvironment, ContainerLinuxEnvironment
import addict
import argparse
import platform

ctx = addict.Dict({
    "all_known_environments": [
        "linux/x86_64",
        "linux/aarch64",
        "linux/armv6h",
        "windows/x86_64"
    ],
    "environments": {},
    "preferred_environment": None,
    "repository_http_root": "https://wonderful.asie.pl/packages/rolling"
})

def add_environment(env, is_fastest):
    if env.path not in ctx.all_known_environments:
        raise Exception(f"environment not in all_known: {env.path}")
    ctx.environments[env.path] = env
    if is_fastest:
        ctx.preferred_environment = env

if platform.system() == "Windows" or platform.system().startswith("MSYS_NT"):
    if platform.machine() == "AMD64" or platform.machine() == "x86_64":
        add_environment(NativeWindowsEnvironment("x86_64"), True)
elif platform.system() == "Linux":
    add_environment(ContainerLinuxEnvironment("x86_64", "x86_64"), platform.machine() == "AMD64" or platform.machine() == "x86_64")
    add_environment(ContainerLinuxEnvironment("aarch64", "aarch64"), not (platform.machine() == "AMD64" or platform.machine() == "x86_64"))
    add_environment(ContainerLinuxEnvironment("armv6h", "arm32v6"), False)

if ctx.preferred_environment is None:
    raise Exception("unsupported platform: " + platform.system() + "/" + platform.machine())
ctx.platform = ctx.preferred_environment.path.split("/")[0]

argp = argparse.ArgumentParser(prog='pkgtool')
subparsers = argp.add_subparsers(title='subcommands', required=True,
                                 description='Valid subcommands')

argp_mirror = subparsers.add_parser('mirror', help='Synchronize a local copy of the repository.')
argp_mirror.add_argument('targets', metavar='target', type=str, nargs='*', help='Requested targets.')
argp_mirror.add_argument('-c', '--clean', dest='clean', action='store_true', help='Remove unused package files.')
argp_mirror.add_argument('-f', '--force', dest='force', action='store_true', help='Download already existing package files. Use sparingly.')
argp_mirror.add_argument('-a', '--all', dest='all', action='store_true', help='Download all targets, including ones not buildable on this machine. [targets] takes priority.')
argp_mirror.set_defaults(func=cmd_mirror)

argp_build = subparsers.add_parser('build', help='Build packages.')
argp_build.add_argument('packages', metavar='package', type=str, nargs='*', help='Requested packages. Format: package_name[@target1[,target2...]]')
argp_build.add_argument('-k', '--keep', dest='keep', action='store_true', help='Keep the old version of the package.')
argp_build.set_defaults(func=cmd_build)

argp_build_bootstrap = subparsers.add_parser('build-bootstrap', help='Build bootstraps.')
argp_build_bootstrap.add_argument('targets', metavar='target', type=str, nargs='*', help='Requested targets.')
argp_build_bootstrap.set_defaults(func=cmd_build_bootstrap)

argp_copy_anyarchs = subparsers.add_parser('copy-anyarchs', help='Copy any-architecture packages.')
argp_copy_anyarchs.add_argument('targets', metavar='target', type=str, nargs='*', help='Source, followed by destination targets.')
argp_copy_anyarchs.add_argument('-k', '--keep', dest='keep', action='store_true', help='Keep the old versions of the packages.')
argp_copy_anyarchs.set_defaults(func=cmd_copy_anyarchs)

args = argp.parse_args()
args.func(ctx, args)
