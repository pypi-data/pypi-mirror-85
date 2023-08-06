"""
REAM: Ream Ain't Markdown
~~~~~~~~~~~~~~~~~~~~~~~~~

this file is part of the ream package

:copyright: Copyright 2020 by Chih-Ming Louis Lee
:license: MIT, see LICENSE for details

"""
import re
import ast
from lark import Transformer

class Ream2Dict(Transformer):
    """
    something
    """

    no_comment = False

    def meta_wrapper(self, wrapper):
        # output_dict = yaml.safe_load("".join([f"{x}\r" for x in wrapper]))
        return ["__metadata__", output_dict]

    def META(self, meta):
        return meta

    def COMMENT(self, comment):
        if self.no_comment:
            return ""
        else:
            return comment[2:] # strip leading "> "

    def STRING(self, string):
        number_rule = r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$'
        if string[0] == '$' and string[-1] == '$': # number
            string = re.sub("_", "", string[1:-1])
            if re.compile(number_rule, re.UNICODE).match(string):
                return string
                #return ast.literal_eval(string)
        elif string[0] == '`' and string[-1] == '`': # command
            if string == '`TRUE`':
                return 'TRUE'
            if string == '`FALSE`':
                return 'FALSE'
            if string == '`NA`':
                return 'NONE'
        return string

    def NAME(self, name):
        return name[:]

    def KEY(self, key):
        return key[:-1] # strip trailing ":"

    def h_wrapper(self, wrapper):
        """
        wrapper[0]: entry name
        wrapper[1:]: content
        """
        name = wrapper[0]
        output_dict = {}
        for item in wrapper[1:]:
            # item[0]: key
            # item[1]: value
            # check value type
            key = item[0]
            value = item[1]
            val_type = type(value)
            if val_type != dict:
                output_dict[key] = value
            else: # dictionary !
                if key not in output_dict:
                    output_dict[key] = [value]
                else:
                    output_dict[key].append(value)
        return (name, output_dict)

    h1_wrapper = h_wrapper
    h2_wrapper = h_wrapper
    h3_wrapper = h_wrapper
    h4_wrapper = h_wrapper
    h5_wrapper = h_wrapper
    h6_wrapper = h_wrapper

    def start(self, everything):
        output_dict = {}
        for item in everything:
            # item[0]: key
            # item[1]: value
            # check value type
            key = item[0]
            value = item[1]
            val_type = type(value)
            if val_type != dict:
                output_dict[key] = value
            else: # dictionary !
                if key not in output_dict:
                    output_dict[key] = [value]
                else:
                    output_dict[key].append(value)
        return output_dict

    def value(self, val):
        """
        One of the following types:
            string_wrapper
            star_list
        """
        return val[0]

    def string_wrapper(self, wrapper):
        """
        wrapper[0]: STRING
        wrapper[1]: COMMENT (Optional)
        join the two as a string, separate by "__COM__"
        """
        if self.no_comment:
            string_output = wrapper[0]
        else:
            wrapper[0] = str(wrapper[0])
            string_output = "__COM__".join(wrapper)
        return string_output

    def variable(self, var):
        """
        var[0]: KEY
        var[1]: value
        """
        return (var[0], var[1])

    def element(self, elem):
        try:
            string_output = "__COM__".join(elem)
        except IndexError:
            string_output = elem[0]
        return string_output

    def star_list(self, s_list):
        return s_list
