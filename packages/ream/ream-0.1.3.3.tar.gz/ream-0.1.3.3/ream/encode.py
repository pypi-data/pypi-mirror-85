"""
REAM: REAM Ain't Markdown
~~~~~~~~~~~~~~~~~~~~~~~~~

this file is part of the ream package

:copyright: Copyright 2020 by Chih-Ming Louis Lee
:license: MIT, see LICENSE for details

"""
import json
import re

def json2ream(input_file, output_file):
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
                            for key_1, value_1 in d_raw_1.items():
                                write_newline(": ".join([key_1, value_1]))
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

def main(input_file, input_ext, output_file):
    "main function for encoding ream file"

    if input_ext in ['json']:
        json2ream(input_file, output_file)
    else:
        print("Input file format not supported.")
    print("Complete")
