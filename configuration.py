# Librairie(s)
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SECRET_FILE_PATH = 'secrets.json'
SECRET_CONFIG_STORE = {}

try:
    with open(SECRET_FILE_PATH) as config:
        SECRET_CONFIG_STORE = json.load(config)
except FileNotFoundError:
    try:
        with open(os.path.join(BASE_DIR, 'secrets.json')) as config:
            SECRET_CONFIG_STORE = json.load(config)
    except Exception:
        raise


class BaseConfig(object):
    APPLICATION_NAME = 'Scripts interface'
    BASE_DIR = BASE_DIR


class Config(BaseConfig):
    DEBUG = 1
    PRIORITY_DEBUG_LEVEL = 100
    GUI_PROPERTIES = {
        "bg": "black",
        "size": ["400", "500"],
        "title": "Scripts Dashboard",
        "space_between_btn": 10
    }
    GLOBAL = dict()
    if "win" in sys.platform:
        GLOBAL["os"] = "win"
        GLOBAL["cmds"] = {
            "add cmd": "&",
            "open new terminal and pass cmds": "start cmd /K",
            "print": "echo"
        }
    elif "linux" in sys.platform:
        GLOBAL["os"] = "linux"
        GLOBAL["cmds"] = {
            "add cmd": ";",
            "open new terminal and pass cmds": "lxterminal -e",
            "print": "echo"
        }
    else:
        GLOBAL["os"] = sys.platform


class ConfigurationException(Exception):
    pass


class Configuration(dict):
    def from_object(self, obj):
        for attr in dir(obj):

            if not attr.isupper():
                continue

            self[attr] = getattr(obj, attr)

        self.__dict__ = self


APP_CONFIG = Configuration()
APP_CONFIG.from_object(Config)
