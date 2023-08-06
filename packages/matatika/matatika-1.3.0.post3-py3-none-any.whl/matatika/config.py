"""config module"""

import configparser
from pathlib import Path
from enum import Enum
from matatika.exceptions import AuthContextNotSetError
from matatika.exceptions import EndpointURLContextNotSetError
from matatika.exceptions import WorkspaceContextNotSetError


class ConfigSection(Enum):
    """Class to handle the enumeration of a section within a config file"""
    DEFAULT = 'DEFAULT'


class ConfigKey(Enum):
    """Class to handle the enumeration of a key within a section of a config file"""

    ENDPOINT_URL = 'endpoint_url'
    WORKSPACE = 'workspace'
    TOKEN = 'token'


class MatatikaConfig():
    """Class to handle read/write operations to a config file"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.optionxform = str

        matatika_home_dir = Path.joinpath(Path.home(), '.matatika')
        Path.mkdir(matatika_home_dir, exist_ok=True)
        self.config_file = Path.joinpath(matatika_home_dir, 'config.matatika')

    # private function
    def _read_config(self, key, section=ConfigSection.DEFAULT.value):
        """Reads from the config file"""

        self.config.read(self.config_file)
        return self.config[section][key]

        # private function
    def _write_config(self, key, value, section=ConfigSection.DEFAULT.value):
        """Writes to the config file"""

        self.config.read(self.config_file)
        self.config[section][str(key)] = value
        with open(self.config_file, 'w+') as conf_file:
            self.config.write(conf_file)
        conf_file.close()

    def set_auth_token(self, token):
        """Sets the auth token in the config file"""

        self._write_config(ConfigKey.TOKEN.value, token)

    def get_auth_token(self):
        """Return the auth token in the config file"""

        try:
            return self._read_config(ConfigKey.TOKEN.value)
        except KeyError as err:
            raise AuthContextNotSetError from err

    def set_default_workspace(self, workspace):
        """Sets the default workspace ID in the config file"""

        self._write_config(ConfigKey.WORKSPACE.value, workspace)

    def get_default_workspace(self):
        """Returns the default workspace ID in the config file"""

        try:
            return self._read_config(ConfigKey.WORKSPACE.value)
        except KeyError as err:
            raise WorkspaceContextNotSetError from err

    def set_endpoint_url(self, url):
        """Sets the endpoint URL in the config file"""

        self._write_config(ConfigKey.ENDPOINT_URL.value, url)

    def get_endpoint_url(self):
        """Returns the endpoint URL in the config file"""

        try:
            return self._read_config(ConfigKey.ENDPOINT_URL.value)
        except KeyError as err:
            raise EndpointURLContextNotSetError from err


# Delete this later - only for dev testing
if __name__ == "__main__":
    conf = MatatikaConfig()
    # conf.set_auth_token('llll')
    # conf.set_default_workspace('workspace')
    print(conf.get_auth_token())
    print(conf.get_default_workspace())
