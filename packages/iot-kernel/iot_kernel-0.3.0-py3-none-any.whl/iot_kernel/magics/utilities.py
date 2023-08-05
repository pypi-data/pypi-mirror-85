from .magic import line_magic, arg, LINE_MAGIC
from ..kernel_logger import logger

from iot_device import Config
import logging


@arg('-v', '--verbose', action='store_true', help="also list hosts defined in $host_dir/base/hosts.py")
@line_magic
def config_magic(kernel, args):
    """Show kernel configuration and hosts
Change configuration defaults in $IOT49/mcu/base/config.py and 
assign host names in $IOT49/mcu/base/hosts.py.

Sample config.py:
    password = '(*jfsdlafj&^*(5))'
    server_port = 8769

Sample hosts.py:
    hosts["30:ae:a4:12:34:28"] = { 'name': 'demo-wifi' }
    hosts["3e:1c:dc:01:0a:fc"] = { 
        'name': 'demo', 
        'projects': ['base', 'stdlib', 'my_app'] }
"""
    kernel.print("{:15} {:20} {}\n\n".format("Name", "Value", "Documentation"))
    for k, v in Config.config().items():
        skip = [ 'password', 'hosts', 'uid', 'wifi_ssid', 'wifi_pwd', 'sys' ]
        if any(x in k for x in skip):
            continue
        v = str(v)
        if len(v) > 20:  v = ".." + v[-16:]
        kernel.print("{:15} {:20} {}\n".format(k, v, Config.getdoc(k)))
    if not args.verbose:
        return
    kernel.print("\n\n{:15} {:20} {}\n".format("Hostname", "Projects", "UID"))
    hosts = Config.get_config(file='hosts.py').get('hosts', {})
    for k, v in hosts.items():
        name = v
        if isinstance(v, dict):
            name = v.get('name')
            projects = v.get('projects', '')
        kernel.print("{:15} {:20} {}\n".format(name, ', '.join(projects), k))


@arg('-v', '--verbose', action='store_true', help="Show detailed help for each line magic.")
@line_magic
def lsmagic_magic(kernel, args):
    """List all magic functions."""
    if args.verbose:
        for k, v in sorted(LINE_MAGIC.items()):
            if not v[1]: continue
            kernel.print(f"MAGIC %{k} {'-'*(70-len(k))}\n")
            v[0](kernel, "-h")
            kernel.print("\n\n")
        return

    kernel.print("Line Magic:    -h shows help (e.g. %discover -h)\n")
    for k, v in sorted(LINE_MAGIC.items()):
        if not v[1]: continue
        kernel.print("  %{:10s}  {}\n".format(k, v[1]))
    kernel.print("  {:11s}  {}\n".format('!', "Pass line to bash shell for evaluation."))
    kernel.print("\nCell Magic:\n")
    kernel.print("  {:11s}  {}\n".format('%%connect', "Evaluate code sequentially on named devices."))
    kernel.print("  {:11s}  {}\n".format('', "--host executes on host (iPython)."))
    kernel.print("  {:11s}  {}\n".format('', "Option -q supresses device name in output."))
    kernel.print("  {:11s}  {}\n".format('%%host', "Pass cell to host (iPython) for evaluation."))
    kernel.print("  {:11s}  {}\n".format('%%bash', "Pass cell to the bash shell for evaluation."))


@arg('level', nargs='?', default='INFO', const='INFO', choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="logging levels")
@arg('logger', nargs='?', help="name of logger to apply level to")
@line_magic
def loglevel_magic(kernel, args):
    """Set logging level.
Without arguments lists name and level of all available loggers.
    """
    if args.logger:
        logging.getLogger(args.logger).setLevel(args.level)
        kernel.print(f"Logger {args.logger} level set to {args.level}\n")
    else:
        fmt = "{:30}  {}\n"
        kernel.print(fmt.format('Logger', 'Level'))
        kernel.print('\n')
        for k, v in logging.root.manager.loggerDict.items():
            s = str(v)
            if '(' in s:
                kernel.print(fmt.format(k, s[s.find("(")+1:s.find(")")]))
    # set global level
    # logging.basicConfig(level=args.level)
    # logger.setLevel(args.level)
    # logger.info("set logger level to '{}'".format(args.level))
