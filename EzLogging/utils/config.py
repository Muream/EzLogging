import os
from ConfigParser import SafeConfigParser

# get the config file
if os.name == 'posix' and os.getenv("USER") == "root":
    SUDOUSER = os.getenv("SUDO_USER")
    CONFIG = "/home/{}/EzLogging/config.cfg".format(SUDOUSER)
else:
    CONFIG = os.path.expanduser("~/EzLogging/config.cfg")


def set_config():
    pass


def read_config():
    config = {}
    parser = SafeConfigParser()
    parser.read(CONFIG)

    for name in parser.options('Strings'):
        config[name] = parser.get('Strings', name)

    for name in parser.options('Floats'):
        config[name] = parser.getfloat('Floats', name)
    config['clip length'] = config['cut before'] + config['cut after']
    return config
