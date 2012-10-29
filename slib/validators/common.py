# -*- coding: utf-8 -*-


import re
import cjson

from . import ValidatorError


##### Public methods #####
def validBool(arg) :
    arg = str(arg).strip().lower()
    true_args_list = ("1", "true", "yes")
    false_args_list = ("0", "false", "no")

    if not arg in true_args_list + false_args_list :
        raise ValidatorError("Argument \"%s\" not in list %s or %s" % (arg, true_args_list, false_args_list))

    return ( arg in true_args_list )

def validNumber(arg, min_value = None, max_value = None, value_type = int) :
    if arg is None :
        raise ValidatorError("Empty argument is not valid a number")

    arg = str(arg).strip()

    try :
        arg = value_type(arg)
    except Exception :
        raise ValidatorError("Argument \"%s\" is not valid a number" % (arg))

    if min_value != None and arg < min_value :
        raise ValidatorError("Argument \"%s\" must be greater or equal than %d" % (arg, min_value))
    if max_value != None and arg > max_value :
        raise ValidatorError("Argument \"%s\" must be lesser or equal then %d" % (arg, max_value))
    return arg

def validRange(arg, valid_args_list) :
    if not arg in valid_args_list :
        raise ValidatorError("Argument \"%s\" not in range %s" % (str(arg), str(valid_args_list)))
    return arg

def validStringList(arg) :
    if arg is None :
        raise ValidatorError("Empty argument is not valid a string list")
    if type(arg) in (list, tuple) :
        return map(str, list(arg))
    return filter(lambda arg : len(arg) != 0, re.split(r"[,\t ]+", str(arg).strip()))

def validEmpty(arg) :
    if arg is None or (type(arg) in (str, unicode) and len(arg.strip()) == 0 ) :
        return None
    else :
        return arg

def validJson(arg) :
    if arg is None :
        raise ValidatorError("Empty argument is not valid a JSON structure")

    arg = str(arg).strip()
    try :
        return cjson.encode(cjson.decode(arg))
    except Exception, err :
        raise ValidatorError("Argument \"%s\" is not valid a JSON structure: %s" % (arg, str(err)))


