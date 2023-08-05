from iot_device import DeviceRegistry                # pylint: disable=import-error
from iot_device import DiscoverNet                   # pylint: disable=import-error
from iot_device import DiscoverSerial                # pylint: disable=import-error
from iot_device import EvalException                 # pylint: disable=import-error
from iot_device import Config                        # pylint: disable=import-error
import iot_device                                    # pylint: disable=import-error

from .output import Output
from .kernel_logger import logger
from .kernel_config import KernelConfig
from .magics.magic import LINE_MAGIC
from .version import __version__

from ipykernel.ipkernel import IPythonKernel         # pylint: disable=import-error
from termcolor import colored                        # pylint: disable=import-error
import traceback, re, os, logging


class IoTKernel(IPythonKernel):
    """
    IoT kernel evaluates code on (remote) IoT devices.
    """

    implementation = 'iot-kernel'
    implementation_version = __version__
    language_info = {
        'name': 'python',
        'version': '3',
        'mimetype': 'text/x-python',
        'file_extension': '.py',
        'pygments_lexer': 'python3',
        'codemirror_mode': {'name': 'python', 'version': 3},
    }
    banner = "IoT Kernel - Python on a microcontroller"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        logger.info(f"versions: iot_kernel {__version__}, {iot_device.__version__}")
        self.__registry = DeviceRegistry()
        DiscoverSerial().register_listener(self.__registry)
        DiscoverNet().register_listener(self.__registry)
        # last used Device is default
        uid = KernelConfig.get('default_uid', '')
        self.__device = self.__registry.get_device(uid)
        logger.info(f"connected to {self.__device}")
        # set initial iPython pwd
        code = "import os;  os.chdir(os.getenv('IOT49', '~'))"
        super().do_execute(code, True, False, False, False)

    @property
    def registry(self):
        return self.__registry

    @property
    def device(self):
        if not self.__device:
            # last used Device is default
            uid = KernelConfig.get('default_uid', '')
            self.__device = self.__registry.get_device(uid)
            if not self.__device:
                raise EvalException("no device connected")
        if self.__device.locked:
            raise EvalException(f"{self.__device.name} is busy")
        return self.__device

    @device.setter
    def device(self, dev):
        self.__device = dev
        KernelConfig.set('default_uid', dev.uid)

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.silent = silent
        self.store_history = store_history
        self.user_expressions = user_expressions
        self.allow_stdin = allow_stdin
        try:
            for cell in ('connect\n' + code).split('\n%%'):
                self.__execute_section('%%' + cell)
        except KeyboardInterrupt:
            self.error('Interrupted')
        except EvalException as rex:
            logger.debug(traceback.format_exc())
            logger.error(f"EvalException in kernel.do_execute: {rex}")
            self.error(str(rex))
        except ConnectionResetError as cre:
            self.error(f"Device disconnected {cre}")
        except Exception as ex:
            logger.exception(f"Unhandled exception '{ex}' in kernel.do_execute")
            self.error(f"{ex}\n")
            self.error(f"\n{traceback.format_exc()}\n")
        return {
            'status': 'ok',
            'execution_count': self.execution_count,
        }

    def __execute_section(self, cell):
        head, code = (cell + '\n').split('\n', 1)
        code = code.strip()
        magic, args = (head + ' ').split(' ', 1)
        args = args.strip()
        if magic == '%%connect':
            if not code:
                return
            if not args:
                # run cell on currently connected mcu
                self.__execute_cell(code)
            else:
                # run cell on each mcu in %%connect argument list
                names = args.split(' ')
                for hostname in names:
                    if not hostname or hostname == '-q':
                        continue
                    if not '-q' in names:
                        self.print(f"\n----- {hostname}\n", 'grey', 'on_yellow')
                    uid = Config.hostname2uid(hostname)
                    if not uid: uid = hostname
                    dev = self.registry.get_device(uid)
                    if not dev:
                        if hostname == '--host':
                            # accept '--host' as the host's hostname
                            self.execute_ipython(code)
                        else:
                            self.error(f"No such device: {hostname}")
                            continue
                    else:
                        dev_ = self.device
                        self.device = dev
                        try:
                            self.__execute_cell(code)
                        finally:
                            self.device = dev_
        elif magic == '%%host':
            # evaluate code on ipython
            return self.execute_ipython(code)
        else:
            # let ipython handle the cell magic
            return self.execute_ipython(cell)

    def execute_ipython(self, code):
        # evaluate code with IPython
        super().do_execute(code, self.silent, self.store_history, self.user_expressions, self.allow_stdin)

    def __execute_cell(self, code):
        # evaluate IoT Python cell
        while code:
            code = code.strip()
            if code.startswith('%') or code.startswith('!'):
                split = code.split('\n', maxsplit=1)
                line = split[0]
                code = split[1] if len(split) > 1 else None
                self.__line_magic(line)
            else:
                # eval on mcu ...
                idx = min((code+'\n%').find('\n%'), (code+'\n!').find('\n!'))
                with self.device as repl:
                    repl.eval(code[:idx], Output(self))
                    code = code[idx:]

    def __line_magic(self, line):
        if line.startswith('!'):
            logger.debug(f"shell escape: {line}")
            self.execute_ipython(line)
            return
        m = re.match(r'%([^ ]*)( .*)?', line)
        if not m:
            self.error(f"Syntax error: '{line.encode()}'\n")
            return
        name = m.group(1)
        rest = m.group(2)
        rest = (rest or '').strip()
        method = LINE_MAGIC.get(name)
        logger.debug(f"line_magic name={name} rest={rest} method={name}")
        if method:
            method[0](self, rest)
        else:
            # pass line magic to ipython
            logger.debug(f"pass to IPython: {line}")
            self.execute_ipython(line)

    def print(self, text, *color):
        text = colored(str(text), *color)
        stream_content = {'name': 'stdout', 'text': text}
        self.send_response(self.iopub_socket, 'stream', stream_content)

    def error(self, text, *color):
        if not len(text.strip()): return
        text = colored(str(text), *color)
        stream_content = {'name': 'stderr', 'text': text}
        self.send_response(self.iopub_socket, 'stream', stream_content)