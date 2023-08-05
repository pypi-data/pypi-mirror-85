#!/usr/bin/env python
# Authors: Franz Knuth & Fawzi Mohamed
from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import str
from builtins import range
from builtins import object
import json
import numpy as np
import sys, re

def numpyDtypeForDtypeStr(dtypeStr):
    """returns the numpy dtype given the meta info dtype"""
    if dtypeStr == "f" or dtypeStr == "f64":
        return np.float64
    elif dtypeStr == "f32":
        return np.float32
    elif dtypeStr == "i" or dtypeStr == "i32":
        return np.int32
    elif dtypeStr == "i64":
        return np.int64
    elif dtypeStr == "b":
        return bool
    elif dtypeStr == "C":
        return object
    elif dtypeStr == "D":
        return object
    elif dtypeStr == "B":
        return object

def valueForStrValue(strValue, dtypeStr):
    """adds a value translating it from a string"""
    try:
        if dtypeStr[0] == "f":
            return float(strValue.replace("d","e").replace("D", "e"))
        elif dtypeStr[0] == "i":
            return int(strValue)
        elif dtypeStr[0] == "b":
            return (re.match("\s*(?:[nN][oO]?|\.?[fF](?:[aA][lL][sS][eE])?\.?|0)\s*$", strValue) is None)
        elif dtypeStr[0] == "B":
            return strValue # assumed to be base64 encoded
        elif dtypeStr[0] == "C":
            return strValue
        elif dtypeStr[0] == "D":
            return json.loads(strValue)
        else:
            raise Exception("unexpected dtypeStr %s" % (dtypeStr))
    except Exception as e:
        raise Exception("Error when converting %r to dtypeStr %r" % (strValue, dtypeStr), e)
