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
import pandas as pd
from ream.transformer import Ream2Dict
from ream.grammar import REAM_RULE

def ream2dict(input_raw, output_file=None, debug=False, no_comment=False):
    """ream to json"""

    if no_comment:
        Ream2Dict.no_comment = True
    else:
        Ream2Dict.no_comment = False

    input_tree = REAM_RULE.parse(input_raw)
    output_raw = Ream2Dict().transform(input_tree)

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
        print(json.dumps(output_raw, indent=4))
        return None



def ream2list(input_raw):

    data = ream2dict(input_raw, no_comment=True)


    def flatten(d):
        parent = []
        children = []
        for value in d.values():
            if type(value) == list:
                for subentry in value:
                    new = flatten(subentry)
                    if type(new[0]) == list:
                        for subsub in new:
                            children.append(subsub)
                    else:
                        children.append(new)
            else:
                parent.append(value)
        if children:
            result = [ parent + child for child in children ]
        else:
            result = parent
        return result

    return(flatten(data))


def ream2csv(input_raw, output_file):

    list_raw = ream2list(input_raw)

    with open(output_file, 'w') as file:
        colname = ",".join([str(x) for x in range(len(list_raw[0]))])
        file.write(colname)
        file.write('\n')
        for entry in list_raw:
            file.write(",".join(entry))
            file.write('\n')

def ream2df(data):
    return pd.DataFrame(ream2list(data))

def main(input_raw, output_file, debug, no_comment):
    """
    main function for decoding ream file
    """

    output_ext = output_file.split('.')[-1]

    # choose conversion function
    if output_ext in ['json']:
        ream2dict(input_raw, output_file, debug, no_comment)
    elif output_ext in ['csv']:
        ream2csv(input_raw, output_file)
    else:
        print("Output file formet not supported")
    print("Complete")
