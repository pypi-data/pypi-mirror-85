"""
REAM: REAM Ain't Markdown
~~~~~~~~~~~~~~~~~~~~~~~~~

This file is part of the ream package

:copyright: Copyright 2020 by Chih-Ming Louis Lee
:license: MIT, see LICENSE for details

"""
import sys
import os
import re
import json
import yaml
from .transformer import Ream2Json
from .grammar import REAM_RULE

def ream2json(input_file, output_file=None, debug=False, no_comment=False):
    """ream to json"""

    with open(input_file, 'r') as file:
        input_raw = file.read()

    if no_comment:
        Ream2Json.no_comment = True
    else:
        Ream2Json.no_comment = False

    input_tree = REAM_RULE.parse(input_raw)
    output_raw = Ream2Json().transform(input_tree)

    if debug:
        print(input_tree)
        print("====================")
        print(input_tree.pretty())
        print("====================")
        print(output_raw)
        print("====================")

    if output_file is None:
        return output_raw
    else:
        with open(output_file, 'w') as file:
            json.dump(output_raw, file)
        #print(json.dumps(output_raw, indent=4))


def json2ream(input_file, output_file=None):
    """json to ream"""

    def write_newline(line, output_file=output_file):
        with open(output_file, "a") as file:
            file.write("".join([line, "\n"]))

    def write_comment(comment):
        write_newline("")
        write_newline("".join(["> ", comment]))
        write_newline("")

    def check_comment(string):
        if len(re.findall("__COM__", string)) == 0:
            output_string = string
            comment = ""
        else:
            output_string, comment = string.split("__COM__")
        return output_string, comment

    def write_header(header_name, level_num):
        write_newline("")
        new_header = "".join(["#" for _ in range(level_num)] + [f" {header_name}"])
        write_newline(new_header)

    def write_variable(key, var_raw):
        var, comment = check_comment(var_raw)
        newline = "".join(["- ", key, ": ", var])
        write_newline(newline)
        if comment != "":
            write_comment(comment)

    def write_starlist(key, star_list):
        write_variable(key, "")
        for item_raw in star_list:
            item, comment = check_comment(item_raw)
            new_item = "".join(["  * ", item])
            write_newline(new_item)
            if comment != "":
                write_comment("".join(["  ", comment]))

    def json2ream_inner(d_raw, count=0):
        for key in d_raw:
            val = d_raw[key]
            if isinstance(val, (str)): # variable
                write_variable(key, val)
            else:
                if isinstance(val[0], str): # list
                    write_starlist(key, val)
                else:
                    count += 1
                    for d_raw_1 in val:
                        ########### generate metadata ##########
                        if key == "__metadata__":
                            write_newline("---")
                            for k, v in d_raw_1.items():
                                write_newline(": ".join([k, v]))
                            with open(output_file, "a") as file:
                                file.write("---")
                        ########################################
                        else:
                            write_header(key, count)
                            json2ream_inner(d_raw_1, count)
                    count -= 1

    with open(input_file) as json_file:
        j_raw = json.load(json_file)

    json2ream_inner(j_raw)

def convert(input_file, output_file, debug=False, force=False, no_comment=True):
    """
    read and convert files
    """

    if no_comment:
        print(no_comment)

    # check whether input file exist
    if not os.path.exists(input_file):
        print("Input file not found. Make sure you enter a valid path.")
        sys.exit()

    # check whether output file exist
    if os.path.exists(output_file) and force == False:
        print("Output file exists. To overwrite it, add --force flag")
        sys.exit()

    # read file type
    input_ext = input_file.split('.')[-1]
    output_ext = output_file.split('.')[-1]

    # choose conversion function
    if input_ext in ["ream", "md"]:
        if output_ext in ["json"]:
            ream2json(input_file, output_file, debug, no_comment)

    elif input_ext in ["json"]:
        if output_ext in ["ream", "md"]:
            json2ream(input_file, output_file)

    else:
        pass
