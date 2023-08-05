from .magic import line_magic, arg
from .mini_pip import install
from iot_device import Config
import upip
import os, sys

"""
Requires 

    micropython-cpython-upip

Install (from Jupyter):

!pip install micropython-cpython-upip

%%host

# patch ...

import os
import upip

file = os.path.expanduser(upip.__file__)
with open(file) as f:
    s = f.read()

s = s.replace("outf.write(file_buf, sz)", "outf.write(file_buf)")
s = s.replace("sz = gc.mem_free() + gc.mem_alloc()", "sz = 100000")

with open(file, "w") as f:
    f.write(s)
"""

@arg("-l", "--lib", default='lib', help="target directory in $host_dir/<project>")
@arg("-p", "--project", default='base', help="target directory in $host_dir")
@arg('packages', nargs="+", help="names (on PyPi) of packages to install")
@arg('operation', help="only supported value is 'install'")
@line_magic
def pip_magic(kernel, args):
    """Install packages from PyPi
Default install directory is "$host_dir/base/lib" and can be changed by 
the -p and -l options. The directory is created if it does not exist.

Examples:

    %pip install adafruit-io
    %pip install pycopy-urequests Adafruit-BME280
    %pip -p my_project -l my_lib install micropython-uargparse micropython-mpu6886

Implemented with https://pypi.org/project/micropython-cpython-upip and pip3.
    """
    path = os.path.join(Config.get('host_dir', '~'), args.project, args.lib)
    os.makedirs(path, exist_ok=True)
    for p in args.packages:
        # try upip first
        try:
            # print("Trying standard pip ...", file=sys.stderr)
            install(p, path)
        except Exception as e1:
            print(e1)
            print("Trying upip ...")
            try:
                # see https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
                # it's a mac issue, ugly fix:
                #    import ssl
                #    ssl._create_default_https_context = ssl._create_unverified_context
                # Better solution: run
                #    /Applications/Python 3.8/Install Certificates.command
                upip.install([p], path)
                print(f"Successfully installed {p} in {path}")
            except Exception as e2:
                print("install failed", file=sys.stderr)
                print(e2, file=sys.stderr)
        print()
