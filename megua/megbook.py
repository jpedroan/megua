# coding=utf-8

r"""
MegBook -- Repository and functionalities for managing exercises.

MEGUA build your own database of exercises in several markup languages.

This module provides a means to produce a database of exercises 
that can be seen as a book of some author or authors.

Using exercices:

- create, edit and delete exercises from a database.
- search for an exercise or set of exercises.
- create a random instance from a set or single exercise
- create an instance based on specific parameters
- create latex (and PDF) from a single or a set of exercises.

AUTHORS:

- Pedro Cruz (2012-06): initial version (based on megbook.py)
- Pedro Cruz (2016-01): first modifications for use in SMC.


TESTS:

::

    sage -t megbook.py


Create or edit a database:

::
   sage: from megua.megbook import MegBook
   sage: from megua.exbase import ExerciseBase
   sage: meg = MegBook(r'_output/megbasedb.sqlite')


Save a new or changed exercise:

::

   sage: meg.save(r'''
   ....: %Summary Primitives
   ....: Here one can write few words, keywords about the exercise.
   ....: For example, the subject, MSC code, and so on.
   ....:   
   ....: %Problem
   ....: What is the primitive of ap x + bp@() ?
   ....: 
   ....: %Answer
   ....: prim1
   ....: 
   ....: class E28E28_pdirect_001(ExerciseBase):
   ....: 
   ....:     def make_random(self,edict=None):
   ....:         self.ap = ZZ.random_element(-4,4)
   ....:         self.bp = self.ap + QQ.random_element(1,4)
   ....:         x=SR.var('x')
   ....:         self.prim1 = integrate(self.ap * x + self.bp,x)
   ....: ''')
   Each problem can have a suggestive name. 
   Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.
   <BLANKLINE>
   -------------------------------
   Instance of: E28E28_pdirect_001
   -------------------------------
   ==> Summary:
   Here one can write few words, keywords about the exercise.
   For example, the subject, MSC code, and so on.
   ==> Problem instance
   What is the primitive of -1 x + (-5/4) ?
   ==> Answer instance
   prim1
   sage: meg
    MegBook('_output/megbasedb.sqlite')

   Long computation? Two examples follow:
   
   sage: meg.save(r'''
   ....: %Summary Long Computations Section; Example 1
   ....: Testing the production of exercises with long computations.
   ....:   
   ....: %Problem Long Computation Problem
   ....: What is the long primitive of ap x + bp@() ?
   ....:  
   ....: %Answer
   ....:  
   ....: prim1
   ....:  
   ....: class E28E28_pdirect_001(ExerciseBase):
   ....: 
   ....:     def make_random(self,edict=None):
   ....:         #suppose a 15 seconds computation here
   ....:         #maximum by default is 10 (see MegBook)
   ....:         #sleep(15)  #remove # for tests
   ....:         #do something else.
   ....: ''')
   Exercise is taking too long to make!
   Check make_random() routine or increase meg.max_computation_time.
   Exercise was not saved.


::

   sage: meg.max_computation_time = 30  #increase patience.
   sage: meg.save(r'''
   ....: %Summary Long Computations Section; Example 2
   ....: Changing maximum length of computation time.
   ....:    
   ....: %Problem Long Computation Problem
   ....: What is the long primitive of ap x + bp@() ?
   ....:  
   ....: %Answer
   ....:  
   ....: prim1
   ....:  
   ....: class E28E28_pdirect_001(ExerciseBase):
   ....:  
   ....:     def make_random(self,edict=None):
   ....:         #suppose a 15 seconds computation here
   ....:         #maximum by default is 10 (see MegBook)
   ....:         #sleep(5)  #remove # for tests
   ....:         #do something else.
   ....:            
   ....: ''') 
   -------------------------------
   Instance of: E28E28_pdirect_001
   -------------------------------
   ==> Summary:
   Changing maximum length of computation time.
   ==> Problem instance
   What is the long primitive of ap x + bp ?
   ==> Answer instance
   prim1


Make a catalog:

::

   sage: meg.catalog()
   
   
Search an exercise:

::

  sage: meg.search("primitive")
  Exercise name E28E28_pdirect_001
  What is the long primitive of ap x + bp@() ?
  <BLANKLINE>

Remove an exercise:

::

   sage: meg.remove('E28E28_pdirect_001',dest=r'_output')
   Exercise 'E28E28_pdirect_001' stored on text file _output/E28E28_pdirect_001.txt.
   sage: meg.remove('E28E28_nonexistant',dest=r'_output')
   Exercise E28E28_nonexistant is not on the database.


DEVELOP:

Execution time control

- authors don't want to wait to much time for an "answer"
- the programming part (python/sage,...)  running must be time controlled
- the markup language (latex, html, ...) instance must be time controlled

Example: The laTeX compilation could took to much time and a warning must be issued.


Meaning of _ and __ (double underscorre):

TODO: read http://stackoverflow.com/questions/1301346/the-meaning-of-a-single-and-a-double-underscore-before-an-object-name-in-python



"""


