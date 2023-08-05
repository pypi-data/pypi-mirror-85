from iot_device import Config      # pylint: disable=import-error
from json import dumps
import datetime
import os

"""
Manage kernel configuration
"""

class KernelConfig:

    CONFIG_FILE = os.path.join(Config.get('host_dir'), ".iotrc")
    __config = {}

    @staticmethod
    def get(param, default=None):
        KernelConfig.__load()
        return KernelConfig.__config.get(param, default)

    @staticmethod
    def set(param, value):
        if not KernelConfig.__config:
            KernelConfig.__config = {}
        KernelConfig.__config[param] = value
        KernelConfig.__save()

    @staticmethod
    def __load():
        if KernelConfig.__config: return
        try:
            with open(KernelConfig.CONFIG_FILE, 'r') as file:
                KernelConfig.__config = {}
                exec(file.read(), KernelConfig.__config)
                KernelConfig.__config.pop('__builtins__', None)
        except FileNotFoundError:
            KernelConfig.__config = {}

    @staticmethod
    def __save():
        if not KernelConfig.__config: return
        with open(KernelConfig.CONFIG_FILE, 'w') as file:
            file.write("# iot-kernel configuration, updated {}\n".format(datetime.datetime.now().isoformat()))
            for k, v in KernelConfig.__config.items():
                file.write("{} = {}\n".format(k, dumps(v)))
