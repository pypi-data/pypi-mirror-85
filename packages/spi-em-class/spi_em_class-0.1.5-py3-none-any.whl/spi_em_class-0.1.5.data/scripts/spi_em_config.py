#!python
# -*- coding: utf-8 -*-

"""
Configure EM classification parameters
Author: Sergey Bobkov
"""

import os
import sys
import argparse
import configparser
import tempfile
import subprocess

from spi_em_class import config, em_data


def get_error_lines(param):
    err_lines = []

    if 'cxi_file' in param:
        if param['cxi_file'] is None:
            err_lines.append("cxi_file is not defined")
        elif not os.path.exists(param['cxi_file']) or not os.path.isfile(param['cxi_file']):
            err_lines.append("File {} doesn't exist".format(param['cxi_file']))
        elif not em_data.check_cxi_file(param['cxi_file']):
            err_lines.append("{} is not a valid cxi file".format(param['cxi_file']))

    if 'q_max' in param:
        if param['q_max'] is None:
            err_lines.append("q_max is not defined")
        elif param['q_max'] < 0:
            err_lines.append("Negative q_max is not allowed")

    if 'q_min' in param:
        if param['q_min'] is None:
            err_lines.append("q_min is not defined")
        elif param['q_min'] < 0:
            err_lines.append("Negative q_min is not allowed")

    if 'q_max' in param and 'q_min' in param:
        if param['q_max'] < param['q_min'] and param['q_max'] > 0:
            err_lines.append("q_max cannot be < q_min")

    if 'num_rot' in param:
        if param['num_rot'] is None:
            err_lines.append("num_rot is not defined")
        elif param['num_rot'] < 1:
            err_lines.append("Number of rotations < 1 is not allowed")

    if 'num_class' in param:
        if param['num_class'] is None:
            err_lines.append("num_class is not defined")
        elif param['num_class'] < 1:
            err_lines.append("Number of classes < 1 is not allowed")

    if 'binning' in param:
        if param['binning'] is None:
            err_lines.append("binning is not defined")
        elif param['binning'] < 1:
            err_lines.append("binning < 1 is not allowed")

    return err_lines


def edit_params(data_file):
    param = config.load_config(data_file)
    tmpf = tempfile.NamedTemporaryFile(suffix=".tmp", delete=False)
    tmpf.close()
    config.save_text_config(tmpf.name, param)

    while True:
        subprocess.call([os.environ.get('EDITOR', 'mcedit'), tmpf.name])
        try:
            new_param = config.load_text_config(tmpf.name)
        except (configparser.Error, ValueError):
            with open(tmpf.name, "a+") as openfile:
                openfile.write('# Parsing Error, please fix and save file\n')
                continue

        err_lines = get_error_lines(new_param)
        if err_lines:
            config.save_text_config(tmpf.name, new_param)
            with open(tmpf.name, "a+") as openfile:
                openfile.write('# ERROR:')
                for line in err_lines:
                    openfile.write('# ' + line + '\n')
                openfile.write('# Invalid parameters, please fix and save file\n')
                continue

        break

    os.remove(tmpf.name)
    config.save_config(data_file, new_param, verbose=True)


def main():
    parser = argparse.ArgumentParser(description='Configure EM classification parameters')
    parser.add_argument('-d', '--data', default=em_data.DEFAULT_DATA,
                        help='File with EM class data')
    parser.add_argument('--cxi', dest='cxi_file', metavar='FILE', help='Input CXI file')
    parser.add_argument('--q_min', dest='q_min', type=int,
                        help='Minumum q-radius used in classification (pixels)')
    parser.add_argument('--q_max', dest='q_max', type=int,
                        help='Maximim q-radius used in classification (pixels)')
    parser.add_argument('--num_rot', dest='num_rot', type=int,
                        help="Number of considered rotation angles")
    parser.add_argument('--num_class', dest='num_class', type=int,
                        help="Number of EM classes")
    parser.add_argument('--friedel', dest='friedel', action='store_true',
                        help="Apply Friedel symmetry")
    parser.add_argument('--no-friedel', dest='nofriedel', action='store_true',
                        help="Do not apply Friedel symmetry")
    parser.add_argument('--logscale', dest='logscale', action='store_true',
                        help="Apply log-scaling to input data")
    parser.add_argument('--no-logscale', dest='nologscale', action='store_true',
                        help="Do not apply log-scaling to input data")
    parser.add_argument('--best', dest='best_proba', action='store_true',
                        help="Consider only one orientation with best probability for each frame")
    parser.add_argument('--no-best', dest='no_best_proba', action='store_true',
                        help="Consider all orientations")
    parser.add_argument('--binning', dest='binning', type=int,
                        help="Bin input frames (Combine pixels in BIN*BIN groups togeather)")
    parser.add_argument('-s', '--show', dest='show', action='store_true',
                        help="Show current configuration (ignore other parameters)")
    parser.add_argument('-e', '--editor', dest='editor', action='store_true',
                        help="Open editor (default if no parameters)")
    parser_args = parser.parse_args()

    data_file = parser_args.data
    show = parser_args.show
    editor = parser_args.editor

    if len(sys.argv) <= 1:
        editor = True

    if not os.path.isfile(data_file):
        parser.error("File {} doesn't exist".format(data_file))

    if editor:
        edit_params(data_file)
    elif show:
        print('Current parameters:')
        param = config.load_config(data_file)
        for key in param:
            print('{:>20s}: {}'.format(key, param[key]))
    else:
        param = config.load_config(data_file)
        if parser_args.friedel and parser_args.nofriedel:
            parser.error("Parameters --friedel and --no-friedel are not compatible")

        if parser_args.best_proba and parser_args.no_best_proba:
            parser.error("Parameters --best and --no-best are not compatible")

        if parser_args.cxi_file is not None:
            cxi_file = parser_args.cxi_file
            param['cxi_file'] = os.path.abspath(cxi_file)

        if parser_args.q_max is not None:
            param['q_max'] = parser_args.q_max

        if parser_args.q_min is not None:
            param['q_min'] = parser_args.q_min

        if parser_args.num_rot is not None:
            param['num_rot'] = parser_args.num_rot

        if parser_args.num_class is not None:
            param['num_class'] = parser_args.num_class

        if parser_args.friedel:
            param['friedel'] = True

        if parser_args.nofriedel:
            param['friedel'] = False

        if parser_args.logscale:
            param['logscale'] = True

        if parser_args.nologscale:
            param['logscale'] = False

        if parser_args.best_proba:
            param['best_proba'] = True

        if parser_args.no_best_proba:
            param['best_proba'] = False

        if parser_args.binning is not None:
            param['binning'] = parser_args.binning

        err_lines = get_error_lines(param)
        if err_lines:
            parser.error('\n'.join(err_lines))
        else:
            config.save_config(data_file, param, verbose=True)


if __name__ == '__main__':
    main()
