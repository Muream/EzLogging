import json
import os

import EzLogging.utils.utils as utils

class Config(object):
    """Configuration class.

    To use it do:
        from EzLogging.core.config import config
        config.my_attr = 'my value'
        print config.my_attr
    If my_attr does not exist, it is added to the config json automatically.
    When you get an attribute, it is directly fetched from the json.
    Any non existing attribute will return None.
    WARNING:
        every attribute of the config SHOULD NOT start with an underscore
        every attribute of the class SHOULD start with an underscore
    """
    def __init__(self):
        self._config_file = None
        self._config_data = {}
        self._get_config_file()

    def __setattr__(self, name, value):
        """Set the attribute with the given value.

        If it starts with an underscore, set it using the default behavior
        Else, add to the json the name as a key and the value as its value
        """
        if name.startswith('_'):
            super(Config, self).__setattr__(name, value)
        else:
            data = self._data
            data[name] = value
            self._data = data

    def __getattr__(self, name):
        """Get the attribute.

        If it starts with an underscore, get it using the default behavior
        Else, get it from the json
        """
        if name.startswith('_'):
            return super(Config, self).__getattribute__(name)

        if self._data.has_key(name):
            return self._data[name]
        else:
            return None

    def __delattr__(self, name):
        """Delete the attribute.

        If it starts with an underscore, delete it using the default behavior
        Else, delete it from the json
        """
        if name.startswith('_'):
            super(Config, self).__delattr__(name)
            return

        if self._data.has_key(name):
            data = self._data
            data.pop(name)
            self._data = data


    @property
    def _data(self):
        return _config_data

    @_data.getter
    def _data(self):
        with open(self._config_file, 'r') as f:
            content = f.read()
        return json.loads(content)

    @_data.setter
    def _data(self, content):
        with open(self._config_file, 'w') as f:
            content = json.dumps(content, indent=4)
            f.write(content)

    def _get_config_file(self):
        if os.name == 'posix' and os.getenv("USER") == "root":
            sudo_user = os.getenv("SUDO_USER")
            config_folder = "/home/{}/EzLogging/".format(sudo_user)
        else:
            config_folder = os.path.expanduser("~/EzLogging/")

        if not config_folder:
            return

        if not os.path.exists(config_folder):
            os.makedirs(config_folder)

        self._config_file = os.path.join(config_folder, "config.json")
        self._config_file = utils.normalize_path(self._config_file)

        if not os.path.exists(self._config_file):
            with open(self._config_file, 'w') as f:
                f.write('{}')


config = Config()

