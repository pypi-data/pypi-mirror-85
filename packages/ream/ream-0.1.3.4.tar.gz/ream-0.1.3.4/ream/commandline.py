"""
REAM: REAM Ain't Markdown
~~~~~~~~~~~~~~~~~~~~~~~~~

This file is part of the ream package

:copyright: Copyright 2020 by Chih-Ming Louis Lee
:license: MIT, see LICENSE for details

"""
import os
import sys
import argparse
import ream.decode
import ream.encode

def parse_arg():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='REAM decoder and encoder')

    parser.add_argument('--input', metavar='FILENAME', required=True,
                        help='input file')

    parser.add_argument('--output', metavar='FILENAME', required=False,
                        help='output file')

    parser.add_argument('--no-comment', action='store_true', dest="no_comment",
                        help='ignore comments')

    parser.add_argument('--debug', '-d', action='store_true',
                        help='print debug info')

    parser.add_argument('--force', '-f', action='store_true',
                        help='overwrite existing output files')

    arg = parser.parse_args()
    return arg


def main():
    """
    main entry point
    """

    arg = parse_arg()

    # check whether input file exist
    if not os.path.exists(arg.input):
        print("Input file not found. Make sure you enter a valid path.")
        sys.exit()

    # read input file
    with open(arg.input, 'r') as file:
        input_raw = file.read()

    # check whehter output file exist
    if os.path.exists(arg.output) and not arg.force:
        print("Output file exists. To overwrite, add --force flag")
        sys.exit()

    # decode or encode
    input_ext = arg.input.split('.')[-1]
    if input_ext in ['md', 'ream']: # decode
        ream.decode.main(
            input_raw=input_raw,
            output_file=arg.output,
            debug=arg.debug,
            #force=arg.force,
            no_comment=arg.no_comment
        )
    else: # encode
        ream.encode.main(
            input_file=arg.input,
            input_ext=input_ext,
            output_file=arg.output,
            #debug=arg.debug,
            #force=arg.force,
            #no_comment=arg.no_comment
        )
