#!python
# -*- coding: utf-8 -*-

"""
Select class by rotational symmetry and save selection into CXI file
Author: Sergey Bobkov
"""

import os
import argparse
import shutil
import subprocess
import numpy as np

from spi_em_class import config, em_data, symmetry


def main():
    parser = argparse.ArgumentParser(description='Select class by rotational symmetry and save selection into CXI file')
    parser.add_argument('order', type=int, help='Symmetry order')
    parser.add_argument('-f', '--fringe', default=0, type=int, help='Fringe to analyse, 0 - consider all data')
    parser.add_argument('-t', '--threshold', default=0.5, type=float, help='Selection threshold')
    parser.add_argument('-o', '--out',
                        help="Output CXI file (default: add selection into base CXI file)")
    parser.add_argument('-c', '--class', dest='class_dset', default='em_class/classes',
                        help="Dataset with result classes")
    parser.add_argument('-s', '--select', dest='select_dset', default='em_class/select',
                        help="Dataset with result selection")
    parser.add_argument('-d', '--data', default=em_data.DEFAULT_DATA,
                        help='File with EM class data')
    parser_args = parser.parse_args()

    fringe = parser_args.fringe
    symmetry_order = parser_args.order
    symmetry_thresh = parser_args.threshold
    out_file = parser_args.out
    class_dset = parser_args.class_dset
    select_dset = parser_args.select_dset
    data_file = parser_args.data

    if not os.path.isfile(data_file):
        parser.error("File {} doesn't exist".format(data_file))

    if not 0 < symmetry_order < 50:
        parser.error("Symmetry order {} do not fit into [2, 50]".format(symmetry_order))

    if not 0 < symmetry_thresh < 1:
        parser.error("Threshold {} do not fit into (0, 1)".format(symmetry_thresh))

    params = config.load_config(data_file)
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

    result_data = em_data.load_iteration_data(data_file, last_iter)
    class_data = result_data['classes']
    model_data = result_data['model']

    if params['logscale']:
        model_data = np.exp(model_data) - 1

    good_class = []
    for i, data in enumerate(model_data):
        scores = symmetry.get_symmetry_scores(data)
        if fringe > 0:
            if fringe > scores.shape[0]:
                raise ValueError('No data for selected fringe: ' + \
                                 '{} > {}'.format(fringe, scores.shape[0] - 1))
            fringe_scores = scores[fringe]
            if scores[0, :].min() > 0:
                fringe_scores /= scores[0, :]
        else:
            fringe_scores = scores[:].sum(axis=0)

        fringe_scores[0] = 0
        fringe_scores /= fringe_scores.sum()
        order_score = fringe_scores[symmetry_order]
        if order_score >= symmetry_thresh:
            good_class.append(i + 1)
            sign = ">="
        else:
            sign = "<"

        print('Class {:2d}: {:0.2f} {} {:0.2f}'.format(i + 1, order_score, sign, symmetry_thresh))

    select_data = np.isin(class_data, [x for x in good_class])

    print('Saved selection of {}/{} frames in {} classes'.format(select_data.sum(),
                                                                 len(select_data),
                                                                 len(good_class)))

    em_data.save2cxi(out_file, class_data, class_dset)
    em_data.save2cxi(out_file, select_data, select_dset)


if __name__ == '__main__':
    main()
