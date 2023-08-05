from .magic import line_magic, arg

from iot_device import Config    # pylint: disable=import-error

@line_magic
def discover_magic(kernel, _):
    "Discover available microcontrollers"
    devices = kernel.registry.devices()
    if devices:
        kernel.print("{:15} {:20} {:7} {}\n".format(
            "Hostname", "Projects", "Con", "UID"))  
        for dev in devices:
            kernel.print("{:15} {:20} {:7} {}\n".format(
                dev.name, ', '.join(dev.projects), dev.connection, dev.uid))
    else:
        kernel.print("Found no devices")


@arg('hostname', help="hostname (from $host_dir/base/hosts.py) or device UID")
@line_magic
def connect_magic(kernel, args):
    "Connect to microcontroller"
    uid = Config.hostname2uid(args.hostname)
    if not uid: uid = args.hostname
    dev = kernel.registry.get_device(uid)
    if dev:
        kernel.device = dev
        kernel.print(f"Connected to {dev.name} with projects [{', '.join(dev.projects)}] @ {dev.address}\n")
    else:
        kernel.error(f"Device not available: '{args.hostname}'")