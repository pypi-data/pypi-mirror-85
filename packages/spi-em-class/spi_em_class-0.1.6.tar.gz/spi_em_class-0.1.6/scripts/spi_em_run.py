#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Run EM classification
Author: Sergey Bobkov
"""

import os
import argparse

from spi_em_class import Classifier, em_data


def main():
    parser = argparse.ArgumentParser(description='Classify CXI data by EMC')
    parser.add_argument('iter', type=int, help="Number of iterations")
    parser.add_argument('-d', '--data', default=em_data.DEFAULT_DATA,
                        help='File with EM class data')
    parser_args = parser.parse_args()

    n_iter = parser_args.iter
    data_file = parser_args.data

    if not os.path.isfile(data_file):
        parser.error("File {} doesn't exist".format(data_file))

    if n_iter < 1:
        parser.error("Number of iterations should be >= 1")

    em_class = Classifier(data_file)
    em_class.run(n_iter)


if __name__ == '__main__':
    main()