# Abstract function
# raise NotImplementedError( "Should have implemented this" )


#*****************************************************************************
#       Copyright (C) 2012,2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************



#PYTHON modules:
import tempfile
import sqlite3 #for row objects as result from localstore.py
import shutil
import os
from os import environ
import subprocess
import random
#import codecs
import re
import codecs
import random as randomlib #random is imported as a funtion somewhere



#SAGE modules
from sage.all import * #needed in exec (see exerciseinstance)
#from sage.repl.preparse import preparse_file,preparse
#sage_eval does not work with class definitions?
#from sage.misc.sage_eval import sage_eval


  
#MEGUA configuration file: server side settings.
#tirar? from megua.mconfig import *



#MEGUA modules:
from megua.mathcommon import *
from megua.exbase import ExerciseBase
from megua.exlatex import ExLatex
from megua.exsiacua import ExSiacua
from megua.localstore import LocalStore,ExIter
from megua.parse_ex import parse_ex
from megua.tounicode import to_unicode
from megua.jinjatemplates import templates
from megua.ur import ur
from megua.megsiacua import MegSiacua
from megua.csection import SectionClassifier
#from platex import pcompile
#from xmoodle import MoodleExporter
#from xsphinx import SphinxExporter
#from xlatex import * #including PDFLaTeXExporter






class MegBook(MegSiacua):
    r"""
    A book of exercises of several markup languages.
    
    """

    #TODO 1: increase docstring examples.

    #TODO 2: assure that there is a natlang folder in templates (otherwise put it in english). Warn for existing languages if specifies lan does not exist.


    def __init__(self,filename=None,natlang='pt_pt',markuplang='latex'): 
        r"""

        INPUT::
        - ``filename`` -- filename where the sqlite database is stored.

        """

        if not filename:
            #TODO: this must be in the LocalStore code.
            raise IOError("MegBook needs database filename.")

    
        #Create or open the database
        try:
            self.megbook_store = LocalStore(filename=filename,natlang=natlang,markuplang=markuplang)
            self.local_store_filename = self.megbook_store.local_store_filename #keep record.
            #print "Opened " + str(self)
        except sqlite3.Error as e:
            print "Filename couldn't be opened: " , e.args[0], "\n"
            raise e


        #For template. See template_create function.
        self.template_row = None

        #In seconds, author can change this value when calling save()
        self.max_computation_time = 10 
        #In seconds, author can change this value when calling save()
        self.max_tried_instances = 10 

        ExerciseBase._megbook = self
        #print self.__repr__()

    def __str__(self):
        return "MegBook('%s')" % self.local_store_filename

    def __repr__(self):
        return "MegBook('%s')" % self.local_store_filename

    def make_index(self,where='.',debug=False):
        #warnings.warn("make_index() is deprecated. TODO: what to do ?", DeprecationWarning)
        raise NotImplementedError

    def save(self,uexercise):
        r"""
        Save an exercise defined on a `python string`_ using a specific sintax defined here_.

        INPUT::

        - ``uexercise`` -- an exercise textual description (utf8 string).
        
        OUTPUT::
        
        - Textual messages with errors.

        DESCRIPTION:
        
        - An exercise textual description must be processed.

        """
        
