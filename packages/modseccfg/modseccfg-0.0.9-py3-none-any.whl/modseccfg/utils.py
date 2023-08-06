# encoding: utf-8
# api: python
#
# Monkeypatching some Python modules, and some convenience wrappers


#-- path
from pathlib import Path as path
def expandpath(dir):
    return str(path(dir).expanduser())


#-- patch re
import re
def re_compile(regex, *kargs, **kwargs):
    if type(regex) is str:
        regex = re.sub('\\\\h', '[\\ \\t\\f]', regex)
    return re.compile_orig(regex, *kargs, **kwargs)
re.compile_orig = re.compile
re.compile = re_compile

def re_grep(regex, list):
    return (s for s in list if re.search(regex, s))
re.grep = re_grep


#-- import frosch for prettier exceptions
try:
    import frosch
    frosch.hook()
except:
    pass

