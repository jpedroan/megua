# -*- coding: iso-8859-15 -*-
# vim:fileencoding=iso-8859-15

r"""
Substitution on a given input text with named placeholders ('variables') by their respective values provided a dictionary.


AUTHORS:

- Pedro Cruz (2010-06): initial version
- Pedro Cruz (2011-08): documentation strings
- Pedro Cruz (2016-03): adpatation to SMC

Types of variables are:

1. ``name``: the ``name`` is directly substituted by the result of ``latex(value)`` where value is the value on the dict.
2. ``name@()``: substitution for ``\left( latex(value) \right)`` if value for name is negative (w.o. () otherwise).
3. ``name@f{2.3g}``: formatted substitution. In the example: substitution for ``"%2.3g" % value`` (this is a python expression).
4. ``name2@s{R15}``: function call substitution. In the example: substitution for ``R15(value)`` (R15 is a user function).
5. ``name3@c{"text0","text1",...}``: In the example, if name3 is 0 then "text0" will appear, if name3 is 1 then text1" will appear, and so on.


EXAMPLES:

.. test as a python module with:    sage -python -m doctest parse_param.py

An example of each kind::

The text "1) name  2) name2@() 3) name@f{2.3g} 4) name2@s{sin}" has 4 placeholders that will be changed.

.. sage output   Examples: 1) -12.1234560000000  2) \left(-34.3200000000000\right) 3) -12.1 4) -34.32
.. python output Examples: 1) -12.123456  2) \left(-34.32\right) 3) -12.1 4) -34.32

    
   sage: from megua.parse_param import parameter_change
   sage: txt = r'''Examples: 1) name  2) name2@() 3) name@f{2.3g} 4) name@s{sin} 5) name3@c{"text0", "tex-t1"}'''
   sage: newdict = {'name': -12.123456, 'name2': -34.32, 'name3': 1, '__init__': 'the init', 'self': 'the self' }
   sage: parameter_change(txt,newdict)
   u'Examples: 1) -12.1234560000000  2) (-34.3200000000000) 3) -12.1 4) 0.42857465435 5) tex-t1'
   sage: newdict = {'name3': 1 }
   sage: txt = u'''1) name3@c{"text0", "c\xc3o"} 2) name3@c{"n\xc3o", "name1"} 3) name3@c{"nop", "text2"} '''
   sage: parameter_change(txt,newdict)
   u'1) c\xc3o 2) name1 3) text2 '
   sage: txt = u''' name3@c{"m\xe1ximo", "m\xednimo"} '''
   sage: parameter_change(txt,newdict)
   u' m\xednimo '

#TODO: parse_parm: example that not work because it needs spaces before and after the string
#   sage: txt = u'''name3@c{"maximo", "minimo"}'''
#   sage: parameter_change(txt,newdict)





IMPLEMENTATION NOTES:

1. If this module is modified to a pure Python module then:
   a. sage -python -m doctest parse_param.py
   b. In Python the example could return "Examples: 1) -12.123456  2) (-34.32) 3) -12.1 4) R15(-34.32)"


REGEX DEFINITIONS:

    Consider this examples:   ``"1) name  2) name2@() 3) name@f{2.3g} 4) name2@s{R15} 5) name3@["text0","text1"] "``. 
    Fields in the regex are for the example are separed in this way:

    * Groups in example 1): (None, None, None, None, None, None, None, 'name')
    * Groups in example 2): ('name2', None, None, None, None, None, None, None)
    * Groups in example 3): (None, 'name', '2.3g', None, None, None, None, None)
    * Groups in example 4): (None, None, None, 'name2', 'R15', None, None, None)
    * Groups in example 5): (None, None, None, 'name2', None, 'name3', '["text0","text1"]', None)

    Detailed description:
    * g0: is the full match
    * g1: name of var that needs () if negative value (otherwise None)
    * g2,g3: name using @f and args (otherwise None,None)
    * g4,g5: name using @s and args (otherwise None,None)
    * g6,g7: name and list of possibilities ["text0","text1"].
    * g8: name without format

    NOTES:
    1. dd must be on end
    2. '\W(' + dd + ')' = a key must be preceeded by a non alphanumeric character
    3. Does not work to do: \W(' + dd + ')\W' because in this case two characters are needed for each dd name. User must be warned of this.

    \W: If UNICODE is set, this will match anything other than [0-9_] and characters marked as alphanumeric in the Unicode character properties database.
    \w: If UNICODE is set, this will match the characters [0-9_] plus whatever is classified as alphanumeric in the Unicode character properties database.



LINKS:

1. See Python MatchObject
2. http://docs.python.org/library/string.html#formatexamples(

FUTURE. Evaluate if any of this forms is really useful::

    name
    @R15(name)
    @round(name,2)
    @(name)
    @["2.3g".format(name)]
    @[t=name1+name2;round(name,2)] ->
    @integrate(f,x) -> (1/2)x^2
    @(name[0],name[1])-> (10.2,23.3)
    @(integrate(f,x),f.diff(x)) -> ((1/2)x^2,1)


"""