#TODO: improve this try because it's hidding programmer coding errors and not only  author coding errors.
#        try:
            #First check: syntatic level ("megua" script)
        row =  parse_ex(to_unicode(uexercise))
        if not row:
            raise
            
            
        #Second check: syntatic and runtime  ("python/sagemath" script)
        ex_instance = self.exerciseinstance(row,ekey=0)            
        #Third check: create contens (latex compilation, for example)
        ex_instance.print_instance()

#       except:
#           print "Exercise was not saved."
        
        
        #After all that, save it on database:                        
        self.megbook_store.insertchange(row)
        


            

#TODO: improve or adpat this check_all method
#    def check_all(self,dest='.'):
#        r""" 
#        Check all exercises of this megbook for errrors.
#
#        INPUT:
#
#        OUTPUT:
#
#            Printed message and True/False value.
#        """
#
#        all_ex = []
#        for row in ExIter(self.megbook_store):
#            if not self.is_exercise_ok(row,dest,silent=True):
#                print "   Exercise '%s' have python/sage or compilation errors." % row['unique_name']
#                all_ex.append(row['unique_name'])
#        if all_ex:
#            print "Review the following exercises:"
#            for r in all_ex:
#                print r
#        else:
#            print "No problem found."



    def select(self,regex=None, addkeys=False):
        r"""
        Performs a search of a regular expression over all fields.
        Regular expressions examples: 
        * "prim" for all words containing prim
        * TO DO: IMPROVE

        TO DO:  time out operation, this!
        Examples:

            meg.select("primitive*")

        INPUT:
        - ``regex`` -- regular expression (see `Regular Expression`_ module). None will get all.
        - ``addkeys`` -- if True then randomly chooses a key for the exercise.

        OUTPUT:
        - List of strings (each string is the name of the exercise).
        - If ``addkeys`` then returns a list ``["exerc1", 10, "exerc2", 20, ...]``
        
        .. _Regular Expression: http://docs.python.org/release/2.6.7/library/re.html
        """
        if regex is None:
            regex=""
        exlist = [row[1] for row in self.megbook_store.search(regex)] #row[0] is unique_name
        #print exlist
        if addkeys:
            pairs = [ (e,random.randint(0,1000)) for e in exlist]
            flat = [ v for p in pairs for v in p] #flatten
        else:
            flat = exlist
        return flat


    def search(self,regex):
        r"""
        Performs a search of a regular expression over all fields.

        Examples:

            meg.search("primitive*")

        INPUT:
        - ``regex`` -- regular expression (see `Regular Expression`_ module).

        OUTPUT:
        - print of a sample of each exercise
        
        .. _Regular Expression: http://docs.python.org/release/2.6.7/library/re.html
        """

        exlist = self.megbook_store.search(regex)
        for row in exlist:
            self.search_print_row(row)


    def search_print_row(self,exrow):
        r"""
        This is an helper function of ``Meg.search`` function to print the contents of a search.
        Not to be called by meg user.

        INPUT:

        - ``exrow`` -- an sqlite row structure_ where fields are accessible by name.

        OUTPUT:

        - html or text.

        NOTES:
            unicode is in utf-8 -> string
            http://en.wikipedia.org/wiki/ISO/IEC_8859-1
            Sage html() requires string.
        """
        #Modify this
        sname = 'Exercise name %s' % exrow['unique_name'].encode('utf8')
        print sname + '\n' + exrow['problem_text'].encode('utf8') + '\n'
        #TODO
        #if is_notebook():
        #    html('<b>' + sname + ': </b><pre>' + exrow['problem_text'].encode('utf8') + '</pre><br/>')
        #else:
        #    print sname + '\n' + exrow['problem_text'].encode('utf8') + '\n'



    def remove(self,unique_namestring,dest='.'):
        r"""
        Removing an exercise from the database.

        INPUT:

        - ``unique_namestring`` -- the class name.
        """

        #Get the exercise
        row = self.megbook_store.get_classrow(unique_namestring)
        if row:            
            fname = os.path.join(dest,unique_namestring+'.txt')
            #store it on a text file
            f = open(fname,'w')
            f.write(row['summary_text'].encode('utf-8')) #includes %summary line
            f.write(row['problem_text'].encode('utf-8')) #includes %problem line
            f.write(row['answer_text'].encode('utf-8')) #includes %answer line
            f.write(row['class_text'].encode('utf-8'))
            f.close()
            print "Exercise '%s' stored on text file %s." % (unique_namestring,fname)

            #remove it
            self.megbook_store.remove_exercise(unique_namestring)
        else:
            print "Exercise %s is not on the database." % unique_namestring



    def new(self, unique_name, ekey=None, edict=None, returninstance=False):
        r"""Prints an exercise instance of a given type

        INPUT:

         - ``unique_name`` -- the class name.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.
         - ``returninstance`` -- if True, this function return a python object.

        OUTPUT:
            An instance of class named ``unique_name``.

        """
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(unique_name)
        if not row:
            print "%s cannot be accessed on database" % unique_name
            return
        
        #Create and print the instance
        ex_instance = self.exerciseinstance(row, ekey, edict)
        
        if returninstance:
            return ex_instance
        else:
            ex_instance.print_instance()
            return

    


    def exerciseclass(self, row):
        r"""
        Interpret the `exercise class` (not an object) from text fields:

        - Put the class designed by an author in the global namespace 
        - (not yet the instance)
        
        DEVELOPMENT:

        Check:
        
        - global namespace has the class name.
        
        Instructions that did not work but don't know why::

            #sage_class_string = preparse_file(row['class_text'],globals=globals())
            #sage_class_string = u"# -*- coding: utf-8 -*\nfrom sage.all import *\nfrom megua.all import *\n" + sage_class_string
            #sage_class_string = u"from sage.all import *\nfrom megua.all import *\n" + sage_class_string
            #exec(...), only exec statment works.

            #exec compile(sage_class,row["unique_name"],'eval')
            #sage_eval did not work. Why ?
            #http://www.sagemath.org/doc/reference/misc/sage/misc/sage_eval.html
            #and spread this for more points in code.

        """
    
        # TODO: control the time and the process. Is it of value?

        sage_class_string = preparse(row['class_text'])
        sage_class_string = u"from megua.all import *\n" + sage_class_string
        exec sage_class_string

         # TODO NOW: ACABAR ISTO
