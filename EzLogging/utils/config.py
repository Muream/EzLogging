import EzLogging.utils as utils
import json

class Config(object):
    """Configuration class.

    This is a singleton so it stays in sync across the applcation.
    to use it do:
        from EzLogging.core.config import config
        config.my_attr = 'my value'
        print config.my_attr
    if my_attr does not exist, it is added to the config json automatically.
    when you get an attribute, it is directly fetched from the json.
    any non existing attribute will return None.
    """
    def __init__(self):
        self._config_file = None
        self._data = None
        self.get_config_file()

    def __setattr__(self, attr, value):
        if not isinstance(attr, str):
            attr = str(attr)
        data = self.data
        data[attr] = value
        self.data = data

    def __getattr__(self, attr):
        if not isinstance(attr, str):
            attr = str(attr)

        if self.data.has_key(attr):
            return self.data[attr]
        else:
            return None

    @property
    def data(self):
        return _data

    @data.getter
    def data(self):
        with open(self._config_file, 'r') as f:
            content = f.read()
        return json.loads(content)

    @data.setter
    def data(self, content):
        with open(self._config_file, 'w') as f:
            content = json.dumps(content, indent=4)
            f.write(content)

    def get_config_file(self):
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
            open(self._config_file, 'w').close


config = Config()