# PYTHON modules
import re



# MEGUA modules
# Named placeholders need functions in mathcommon: latex, R15, ...
from megua.mathcommon import *


#TODO: answer this
# Why is this here?
#from sage.symbolic.expression import is_Expression


#See expression1() below
#TODO: improve for cases without space: $n@$ ($), $n@+40$ (operators +-*/), etc 
#old prog = re.compile(r'(\w+)@(\s|\(\)|\[(.*)\]|{(.*)})',re.MULTILINE|re.DOTALL|re.IGNORECASE)




#ReEX definition:
BASE_REGEX = ur'\W(\w+)@\(\)|'\
             ur'\W(\w+)@f\{([\.#bcdeEfFgGnosxX<>=\^+\- 0-9\%]+)\}|'\
             ur'\W(\w+)@s\{(\w+)\}|'\
             ur'\W(\w+)@c\{(.+?)\}|'  #"|" means this expression will continue below


#             ur'\W(\w+)@c\{([\\~\'\s",\-\w\.]+)\}|'  #"|" means this expression will continue below


#Original REGEX definition:
#re_str = r'\W(\w+)@\(\)|'\
#         r'\W(\w+)@f\{([\.#bcdeEfFgGnosxX<>=\^+\- 0-9\%]+)\}|'\
#         r'\W(\w+)@s\{(\w+)\}|'\
#         r'\W(\w+)@c\{([\s",\-\w\.]+)\}|' + \
#         r'\W(' + c_dict_keys + ')'


"""
When ExBase.search_replace is called
it will output values using some "global" method
Decorators, inside txtual sources, can change this
default behaviour.
"""
EXPR2LATEX = 0x1 #sage.symbolic.expression.Expression to latex
DEFAULT_OUTPUT_METHOD = EXPR2LATEX


#Avoid this members in exercise
AVOID_KEYWORDS = ['self', 'imagedirectory', 'image_relativepathnames', 'image_fullpathnames', 'has_instance', 'ekey', 'dpi', 'dimy', 'dimx', 'working_dir']



