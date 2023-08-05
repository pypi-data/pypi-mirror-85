from .magic import line_magic, arg

import time

@arg("-q", "--quiet", action="store_true", help="suppress terminal output")
@line_magic
def softreset_magic(kernel, args):
    """Reset microcontroller. Similar to pressing the reset button.
Purges all variables and releases all devices (e.g. I2C, UART, ...).

Example:
    a = 5
    %softreset
    print(a)   # NameError: name 'a' isn't defined
"""
    with kernel.device as repl:
        repl.softreset()
    if args.quiet:
        return
    kernel.print("\n")
    kernel.print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", 'red', 'on_cyan')
    kernel.print("!!!!!      softreset      !!!!!\n", 'red', 'on_cyan')
    kernel.print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n", 'red', 'on_cyan')
    kernel.print("\n")


@line_magic
def uid_magic(kernel, _):
    """Print UID of microcontroller.
Derived from machine.unique_id() (MicroPython) or 
microcontroller.cpu.uid (CircuitPython)."""
    kernel.print(f"{kernel.device.uid}\n")


@line_magic
def name_magic(kernel, _):
    """Name of currently connected microcontroller.
Define names in $host_dir/base/hosts.py"""
    kernel.print(f"{kernel.device.name}\n")


@line_magic
def synctime_magic(kernel, _):
    "Synchronize microcontroller time to host"
    with kernel.device as repl:
        repl.sync_time()


@line_magic
def gettime_magic(kernel, _):
    "Query microcontroller time"
    with kernel.device as repl:
        t = time.mktime(repl.get_time())
    kernel.print(f"{time.strftime('%Y-%b-%d %H:%M:%S', time.localtime(t))}\n")
    # kernel.print(f"{time.strftime('%Y-%b-%d %H:%M:%S', time.gmtime(t))}\n")
