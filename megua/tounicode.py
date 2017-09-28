# coding=utf-8

r"""
ExerciseBase - This module defines the base class for exercise templating.

To build a database of exercise templates read details of module ``megbook``.
 

AUTHORS:

- Pedro Cruz (2016-01): refactoring for SMC.


"""



def to_unicode(s):
    if type(s)!=unicode:
        res = unicode(s,'utf-8')
    else:
        res = s
    #print "tounicode.py: type(res)=", type(res)
    #print "tounicode.py: codes in res=",[ord(c) for c in res]
    return res