#        except: 
#            tmp = "_temp" #tempfile.mkdtemp()
#            pfilename = tmp+"/"+row["unique_name"]+".sage"
#            pcode = open(pfilename,"w")
#            pcode.write("# -*- coding: utf-8 -*\nfrom megua.all import *\n" + row['class_text'].encode("utf-8") )
#            pcode.close()
#            errfilename = "%s/err.log" % tmp
#            os.system("sage %s 2> %s" % (pfilename,errfilename) ) # sage -python ???
#            errfile = open(errfilename,"r")
#            err_log = errfile.read()
#            errfile.close()
#            #TODO: adjust error line number by -2 lines HERE.
#            #....
#            #remove temp directory
#            #print "=====> tmp = ",tmp
#            #os.system("rm -r %s" % tmp)
#            print "Error log:", err_log #user will see errors on syntax.
#            raise SyntaxError  #to warn user #TODO: not always SyntaxError
    
        #Get class name
        #The string contents row['unique_name'] is now a valid identifier.
        ex_class = eval(row['unique_name']) 

    
        #class fields
        ex_class._summary_text = row['summary_text']
        ex_class._problem_text = row['problem_text']
        ex_class._answer_text  = row['answer_text'] 
        ex_class._unique_name  = row['unique_name']
        ex_class._suggestive_name = row['suggestive_name']
    
        return ex_class
    
        
    
    def exerciseinstance(self, row, ekey=None, edict=None):
        r"""
        Instantiates the `exercise class` (not an object) from text fields.
        Then, creates an instance using  `exercise_instance` routine.
    
        This function creates an instance of a class named in parameter unique_namestring. That class must be already defined in memory.
    
        INPUT:
    
         - ``row``-- the sqlite row containing fields: 'summary_text', 'problem_text',  'answer_text'.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.
    
        OUTPUT:
            An instance of class named ``unique_namestring``.
    
        DEVELOP:
    
        - http://docs.python.org/library/exceptions.html#exceptions.Exception
        - TODO: control the time and the process

        """

        #Create the class (not yet the instance). 
        #See exerciseclass definition above.
        ex_class = self.exerciseclass(row)    


        #TODO: remove this and active "try" below
        #TODO: use "load" (check sandbox/python_modules)
        ex_instance = ex_class(ekey,edict)
    
