from openpyn import __basefilepath__
from openpyn import root
import yaml
from pathlib import Path

# This module should store and retrieve the app config
# We should store in the config a key, which can be used
# to unlock the uname/password
DEFAULT_CONFIG = Path('/home/connor/.config/nordvpn.yml')


def get_config(path=DEFAULT_CONFIG) -> dict:
    '''Returns a dict containing config variables for this host'''
    try:
        with path.open('r') as config_file:
            config = yaml.load(config_file)

    except FileNotFoundError:
        return {}

    return config


def write_config(config, path=DEFAULT_CONFIG):
    '''Writes the given config to the provided path.'''
    if not path.exists():
        path.touch()

    with path.open('w') as config_file:
        config_file.write(yaml.dump(config))
