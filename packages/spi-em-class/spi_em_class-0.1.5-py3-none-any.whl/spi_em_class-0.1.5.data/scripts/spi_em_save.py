#!python
# -*- coding: utf-8 -*-

"""
Save selection into CXI file
Author: Sergey Bobkov
"""

import os
import argparse
import shutil
import subprocess
import numpy as np

from spi_em_class import config, em_data


def main():
    parser = argparse.ArgumentParser(description='Save selection into CXI file')
    parser.add_argument('select_class', nargs='+', type=int, help='Selected classes')
    parser.add_argument('-o', '--out',
                        help="Output CXI file (default: add selection into base CXI file)")
    parser.add_argument('-c', '--class', dest='class_dset', default='em_class/classes',
                        help="Dataset with result classes")
    parser.add_argument('-s', '--select', dest='select_dset', default='em_class/select',
                        help="Dataset with result selection")
    parser.add_argument('-d', '--data', default=em_data.DEFAULT_DATA,
                        help='File with EM class data')
    parser_args = parser.parse_args()

    good_class = parser_args.select_class
    out_file = parser_args.out
    class_dset = parser_args.class_dset
    select_dset = parser_args.select_dset
    data_file = parser_args.data

    if not os.path.isfile(data_file):
        parser.error("File {} doesn't exist".format(data_file))

    params = config.load_config(data_file)

    for cla in good_class:
        if not 0 < cla < params['num_class']:
            parser.error("Class {} do not fit into [1, {}]".format(cla, params['num_class']))

    last_iter = em_data.get_num_saved_iterations(data_file)
    if last_iter == 0:
        parser.error('Empty classification data')

    if out_file is None:
        out_file = params['cxi_file']
    else:
        if os.path.exists(out_file):
            parser.error("File {} already exist".format(out_file))

        out_dir = os.path.dirname(out_file)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        shutil.copy(params['cxi_file'], out_file)
        subprocess.call(["/bin/chmod", "u+w", out_file])

    result_data = em_data.load_iteration_data(data_file, last_iter, for_report=True)
    class_data = result_data['classes']
    select_data = np.isin(class_data, [x for x in good_class])

    print('Saved selection of {}/{} frames in {} classes'.format(select_data.sum(),
                                                                 len(select_data),
                                                                 len(good_class)))

    em_data.save2cxi(out_file, class_data, class_dset)
    em_data.save2cxi(out_file, select_data, select_dset)


if __name__ == '__main__':
    main()
