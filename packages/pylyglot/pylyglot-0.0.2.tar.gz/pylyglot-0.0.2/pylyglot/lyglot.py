import difflib

def similar(a, b):
    """
    This function is about similarity of strings
    :param a: first string
    :param b: second string
    :return: ratio similarity between two strings
    """
    return difflib.SequenceMatcher(None, a, b).ratio()

def remove_semicolon(code):
    """
    This function removes semicolons from the whole text
    :param code: text
    :return: text without semicolons
    """
    return code.replace(";","")

def trim(code):
    """
    This function remove tabs and left/right spaces
    :param code: text
    :return: text without tabs
    """
    return code.strip().replace("\t", "")

def code_tree(code):
    """
    This function converts text to tree as a list
    :param code: text
    :return: each line tokens in a list
    """
    return [i for i in code.split("\n") if i != ""]