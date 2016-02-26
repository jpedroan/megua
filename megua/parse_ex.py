# -*- coding: iso-8859-15 -*-

r"""
Convert an input text containing an exercise template into a tuple ``(unique_name,txt_summary,txt_problem,txt_answer,txt_class)`` extracted from text.
See ``exer_parse`` function.


AUTHORS:

- Pedro Cruz (2011-06): initial version
- Pedro Cruz (2011-08): documentation string as tests.
- Pedro Cruz (2016-02): Prepare for SMC.


IMPLEMENTATION NOTES:

* Test with ``sage -t paramparse.py``.
* This is a pure Python module that can be adapted to a windows ``meg`` system using Sympy for example.

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

#PYTHON  modules
import re

#MEGUA modules
from megua.tounicode import to_unicode


#Old form
#prog = re.compile(ur'%SUMMARY(.+)%PROBLEM(.+)%ANSWER(.+)^(class (\w+)\(Exercise\):.+)',re.MULTILINE|re.DOTALL|re.IGNORECASE|re.U)


class ExState:
    STARTING_BLANKS=0
    SUMMARY=1
    PROBLEM=2
    ANSWER=3
    CLASS=4


#str.splitlines([keepends])
#file:///home/jpedro/Downloads/python-2.6.4-docs-html/library/stdtypes.html#string-methods


re_blanks = re.compile(ur'[ \t]*\n',re.U)

re_summary = re.compile(ur'[ \t]*%[ \t]*summary[ \t]*(.*)\n',re.IGNORECASE|re.U)
re_problem = re.compile(ur'[ \t]*%[ \t]*problem[ \t]*(.*)\n',re.IGNORECASE|re.U)
re_answer = re.compile(ur'[ \t]*%[ \t]*answer[ \t]*(.*)\n',re.IGNORECASE|re.U)

#Includes grammar for class name in form: E dd letter dd
#re_class = re.compile(ur'^class[ \t]+(E(\d\d(\b|[\-a-zA-Z])(\b|\d\d))_\w+_\d+)\(Exercise\):\s*',re.U)
#In this re_class the prefix is less rigorous.
re_class = re.compile(ur'^class[ \t]+(E([a-zA-Z0-9]+)_\w+_\d+)\(\w+\):\s*',re.U)

re_wrongclass = re.compile(ur'[ \t]*class[ \t]+(.+):\s*',re.U)

re_rest = re.compile(ur'.+',re.U)



class LineToken:
    """
    The command ``LineToken(lineno,linetag,lineinfo,completeline)`` creates a tuple with:

    - ``lineno`` -- is the line number in the original text.
    - ``linetag``-- is the type of contens of the line: see re_* expressions above.
    - ``lineinfo``-- for each type cna be information that needs to be available.
    - ``completeline`` -- the complete original text line.

    """ 

    def __init__(self,lineno,linetag,lineinfo,completeline):
        self.lineno = lineno
        self.linetag = linetag
        self.lineinfo = lineinfo
        self.completeline = completeline

    def __repr__(self):
        return "LineToken(%d,%s,%s,%s)" % (self.lineno, self.linetag, self.lineinfo, self.completeline)


    def __str__(self):
        return "LineToken(%d,%s,%s)\n%s" % (self.lineno, self.linetag, self.lineinfo, self.completeline)


def emptyifnone(txt):
    if txt is None:
        return ""
    else:
        return txt



def classify(no,line):
    """
    Parse a line and return the type of the line contents and other information.

    INPUT:
    - ``no`` -- is the line number.
    - ``line`` -- a line of text.

    OUTPUT:
        A LineToken tuple.
    """

    if re_blanks.match(line):
        return LineToken(no,'re_blanks',None,line)

    mobj = re_summary.match(line)
    if mobj is not None:
        return LineToken(no,'re_summary',mobj.group(1),line)

    mobj = re_problem.match(line)
    if mobj is not None:
        return LineToken(no,'re_problem',mobj.group(1),line)

    mobj = re_answer.match(line)
    if mobj is not None:
        return LineToken(no,'re_answer',mobj.group(1),line)

    mobj = re_class.match(line)
    if mobj is not None:
        return LineToken(no,'re_class',[mobj.group(1),mobj.group(2)],line)

    mobj = re_wrongclass.match(line)
    if mobj is not None:
        return LineToken(no,'re_wrongclass',mobj.group(1),line)

    #if re_rest.match(line):
    return LineToken(no,'re_rest',None,line)



def flex(txt):
    """
    Breaks input ``txt`` in a list of lines.
    Classify each line adding it tag type.

    INPUT:
    - ``txt`` -- full text.
    OUTPUT:
        A list of LineToken instances (one for each line).

    """

    #Break txt in lines
    lines = txt.splitlines(True) #including \n

    classlines = []

    #Classify each line
    for no,line in enumerate(lines):
        classlines.append( classify(no,line) )

    return classlines



def parse_ex(inputtext):
    r"""
    Convert ``inputtext`` into a tuple ``(unique_name,txt_summary,txt_problem,txt_answer,txt_class)`` extracted from text.

    INPUT:
    - ``inputext``-- text in the form "%summary...". See top of file.

    OUTPUT:
        A tuple ``(unique_name,txt_summary,txt_problem,txt_answer,txt_class)`` or None if there errors. Errors will be printed (``print``).

    ALGORITHM:

    0. absorbing initial blanks
    1. absorbing summary
    2. absorbing problem
    3. absorbing answer
    4. absorbing class

    EXAMPLES:

    ... OLD test with: sage -python -m doctest parse_ex.py

    sage -t parse_ex.py
    
    
    Example of the standard situation::

    sage: from megua.parse_ex import parse_ex
    sage: parse_ex(r'''
    ....: %summary Section
    ....:  My summary.
    ....: %problem Suggestive Textual Name
    ....:  My Problem.
    ....: %answer
    ....:  My answer.
    ....: class E12A34_name_001(ExerciseBase):
    ....:   more lines here''')
    {'answer_text': '\n My answer.\n',
     'class_text': 'class E12A34_name_001(ExerciseBase):\n  more lines here',
     'problem_text': '\n My Problem.\n',
     'sections_text': 'Section',
     'suggestive_name': 'Suggestive Textual Name',
     'summary_text': '\n My summary.\n',
     'unique_name': 'E12A34_name_001'}
     

    Example when there are comments in front of tags::

    sage: parse_ex(r'''
    ....: %summary Section
    ....:      My summary.
    ....: %problem Suggestive Textual Name
    ....:      My Problem.
    ....: %answer Answer Comment
    ....:     My answer.
    ....: class E12A34_name_001(ExerciseBase):
    ....:       more lines ''')
    Ignoring text 'Answer Comment' in %answer tag at line 6.
    <BLANKLINE>
    {'answer_text': '\n    My answer.\n',
     'class_text': 'class E12A34_name_001(ExerciseBase):\n      more lines ',
     'problem_text': '\n     My Problem.\n',
     'sections_text': 'Section',
     'suggestive_name': 'Suggestive Textual Name',
     'summary_text': '\n     My summary.\n',
     'unique_name': 'E12A34_name_001'}

    Example when class name is malformed::

    sage: parse_ex(r'''
    ....: %summary
    ....:      My summary.
    ....: %problem
    ....:      My Problem.
    ....: %answer
    ....:      My answer.
    ....: class name_001(ExerciseBase):
    ....:       more lines ''')
    Each exercise can belong to a section/subsection/subsubsection. 
    Write sections using ';' in the '%summary' line. For ex., '%summary Section; Subsection; Subsubsection'.
    <BLANKLINE>
    Each problem can have a suggestive name. 
    Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.
    <BLANKLINE>
    Expected python/sage class definition on line 8 or class identifier is wrong.
    Class identifier must follow a name like: E12A34_somename_number.
    """

    #Parse each line to LineToken "lines"
    classlines = flex(inputtext)

    current = 0
    numlines=len(classlines)

    state = ExState.STARTING_BLANKS

    error_found = False

    while current<numlines and not error_found:

        tag = classlines[current].linetag

        #Debug:
        #print "=================="
        #print classlines[current]

        if state == ExState.STARTING_BLANKS: #consume blanks
            #Check transition
            if tag == 're_blanks':
                #action
                current+=1
            elif tag  == 're_summary':
                state = ExState.SUMMARY
                if classlines[current].lineinfo is not None:
                    txtinfo = classlines[current].lineinfo.strip()
                    if txtinfo == '':
                        print "Each exercise can belong to a section/subsection/subsubsection. \n"\
                              "Write sections using ';' in the '%summary' line. For ex., '%summary Section; Subsection; Subsubsection'.\n"
                    txt_sections = txtinfo
                #TODO review: txt_summary = '\n%summary ' + txtinfo + '\n'
                txt_summary = '\n'
                current+=1
            else:
                error_found = True
                print "Expected %summary tag on line {0}.".format(current+1)

        elif state == ExState.SUMMARY: #consume summary lines
            #Check transition
            if tag  == 're_blanks' or tag  == 're_rest':
                #action
                txt_summary += classlines[current].completeline
                current+=1
            elif tag  == 're_problem':
                #action
                state=ExState.PROBLEM
                txt_problem = '' #TODO review '\n%problem\n'
                if classlines[current].lineinfo is not None:
                    txtinfo = classlines[current].lineinfo.strip()
                    if txtinfo == '':
                        print "Each problem can have a suggestive name. \n"\
                              "Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.\n"
                    txt_problemname = txtinfo
                #TODO Review this txt_problem = '\n%problem ' + txtinfo + '\n'
                txt_problem = '\n'
                current+=1
            else:
                error_found = True
                print "Expected %problem tag on line {0}.".format(current+1)

        elif state == ExState.PROBLEM: #consume problem lines
            #Check transition
            if tag  == 're_blanks' or tag  == 're_rest':
                #action
                txt_problem += classlines[current].completeline
                current+=1
            elif tag  == 're_answer':
                #action
                state=ExState.ANSWER
                txt_answer = '\n' #TODO review '\n%answer\n'    
                if classlines[current].lineinfo is not None:
                    txtinfo = classlines[current].lineinfo.strip()
                    if  txtinfo != '':
                        print "Ignoring text '" + txtinfo + "' in %answer tag at line {0}.\n".format(current+1)
                current+=1
            else:
                error_found = True
                print "Expected %answer tag on line {0}.".format(current+1)

        elif state == ExState.ANSWER: #consume answer lines
            #Check transition
            if tag  == 're_blanks' or tag  == 're_rest':
                #action
                txt_answer += classlines[current].completeline
                current+=1
            elif tag  == 're_class':
                #action
                state=ExState.CLASS
                unique_name = classlines[current].lineinfo[0]
                #print "Line info\n" + str(classlines[current].lineinfo)
                txt_class = classlines[current].completeline
                current+=1
            elif tag  == 're_wrongclass':
                #this error find "class" word in text but something is wrong. This error here prints the proper line number.
                error_found = True
                txt_class = ''
                print "Expected python/sage class definition on line %d or class identifier is wrong." % (current+1)
                print "Class identifier must follow a name like: E12A34_somename_number."
            else:
                error_found = True
                print "Expected python/sage class definition on line %d or class identifier is wrong." % (current+1)
                print "Class identifier must follow a name like: E12A34_somename_number."

        elif state == ExState.CLASS: #consume class lines
            #Check transition
            if tag  == 're_blanks' or tag  == 're_rest':
                #action
                txt_class += classlines[current].completeline
                current+=1
            else:
                error_found = True
                print "Symbol not expected at line %d." % (current+1)

    if not error_found and state != ExState.CLASS:
        error_found = True
        print "Expected python/sage class definition on line %d or class identifier is wrong." % (current+1)
        print "Class identifier must follow a name like: E12A34_somename_number."

    if error_found:
        return None
    else:
        #old way: return (unique_name,txt_sections,txt_summary,txt_problem,txt_answer,txt_class)
        return  {
            'unique_name': unique_name.strip(), 
            'sections_text': txt_sections.strip(), 
            'suggestive_name': txt_problemname.strip(),
            'summary_text': txt_summary.strip(), 
            'problem_text': txt_problem.strip(), 
            'answer_text': txt_answer.strip(), 
            'class_text': txt_class.strip()
        }




#TODO: change this !

def test1():
    txt = '''

   % summary

   % summary COM TEXTO

% problem    
 
%answer

class E12(Exercise):

class E12X(Exercise):

class E12X34(Exercise):

class E26A36_antiderivativeparts_005(Exercise):

    ola'''

    #print txt

    txtlines = txt.splitlines()

    for line,r in enumerate(flex(txt)):
            print '"' + txtlines[line] +'"'
            print r


def test2():

    txt=r'''

 % summary 

Primitivas (26A36) Antidifferentiation: Primitivas por partes 
Primitiva de (ax)(bx+c)^i 


Palavras chave: Primitiva, antiderivada, partes, pot\^encia


%PROBLEM inicia o enunciado
Determine a fam\'lia de primitivas
\[
\int{ongl\,(onfl)^{ini} \, dx}
\] 

   %   ANSWER
Usando o m\'etodo de primitiva\c c\~ao por partes
\[
\int{f'(x) \, g(x) \, dx}=f(x)\, g(x)- \int{f(x) \, g'(x)\,dx}
\]
considera-se
\[
\begin{array}{lll}
f'(x)=(onfl)^{ini} & \quad & \displaystyle f(x)=onb1l \, \frac{(onfl)^{oni1}}{oni1}=onb2l\,(onfl)^{oni1}\\
& & \\
g(x)=ongl & \quad &\displaystyle  g'(x)=ongdl
\end{array}.
\]
Ent\~ao,
\[
\begin{array}{lll}
\int{ongl\,(onfl)^{ini} \, dx}&=&\displaystyle ongl \, onb2l \, (onfl)^{oni1}-\int{ongdl \, onb2l \,(onfl)^{oni1} \, dx}\\
&  & \\
&=&\displaystyle onb3l \,x (onfl)^{oni1} -onb3l \, \frac{(onfl)^{oni2}}{oni2}+C\\
& & \\
&=&\displaystyle onb3l \,x (onfl)^{oni1} -onb4l \, (onfl)^{oni2}+C, \, C \in \mathbb{R}
\end{array}
\] 


class E26A36_antiderivativeparts_005(Exercise):

    def make_random(self,seed):
        #obrigatorio
        Exercise.make_random(self,seed)
        
        x=var('x')
        y=var('y')
        self.ina=ur.iunif_nonset(2,10,[0,1])
        self.inb=ur.iunif_nonset(2,10,[0])
        self.inc=ur.iunif_nonset(2,10,[0,1,-1])
        self.ini=ur.iunif(5,20)
        
        
    def solve(self):
        #obrigatorio e atencao aos espacos = 4
        Exercise.solve(self)
        self.ona = showmul(self.ina)
        self.onb = showmul(self.inb)
        self.onc = showmul(self.inc)
        #definir a fun\c c\~ao f
        self.onf=self.inb*x+self.inc
        self.onfl=latex(self.onf)
        #definir a primitiva de f
        self.oni1=self.ini+1
        self.oni2=self.ini+2
        self.onb1=1/self.inb
        self.onb1l=latex(self.onb1)
        self.onb2=self.onb1/self.oni1
        self.onb2l=latex( self.onb2)
        #definir a fun\c c\~ao g
        self.ong=self.ina*x
        self.ongl=latex(self.ong)
        self.ongd=derivative(self.ong,x)
        self.ongdl=latex(self.ongd)
        self.onb3=self.onb2*self.ongd
        self.onb3l=latex(self.onb3)
        self.onb4=self.onb3/self.oni2
        self.onb4l=latex(self.onb4)
        
    '''

    txtlines = txt.splitlines()

    for line,r in enumerate(flex(txt)):
            print 'line '+str(line+1)+': "' + txtlines[line] +'"'
            print r

    res = exerc_parse(txt)
    if res is not None:    
        (s,p,a,c) = res
        print s
        print p
        print a
        print c
    else:
        print "See error above."



#if __name__=='__main__':
#
#    test2()



