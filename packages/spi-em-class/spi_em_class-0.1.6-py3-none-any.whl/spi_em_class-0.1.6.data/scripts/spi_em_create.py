#!python
# -*- coding: utf-8 -*-

"""
Create new EM classification
Author: Sergey Bobkov
"""

import os
import argparse

from spi_em_class import config, em_data


def main():
    parser = argparse.ArgumentParser(description='Create new EM classification')
    parser.add_argument('cxi_file', metavar='FILE', help='Input CXI file')
    parser.add_argument('-d', '--data', default=em_data.DEFAULT_DATA, help='Output file with EM class data')
    parser_args = parser.parse_args()

    cxi_file = parser_args.cxi_file
    data_file = parser_args.data

    if not os.path.isfile(cxi_file):
        parser.error("File {} doesn't exist".format(cxi_file))

    if not em_data.check_cxi_file(cxi_file):
        parser.error("File {} is not a valid CXI file".format(cxi_file))

    if os.path.exists(data_file):
        parser.error("File {} already exist".format(data_file))
    else:
        dirname = os.path.dirname(data_file)
        if dirname:
            os.makedirs(dirname, exist_ok=True)

    params = config.default_config()
    params['cxi_file'] = os.path.abspath(cxi_file)

    config.save_config(data_file, params)

    print('Create new EM classification data in {}'.format(data_file))


if __name__ == '__main__':
    main()
