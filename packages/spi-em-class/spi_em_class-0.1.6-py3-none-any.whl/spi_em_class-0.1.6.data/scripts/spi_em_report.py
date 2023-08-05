#!python
# -*- coding: utf-8 -*-

"""
Create PDF report for EM class data
Author: Sergey Bobkov
"""

import os
import argparse

from spi_em_class import em_data, pdfreport


def main():
    parser = argparse.ArgumentParser(description='Create PDF report for EM class data')
    parser.add_argument('-o', '--out', default=pdfreport.PDF_REPORT_NAME, help="Output file")
    parser.add_argument('-d', '--data', default=em_data.DEFAULT_DATA,
                        help='File with EM class data')
    parser_args = parser.parse_args()

    data_file = parser_args.data
    report_file = parser_args.out

    if not os.path.isfile(data_file):
        parser.error("File {} doesn't exist".format(data_file))

    pdfreport.create_pdf_report(data_file, report_file)


if __name__ == '__main__':
    main()
