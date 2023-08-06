import os
from configparser import ConfigParser
from pathlib import Path


class LinuxAuth:

    def _get_auth_from_env(self):
        """Loading auth code for unix system"""
        token = os.getenv('TCR')
        if token is not None:
            return token

        return None

    def get_auth_from_env(self):
        """Loading auth code for unix system"""
        return self._get_auth_from_env()

    def _get_auth_from_property(self):
        """Loading auth code for unix system"""
        home = str(Path.home())
        prop_file = home + '\.tcr'
        config = ConfigParser()
        config.read(prop_file)
        token = config.get('default', 'token')
        return token

    def get_auth_from_property(self):
        """Loading auth code for unix system"""
        return self._get_auth_from_property()
