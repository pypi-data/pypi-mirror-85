#!python
# -*- coding: utf-8 -*-

"""
Reset EM classification data
Author: Sergey Bobkov
"""

import os
import argparse

from spi_em_class import em_data


def main():
    parser = argparse.ArgumentParser(description='Reset EM classification data')
    parser.add_argument('-d', '--data', default=em_data.DEFAULT_DATA,
                        help='File with EM class data')
    parser_args = parser.parse_args()

    data_file = parser_args.data

    if not os.path.isfile(data_file):
        parser.error("File {} doesn't exist".format(data_file))

    em_data.reset_data(data_file)


if __name__ == '__main__':
    main()
