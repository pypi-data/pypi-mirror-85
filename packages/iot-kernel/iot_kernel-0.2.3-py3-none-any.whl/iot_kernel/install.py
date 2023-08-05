import argparse
import json
import os
import sys
import shutil

from jupyter_client.kernelspec import KernelSpecManager   # pylint: disable=import-error
from IPython.utils.tempdir import TemporaryDirectory      # pylint: disable=import-error

kernel_json = {
    "argv": [sys.executable, "-m", "iot_kernel", "-f", "{connection_file}"],
    "display_name": "IoT",
    "language": "text",
}


def install_my_kernel_spec(user=True, prefix=None):
    with TemporaryDirectory() as td:
        os.chmod(td, 0o755)  # Starts off as 700, not user readable
        with open(os.path.join(td, 'kernel.json'), 'w') as f:
            json.dump(kernel_json, f, sort_keys=True)
            
        # Copy logo
        import iot_kernel
        path = os.path.dirname(iot_kernel.__file__)
        print(f"Path: {path}")
        print(f"Install-dir: {os.getcwd()}")
        for f in [ 'logo-32x32.png', 'logo-64x64.png' ]:
            # not sure how to do this right
            for dir in [ 'images', '../images' ]:
                try:
                    shutil.copyfile(os.path.join(path, dir, f), os.path.join(td, f))
                    break
                except:
                    pass
        print('Installing Jupyter kernel spec')
        KernelSpecManager().install_kernel_spec(td, 'iot_kernel', user=user, prefix=prefix)


def _is_root():
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False  # assume not an admin on non-Unix platforms


def main(argv=None):
    parser = argparse.ArgumentParser(description='Install KernelSpec for IoT Kernel')
    prefix_locations = parser.add_mutually_exclusive_group()
    prefix_locations.add_argument('--user', action='store_true',
        help="Install to the per-user kernels registry. Default if not root.")
    prefix_locations.add_argument('--sys-prefix', action='store_true',
        help="Install to sys.prefix (e.g. a virtualenv or conda env)")
    prefix_locations.add_argument('--prefix',
        help="Install to the given prefix. "
             "Kernelspec will be installed in {PREFIX}/share/jupyter/kernels/",
             default=None)
    args = parser.parse_args(argv)

    user = False
    prefix = None
    if args.sys_prefix:
        prefix = sys.prefix
    elif args.prefix:
        prefix = args.prefix
    elif args.user or not _is_root():
        user = True

    install_my_kernel_spec(user=user, prefix=prefix)


if __name__ == '__main__':
    main()
