from .magic import line_magic, arg
from ..output import Output

from iot_device import Config
from iot_device import DeviceError
from iot_device import cd
import contextlib
import os
import sys


@arg("destination", help="Name of destination file/directory")
@arg("sources", nargs="+", help="Names of source files")
@line_magic
def cp_magic(kernel, args):
    """Copy files between host and microcontroller.
File/directory names starting with colon (:) refer to the microcontroller.
Path are relative to $host_dir on the host and root (/) on the microcontroller.

CircuitPython: By default, CircuitPython disables writing to the 
               microcontroller filesystem. To enable, add the line 

                   storage.remount("/", readonly=False)" 
                   
               to boot.py.

Examples:
    # copy file from host microcontroller, changing the name
    %cp a.txt :b.txt

    # same, filename on microcontroller is same as on host (a.txt)
    %cp a.txt :

    # copy several files to microcontroller
    %cp a.txt b.txt :/

    # copy files to subfolder
    %mkdirs x/y
    %cp a.txt b.txt :x/y/

    # copy file from microcontroller to host
    %cp :a.txt :b.txt ./
    """
    # see https://github.com/micropython/micropython/blob/master/tools/pyboard.py
    def fname_remote(src):
        if src.startswith(":"):
            src = src[1:]
        return src

    def fname_cp_dest(src, dest):
        src = src.rsplit("/", 1)[-1]
        if dest is None or dest == "":
            dest = src
        elif dest == ".":
            dest = "./" + src
        elif dest.endswith("/"):
            dest += src
        return dest

    srcs = args.sources
    dest = args.destination
    with kernel.device as repl:
        if srcs[0].startswith("./") or dest.startswith(":"):
            xfer = repl.fput
            dest = fname_remote(dest)
        else:
            xfer = repl.fget
        for src in srcs:
            src = fname_remote(src)
            dst = fname_cp_dest(src, dest)
            xfer(src, dst)
            if False:
                try:
                    xfer(src, dst)
                except DeviceError as re:
                    kernel.error(f"Error in cp {src} {dst}\n")
                    kernel.error(f"\n{re}\n")
                except FileNotFoundError as fne:
                    kernel.error(f"\n{fne}\n")


@arg("path", help="path to file")
@line_magic
def cat_magic(kernel, args):
    "Print contents of named file on microcontroller"
    with kernel.device as repl:
        repl.cat(Output(kernel), args.path)
    kernel.print('\n')


@arg("path", help="path to file/directory")
@arg('-r', '--recursive', action='store_true', help="recursively delete content in directories")
@line_magic
def rm_magic(kernel, args):
    """Delete files/directories on microcontroller"""
    with kernel.device as repl:
        res = repl.rm_rf(args.path, args.recursive)
        if not res:
            kernel.error(f"***** '{args.path}' not deleted")


@arg("path")
@line_magic
def mkdirs_magic(kernel, args):
    """Create all directories specified by the path, if they do not exist
Example:
    # create /a and subfolder /a/b on microcontroller
    %mkdirs a/b
"""
    with kernel.device as repl:
        if not repl.makedirs(args.path):
            kernel.error("Directories not created")