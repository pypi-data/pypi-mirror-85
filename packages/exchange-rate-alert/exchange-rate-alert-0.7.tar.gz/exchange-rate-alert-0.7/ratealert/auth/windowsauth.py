import os
from configparser import ConfigParser
from pathlib import Path


class WindowsAuth:

    def _get_auth_from_env(self):
        """Loading auth code for windows system from environment variable"""
        token = os.getenv('TCR')
        if token is not None:
            return token

        return None

    def get_auth_from_env(self):
        """Loading auth code for windows system from environment variable"""
        return self._get_auth_from_env()

    def _get_auth_from_property(self):
        """Loading auth code for windows system from property file"""
        home = str(Path.home())
        prop_file = home+'\.tcr'
        config = ConfigParser()
        config.read(prop_file)
        token = config.get('default', 'token')
        return token

    def get_auth_from_property(self):
        """Loading auth code for windows system from property file"""
        return self._get_auth_from_property()
