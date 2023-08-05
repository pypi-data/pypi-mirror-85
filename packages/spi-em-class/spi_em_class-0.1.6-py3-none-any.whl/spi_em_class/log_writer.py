"""
Functions for classification log
Author: Sergey Bobkov
"""

import sys

LOG_FILENAME = 'EM.log'


def show_message(text):
    sys.stderr.write(text+'\n')
    sys.stderr.flush()


def write_log_header(param, num_frames):
    with open(LOG_FILENAME, 'w') as logfile:
        logfile.write('Classification with the EM algorithm\n\n')

        logfile.write('Data parameters:\n')
        logfile.write('\tnum data = {}\n'.format(num_frames))
        logfile.write('\tq_min = {}\n'.format(param['q_min']))
        logfile.write('\tq_max = {}\n'.format(param['q_max']))
        logfile.write('\tnum rotations = {}\n'.format(param['num_rot']))
        logfile.write('\tnum classes = {}\n'.format(param['num_class']))
        logfile.write('\tfriedel = {}\n'.format(param['friedel']))
        logfile.write('\tlogscale = {}\n'.format(param['logscale']))
        logfile.write('\tbest_proba = {}\n'.format(param['best_proba']))
        logfile.write('\tbinning = {}\n'.format(param['binning']))
        logfile.write('\n')

        logfile.write('Iter \ttime \tmutual_info\n')


def write_log_iter(iter_num, iter_time, mutual_info):
    with open(LOG_FILENAME, 'a+') as logfile:
        logfile.write('{:>4d}\t{:0.2f}\t{:0.2f}\n'.format(iter_num, iter_time, mutual_info))