#        try:
#            ex_instance = ex_class(ekey,edict)
#        except: 
#            tmp = "_temp" # tempfile.mkdtemp()
#            pfilename = tmp+"/"+row["unique_name"]+".sage"
#            pcode = open(pfilename,"w")
#            pcode.write("# coding=utf-8\nfrom megua.all import *\n" + row['class_text'].encode("utf-8")+"\n")
#            pcode.write(row['unique_name'] + "(ekey=" + str(ekey) + ", edict=" + str(edict) + ")\n")
#            pcode.close()
#            errfilename = "%s/err.log" % tmp
#            os.system("sage %s 2> %s" % (pfilename,errfilename) )
#            errfile = open(errfilename,"r")
#            err_log = errfile.read()
#            errfile.close()
#            #TODO: adjust error line number by -2 lines HERE.
#            #....
#            #remove temp directory
#            #print "=====> tmp = ",tmp
#            ######os.system("rm -r %s" % tmp)
#            print err_log
#            return None #raise #Need to specify "raise Exception"?  
        
        return ex_instance
    
    

#TODO: remove get method ?    
#    def get(self,unique_name,ekey=None,edict=None):
#        r"""
#
#        INPUT:
#
#        - ``unique_name``: problem name (name in "class E12X34_something_001(Exercise):").
#        - ``ekey``: numbers that generate the same problem instance.
#        - ``edict``: dictionary of values
#
#        OUTPUT:
#
#        - this command writes an html file with all instances.
#
#        NOTE:
#
#        - you can export between 3 and 6 wrong options and 1 right.
#
#            
#        Algorithm:
#            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.
#
#        """    
#        
#        #Create exercise instance
#        row = self.megbook_store.get_classrow(unique_name)
#        if not row:
#            print "Exercise %s not found." % unique_name
#            return
#
#        if ekey or edict:
#            return self.exerciseinstance(row,ekey,edict)
#        else:
#            return self.exerciseclass(row) 





    def thesis(self,problem_list):
        r"""
        Generates a tex file ready in standard LaTeX to put in a thesis.

        INPUT:
        
        - `problem_list`: see below.

        Structure example:
            Simple: no division in groups ("sections") in the final examination sheet.
            [ 
                "E12X34_Calc_001", 10,  #specific problem key
                "E12X34_Calc_001", 20,  #specific problem key (repeat the template)
                "E12X34_Deriv_001"      #select a random key for this problem
            ]

        """

        #Build paired list (ex,ekey) adding a random ekey when
        #no key is given.
        i = 0
        n = len(problem_list)

        for j in range(n):
            #if problem_list[i] is unicode convert to str 
            #for the next ifs
            if type(problem_list[j])==unicode:
                problem_list[j] = str(problem_list[j])

        paired_list = []
        #print random.__module__
        rn = randomlib.randint(0,10**5) #if user did not supplied an ekey.
        while i < (n-1):

            if type(problem_list[i])==str and type(problem_list[i+1])==str: #two problems
                paired_list.append( (problem_list[i], rn) ) 
                i += 1 #advance to position i+1
            elif type(problem_list[i])==str and type(problem_list[i+1])!=str: #!= probably a number
                paired_list.append( (problem_list[i], problem_list[i+1]) )
                i += 2 #advance to position i+2, consuming the ekey
        if i < n: #add last problem 
            paired_list.append( (problem_list[i], rn) )



        #amc template without groups for each question
        allproblems_text = ''
        for (problem_name,ekey) in paired_list:

            print "Generating sample of",problem_name

            #print "Write",(problem_name,ekey),"in thesis."

            #generate problem and answer text (choices are in the answer part)

            #Get summary, problem and answer and class_text
            row = self.megbook_store.get_classrow(problem_name)
            if not row:
                print "meg.thesis(): %s cannot be accessed on database" % problem_name
                continue
            #Create and print the instance
            ex_instance = exerciseinstance(row, int(ekey) )

            summary =  ex_instance.summary() 
            problem = ex_instance.problem()
            answer = ex_instance.answer()
            problem_name =  ex_instance.name
    
            #Adapt for appropriate URL for images
            if ex_instance.image_list != []:
                problem = self._adjust_images_url(problem)
                answer = self._adjust_images_url(answer)
                #see siacua functions: self.send_images()



            #TODO: this lines are a copy of code in "siacua()".
            if ex_instance.has_multiplechoicetag:
                if ex_instance.image_list != []:
                    answer_list = [self._adjust_images_url(choicetxt) for choicetxt in ex_instance.collect_options_and_answer()]
                else:
                    answer_list = ex_instance.collect_options_and_answer()
            else:
                answer_list = ex_instance.answer_extract_options()


            #TODO: os CDATA tem que ser recuperados neste ficheiro e os <choice> ja estao no campo ex.all_choices.

            #generate amc problemtext

            problem_string = self.template("thesis_problem.tex",
                    problem_name=problem_name,
                    slashedproblem_name=latexunderscore(problem_name),
                    problem_text=html2latex(problem),
                    correcttext=equation2display( html2latex(answer_list[0]) ),
                    wrongtext1=equation2display( html2latex(answer_list[1]) ),
                    wrongtext2=equation2display( html2latex(answer_list[2]) ),
                    wrongtext3=equation2display( html2latex(answer_list[3]) ),
                    summtxt=latexcommentthis(summary),
                    detailedanswer=html2latex(answer_list[4]) 
                      #expected at position 4 the full answer.
            )

            #Convert the link below to \includegraphics{images/E12A34_cilindricas_0001-fig4-10.png}
            #<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/E12A34_cilindricas_0001-fig4-10.png'></img>
            problem_string = re.subn(
                """<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/(.*?)'></img>""",
                r'\n\\begin{center}\n\includegraphics[width=8cm]{images/\1}\n\end{center}\n', 
                problem_string, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]

            #add this to allproblems_text
            allproblems_text += problem_string


        os.system("zip -r images images > /dev/null 2>&1")


        #Apply to all "allproblems_text"
        
        r"""2. Convert
                \questao{ 
    
                 $\displaystyle 7.95$ 
                 }
            to 
                \questao{$\displaystyle 7.95$}
            but it does not work right with
                \questao{ 
 
                    \begin{center}
                    \includegraphics[width=8cm]{images/E97k40_grafico_tabela_001-fig1-9.png}
                    \end{center}
 
                 }
        """

        pos = 0
        new_allproblems_text = ''  #below pattern is not perfect because last } could match \begin{center} <-- this }
        for m in re.finditer(r'\\questao\{(.*?)\}', allproblems_text, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE):
            inside = m.group(1)
            inside,nc = re.subn("\n","",inside,re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
            new_allproblems_text += allproblems_text[pos:m.start(1)] + inside  
            pos = m.end(1)

        new_allproblems_text += allproblems_text[pos:]

        #Produce "Source Code" from each problem.
        PDFLaTeXExporter(self,where='.',exerset=paired_list,debug=False)
        f = codecs.open( "megua_ex.tex", encoding='latin1', mode='r') 
        #f = open("megua_ex.tex","r")
        source_code = f.read()
        #print "type=",type(source_code)
        f.close()

        #Make a latex file to be compiled using amc program (or pdflatex).
        latextext_string = self.template("thesis_latexfile.tex",
            ungroupedquestions=new_allproblems_text,
            sourcecode=source_code
        )


        f = open('thesis_problems.tex','w')
        f.write(latextext_string.encode('latin1')) #utf8 #latin1  <-- another option
        f.close()

        #os.system("pdflatex -interact=nonstopmode {0} > /dev/null 2>&1".format("thesis_problems.tex"))
        #os.system("rm thesis_problems.log thesis_problems.aux > /dev/null 2>&1") 
        #os.system("rm -r images > /dev/null 2>&1")


        print '\nInstrucoes:\n1. Use o botao direito e "Save link as..." para guardar "thesis_problems.tex" no seu computador.'
        print '2. Se houver imagens, o conteudo do ficheiro "images.zip" deve ser colocado numa pasta "images".'
        print '3. Sera necessaria paciencia para finalizar a pre conversao de HTML para LaTeX em cada exercicio.'
        print '4. Recomenda-se adaptar um exercicio de cada vez compilado um por um.'
    





    def catalog(self,what='all',export='latex'):
        r"""Writes exercises in an ordered fashion 
        Only: all and latex formats, now.
        """

        self.sc = SectionClassifier(self.megbook_store)
        section_iterator = self.sc.section_iterator()

        #ver templates: megbook_catalog_latex
        lts = u'' #exerciseinstanceslatex

        #Instance creation
        print "MegBook.py say: making instances of the exercises."
        for s in section_iterator:

            #Section creation
            if s.level==0: # {{ => }
                lts += u'\n\n\section{{{0} ({1})}}\n\n'.format(s.sec_name,len(s.exercises))
            elif s.level==1:
                lts += u'\n\n\subsection{{{0} ({1})}}\n\n'.format(s.sec_name,len(s.exercises))
            elif s.level==2:
                lts += u'\n\n\subsubsection{{{0} ({1})}}\n\n'.format(s.sec_name,len(s.exercises))
            else:
                lts += u'\n\n\textbf{{{0} ({1})}}\n\n'.format(s.sec_name,len(s.exercises))

            #Get the instances, if they exist on this section, subsection or subsubsection
            #TODO: image render mode to "filenameimage"
            lts += u'\n\nThis section has {0} exercises.\n\n'.format(len(s.exercises)) # {{ => }
            for unique_name in s.exercises:
                ex = self.new(unique_name,ekey=0,returninstance=True)
                if ExLatex in ex.__class__.__bases__:
                    #TODO: incluir tipo no template e na section acima
                    ex_str = templates.render("megbook_catalog_instance.tex",
                                exformat="latex",
                                unique_name_noslash = unique_name.replace("_","\_"),
                                summary = ex.summary(),
                                suggestive_name = ex.suggestive_name(),
                                problem = ex.problem(),
                                answer = ex.answer()
                    )
                elif ExSiacua in ex.__class__.__bases__:
                    #TODO: incluir tipo no template e na section acima
                    ex_str = templates.render("megbook_catalog_instance.tex",
                                exformat="siacua",
                                unique_name_noslash = unique_name.replace("_","\_"),
                                summary = ex.summary(),
                                suggestive_name = ex.suggestive_name(),
                                problem = ExSiacua.to_latex(ex.problem()), #u'\\begin{verbatim}\n'+ex.problem()+'\n\\end{verbatim}\n',
                                answer = ExSiacua.to_latex(ex.answer()) #u'\\begin{verbatim}\n'+ex.answer()+'\n\\end{verbatim}\n'
                    )
                else:
                    #TODO: incluir tipo no template e na section acima
                    ex_str = templates.render("megbook_catalog_instance.tex",
                                exformat="textual (exbase)",
                                unique_name_noslash = unique_name.replace("_","\_"),
                                summary = ex.summary(),
                                suggestive_name = ex.suggestive_name(),
                                problem = u'\\begin{verbatim}\n'+ex.problem()+'\n\\end{verbatim}\n',
                                answer = u'\\begin{verbatim}\n'+ex.answer()+'\n\\end{verbatim}\n'
                    )

                lts += ex_str

                #Only for latex (was first version)
                #lts += u'\\bigskip\n\\textbf{{Unique Name {0}}} with ekey=0\n'.format(unique_name.replace("_","\_"))
                #lts += u'%{0}\n\n'.format(unique_name)
                #lts += u'\\textbf{{Summary}}\n\n\\begin{{verbatim}}\n{0}\n\\end{{verbatim}}\n\n'.format(ex.summary())
                #lts += u'\\textbf{{Problem {0}}}\n\n{1}\n\n'.format(
                #    ex.suggestive_name(),
                #    ex.problem())
                #lts += u'\\textbf{{Answer}}\n\n{0}\n\n'.format(ex.answer())




        print "MegBook.py say: compiling latex file containing the instances of the exercises."

        latex_string =  templates.render("megbook_catalog_latex.tex",
                         exerciseinstanceslatex=lts)


        MEGUA_EXERCISE_CATALOG = environ["MEGUA_EXERCISE_CATALOG"]
        CATALOG_TEX_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOG,"catalog.tex")
        CATALOG_PDF_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOG,"catalog.pdf")

        f = codecs.open(CATALOG_TEX_PATHNAME, mode='w', encoding='utf-8')
        f.write(latex_string)
        f.close()

        #TODO: convert all os.system to subprocess.call or subprocess.Popen
        os.system("cd '%s'; pdflatex -interaction=nonstopmode %s 1> /dev/null" % (MEGUA_EXERCISE_CATALOG,"catalog.tex") )
        os.system("cd '%s'; pdflatex -interaction=nonstopmode %s 1> /dev/null" % (MEGUA_EXERCISE_CATALOG,"catalog.tex") )


        if environ["MEGUA_PLATFORM"]=='SMC':
            if environ["MEGUA_BASH_CALL"]=='on': #see megua bash script at megua/megua
                print "MegBook module say:  open ", CATALOG_PDF_PATHNAME
                #Does not work in SMC: subprocess.Popen(["/bin/open",CATALOG_PDF_PATHNAME])
                #Does not work using "sage -python": from smc_pyutil import smc_open
                #Works using: "python": from smc_pyutil import smc_open
                #                        smc_open.process([CATALOG_PDF_PATHNAME])
                #WORKS:subprocess.call(["openpdf.py",CATALOG_PDF_PATHNAME])
                #ANOTHER SOLUTION (http://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath)
                sys.path.append('/usr/local/lib/python2.7/dist-packages')
                from smc_pyutil import smc_open
                smc_open.process([CATALOG_PDF_PATHNAME])
            else: #sagews SALVUS
                from smc_sagews.sage_salvus import salvus
                salvus.file(CATALOG_PDF_PATHNAME,show=True,raw=True); print "\n"
                salvus.file(CATALOG_TEX_PATHNAME,show=True,raw=True); print "\n"
                salvus.open_tab(CATALOG_PDF_PATHNAME)
        elif environ["MEGUA_PLATFORM"]=='DESKTOP':
            print "MegBook module say: evince ",CATALOG_PDF_PATHNAME
            subprocess.Popen(["evince",CATALOG_PDF_PATHNAME])
        else:
            print """MegBook module say: environ["MEGUA_EXERCISE_CATALOG"] must be properly configured at $HOME/.megua/mconfig.sh"""





def m_get_sections(sectionstxt):
    r"""

    LINKS::

       http://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python?rq=1
    """
    s = "megua/"+sectionstxt.replace("; ","/") #case "; " by "/"
    return s.replace(";","/") #possible case without space: ";" by "/"




#end class MegBook


