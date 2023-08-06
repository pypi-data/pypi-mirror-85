from pylyglot.cslyglot import *
from pylyglot.lyglot import *

def convert(code):
    """
    This function converts CS code to Python
    :param code: text
    :return: cs->py
    """

    #General
    code=remove_semicolon(code)
    code=trim(code)

    #Tree processing
    _code_tree=code_tree(code)
    _code_tree=remove_tabs(_code_tree)
    _code_tree=remove_keywords(_code_tree)
    _code_tree=remove_blocks(_code_tree)
    _code_tree=paste_tabs(_code_tree)
    _code_tree=remove_brackets(_code_tree)
    _code_tree=translate(_code_tree)
    _code_tree=remove_types(_code_tree)
    _code_tree=paste_colons(_code_tree)
    _code_tree=replace_args(_code_tree)

    return "\n".join(_code_tree)