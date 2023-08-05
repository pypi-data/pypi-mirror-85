import json
from os import path
from pathlib import Path  # if you haven't already done so

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]


def read_config_file(filename):
    with open(path.join(parent, filename), "r") as f:
        config = json.load(f)
    return config


def write_config_file(config, filename):
    writeable_config = json.dumps(config, indent=4)
    with open(path.join(parent, filename), "w") as f:
        f.write(writeable_config)


def set_config(key, value, filename="config.json"):
    config = read_config_file(filename=filename)
    config[key] = value
    write_config_file(config, filename=filename)


def get_config(key, filename="config.json"):
    config = read_config_file(filename=filename)
    return config[key]


class Config(object):
    def __init__(self, filename):
        self.filename = filename

    def __getattr__(self, key):
        """对于要请求的参数 直接从配置文件获取
        Args:
            key (string): 文件名
        """
        return get_config(key, filename=self.filename)
