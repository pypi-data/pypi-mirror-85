"""
REAM: Ream Ain't Markdown
~~~~~~~~~~~~~~~~~~~~~~~~~

this file is part of the ream package

:copyright: Copyright 2020 by Chih-Ming Louis Lee
:license: MIT, see LICENSE for details

"""
from lark import Lark

REAM_RULE = Lark(r"""
    start: _NL? meta_wrapper? h1_wrapper*

    _DASH:     "- "
    _STAR:     "*"
    _TRI_DASH: "---"
    _HEADER_1: "#"
    _HEADER_2: "##"
    _HEADER_3: "###"
    _HEADER_4: "####"
    _HEADER_5: "#####"
    _HEADER_6: "######"

    meta_wrapper: _TRI_DASH META+ _TRI_DASH
    META: /.+/


    h1_wrapper: _HEADER_1 NAME _NL* variable* h2_wrapper*
    h2_wrapper: _HEADER_2 NAME _NL* variable* h3_wrapper*
    h3_wrapper: _HEADER_3 NAME _NL* variable* h4_wrapper*
    h4_wrapper: _HEADER_4 NAME _NL* variable* h5_wrapper*
    h5_wrapper: _HEADER_5 NAME _NL* variable* h6_wrapper*
    h6_wrapper: _HEADER_6 NAME _NL* variable*

    NAME: /.+/

    variable: _DASH KEY value _NL*
    KEY:   /.+:/
    value: string_wrapper
         | star_list

    string_wrapper: STRING (COMMENT)*
    STRING: /[^\*].*/
    COMMENT: / *>.+/

    star_list: (_STAR element)+ _NL*
    element: STRING (COMMENT)*



    %import common.NEWLINE -> _NL
    %import common.WS
    %ignore WS

""", parser="lalr")