def parameter_change(inputtext,datadict):
    """
    Substitution on a given input text with names acting as placeholders by their values on a provided dict.

    INPUT:
    
    - ``inputtext``-- text containing an exercise template with named placeholders.
    - ``datadict`` -- a dictionary with the names that will be changed by values.

    OUTPUT:
    
    - text where names where replaced by values.

    See examples at top of the file.
    Implementation details below.

    """

    #Create regex using datadict names
    keys_no_keyword = [ v for v in datadict.keys() if v[0]!='_' and v not in AVOID_KEYWORDS] 

    #Reverse: why is important.
    #This reversed sort guarantees that 'onb1' is first changed and only then 'onb'.
    #Otherwise, if key onb1 appear,  "onb" will be first replaced leaving '1' in the text.
    keys_no_keyword.sort(reverse=True) 
    c_dict_keys = "|".join( keys_no_keyword ) #see use below.
    re_str = BASE_REGEX + ur'\W({0})'.format(c_dict_keys)


    #TODO: maybe this should be above.
    #print "type=",type(inputtext)
    if type(inputtext) == str:
        inputtext = unicode(inputtext,'utf-8')


    #re.MULTILINE|re.DOTALL|re.IGNORECASE|re.|
    match_iter = re.finditer(re_str,inputtext,re.UNICODE|re.LOCALE)


    #Debug
    #import unicodedata
    #print "UNICODE DATA FOR REGEX:----------------"
    #for i, c in enumerate(inputtext):
    #    print i, '%04x' % ord(c), unicodedata.category(c),
    #    print unicodedata.name(c)

    outputtext = u""

    text_last = 0

    for match in match_iter:
        
        
        #if type(inputext) == unicode:
        #    print "Full match group(0) is: " + unicode(match.group(0))
        #    print "Groups(1..n) in this match: " + match.groups())

        try:

            if match.group(1) is not None:
                
                #CASE: name@()
                #Get data from dict for this match
                keyname = match.group(1)
                data_value = datadict[keyname]    #; print "data_value=",data_value
                outputtext += inputtext[text_last:match.start()+1]
                outputtext += output_value(data_value,DEFAULT_OUTPUT_METHOD,parentesis=True)
                
            elif match.group(2) is not None and match.group(3) is not None:
                
                #CASE: name@f{0.2g}
                keyname = match.group(2)
                data_value = datadict[keyname]
                format_text = r"%" + match.group(3)
                formated_argument = format_text % data_value
                outputtext += inputtext[text_last:match.start()+1] + formated_argument
                
            elif match.group(4) is not None and match.group(5) is not None:
                
                #CASE: name@s{RealField15}
                keyname = match.group(4)
                data_value = datadict[keyname]
                sage_command = match.group(5) + '(' + str(data_value) +')'
                ev = eval(sage_command,globals())
                outputtext += inputtext[text_last:match.start()+1] + str(ev)
                
            elif match.group(6) is not None and match.group(7) is not None:
                
                #print """parse_param.py: CASE: name@c{"text0","text1"}"""
                #print "match.group(6)=",match.group(6)
                #print "match.group(7)=",match.group(7)
                
                try:
                    #create list with user given strings:
                    #name@c{"text0","text1"} --> ["text0","text1"]
                    str_uni = u"[" + match.group(7) + u"]"
                    #print "parse_param.py: ",str_uni
                    str_list = eval( str_uni )
                    
                    #get value of 'name'
                    keyname = match.group(6)
                    data_value = datadict[keyname]
                    #get string from the list
                    str_value = str_list[data_value]

                    #TODO: Check if rmeove this is ok
                    #if str_value in datadict:
                    #    data = datadict[str_value]
                    #    if type(data) == str:
                    #        str_value = unicode(datadict[str_value],'utf-8')
                    #    else:
                    #        str_value = data
                    #else:
                    #    if type(str_value) == str:
                    #        str_value = unicode(str_value,'utf-8')

                except SyntaxError as e:
                    #value = keyname
                    print """parse_param.py: syntax problem on name@c{"text0","text1"}. Text say: %s.""" % match.group(7)
                    raise SyntaxError(e)
                except NameError as e:
                    #value = keyname
                    print "parse_param.py: use double quotes even on names (case: %s in '%s')." % (e,match.group(7))
                    raise NameError(e)
                #print type(str_value), " ", str_value
                if type(str_value) == str:
                    str_value = unicode(str_value,'utf-8')
                outputtext += inputtext[text_last:match.start()+1] + str_value
                
            else: #same as if match.group(5) is not None
            
                #CASE: name wihtout formating
                keyname = match.group(8)
                data_value = datadict[keyname]
                if type(data_value) is str:
                    outputtext += inputtext[text_last:match.start()+1] + unicode(data_value,'utf8')
                elif type(data_value) is unicode:
                    outputtext += inputtext[text_last:match.start()+1] + data_value
                else:
                    outputtext += inputtext[text_last:match.start()+1] 
                    outputtext += output_value(data_value,DEFAULT_OUTPUT_METHOD)
                    
        except KeyError:
            
                #outputtext += inputtext[text_last:match.start()+1] + unicode(keyname,'utf-8')
                outputtext += inputtext[text_last:match.start()+1] + keyname

        text_last = match.end()            

    outputtext += inputtext[text_last:]

    return outputtext




def output_value(s,output_method=None,parentesis=False):
    r"""Return a unicode string with the 
        value or expression ``s`` 
        or some transformation of it.

    INPUT:
    
    - ``s'': an expression or value
    - ``output_method'': a sequence of bits (see EXPR2LATEX at the top of the file)
    - ``parentesis'': to write out or not parentesis

    OUTPUT:
    
    - an unicode utf8 string appropriatedly formated.
    
    """

    #old def ulatex(...)
    #TODO: var@l => force latex(var)
    #TODO: improve this function
    #print type(s)

    #convert the value into a string
    if output_method & EXPR2LATEX:
        s_str = unicode(latex(s),'utf-8')
    else:
        s_str = unicode(str(s),'utf-8')
    
    if parentesis and bool(s<0):

        if type(s)==sage.symbolic.expression.Expression:
            return ur'\left(' + s_str + ur'\right)'
        else:
            return r'(' + s_str + r')'
            
    else:
        
        return s_str  #unicode(s,'utf-8')


"""
Helper functions
"""

def test1():
    """
    Regular Expression number 1

    group 0: full match
    group 1: name
    group 2: format
    group 3: {...} format
    group 4: s{...} format
    """

    text = """ 
    START
        1) name@ 
        2) name@()
        3) name@{x,a.s}
        4) name@s{md,d.d,}
    END
    """

    #prog = re.compile(r'(\w+)@(\s|\(\)|{(.*)}|s{(.*)})')

    match_iter = re.finditer(prog,text)

    for match in match_iter:
        print "Groups in here: " + str(match.groups())
        print text[match.start():match.end()]
        print "Group = " + str(match.group(0))
        print "Group = " + str(match.group(1))
        print "Group = " + str(match.group(2))
        print "Group = " + str(match.group(3))
        print "Group = " + str(match.group(4))
        print




#if __name__=='__main__':
#    """Testing with 
#        python -doctest 
#    """
#    test1()



