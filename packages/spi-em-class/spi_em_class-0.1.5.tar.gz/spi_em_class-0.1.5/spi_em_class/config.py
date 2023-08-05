"""
Functions for configuration file
Author: Sergey Bobkov
"""

import os
import sys
import errno
import configparser
import h5py


CONFIG_PARAMS = {
    # Param names in config with corresponding types
    'best_proba': bool,
    'binning': int,
    'cxi_file': str,
    'friedel': bool,
    'logscale': bool,
    'num_class': int,
    'num_rot': int,
    'q_max': int,
    'q_min': int,
}


def save_config(data_file, param_dict, verbose=False):
    """Save parameters into hdf5 data file, update if already present

    Keyword arguments:
    data_file -- hdf5 file to save configuration
    param_dict -- dict with parameters
    verbose -- print updates to stderr
    """

    with h5py.File(data_file, 'a') as h5file:
        config_group = h5file.require_group('config')

        if verbose:
            print('Config update:', file=sys.stderr)
        for key in CONFIG_PARAMS:
            value = param_dict[key]
            if value is None:
                raise ValueError('Value of {} is None'.format(key))
            if key in config_group:
                if config_group[key][()] != value and verbose:
                    print('\tUpdate {}: {}->{}'.format(key, config_group[key][()], value),
                          file=sys.stderr)
                del config_group[key]
            elif verbose:
                print('\tAdd {}: {}'.format(key, value), file=sys.stderr)
            config_group[key] = value


def load_config(data_file):
    """Load parameters from hdf5 data file and returns them as dict

    Keyword arguments:
    data_file -- hdf5 file with configuration

    Return:
    param_dict -- dict with parameters
    """

    if not os.path.exists(data_file):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), data_file)

    with h5py.File(data_file, 'r') as h5file:
        config_group = h5file['config']
        param_dict = {}
        for key in CONFIG_PARAMS:
            param_dict[key] = config_group[key][()]

        return param_dict


def load_text_config(text_file):
    """Load parameters from text configuration file and returns them as dict

    Keyword arguments:
    text_file -- text file with configuration

    Return:
    param -- dict with parameters
    """
    config = configparser.ConfigParser()
    config.read(text_file)

    def_section = config['default']

    param = {}

    for key, key_type in CONFIG_PARAMS.items():
        if key_type == bool:
            param[key] = def_section.getboolean(key)
        elif key_type == int:
            param[key] = def_section.getint(key)
        elif key_type == str:
            param[key] = def_section.get(key)
        else:
            raise ValueError('Unknown parameter type: {}'.format(key_type))

    return param


def save_text_config(text_file, param):
    """Save parameters into text file

    Keyword arguments:
    text_file -- text file to save configuration
    param -- dict with parameters
    """
    config = configparser.ConfigParser()
    def_sect = {}
    for key, key_type in CONFIG_PARAMS.items():
        if key_type == bool:
            def_sect[key] = 'yes' if param[key] else 'no'
        else:
            def_sect[key] = param[key]

    config['default'] = def_sect

    with open(text_file, 'w') as configfile:
        config.write(configfile)


def default_config():
    """Load default config

    Return:
    param -- dict with parameters
    """
    config_file = os.path.join(os.path.dirname(__file__), 'data/default_config.ini')
    return load_text_config(config_file)
