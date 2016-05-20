# coding: utf-8

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
   Check exercise E28E28_pdirect_001 for the above warnings.
   -------------------------------
   Instance of: E28E28_pdirect_001
   -------------------------------
   ==> Summary:
   Here one can write few words, keywords about the exercise.
   For example, the subject, MSC code, and so on.
   ==> Problem instance
   What is the primitive of -1 x + (-\frac{5}{4}) ?
   ==> Answer instance
   prim1





Testing a warning error:

::

   sage: meg.save(r'''
   ....: %Summary Primitives
   ....: Here one can write few words, keywords about the exercise.
   ....: For example, the subject, MSC code, and so on.
   ....:   
   ....: %Problem A Primitive
   ....: What is the primitive of ap x + bp@() ?
   ....: 
   ....: %Answer
   ....: prim1
   ....: 
   ....: class E28E28_pdirect_001(ExerciseBase):
   ....: 
   ....:     def make_random(self,edict=None):
   ....:         x = SR.var("x")
   ....:         yy = (exp(x)*exp(5*x)).simplify_exp() #deprecated
   ....:         self.ap = ZZ.random_element(-4,4) + yy
   ....:         self.bp = self.ap + QQ.random_element(1,4)
   ....:         x=SR.var('x')
   ....:         self.prim1 = integrate(self.ap * x + self.bp,x)
   ....: ''')
    MegBook.py say: exercise "E28E28_pdirect_001" needs review! See below:
    simplify_exp is deprecated. Please use canonicalize_radical instead.
    See http://trac.sagemath.org/11912 for details.
            x = SR.var("x")
            yy = (exp(x)*exp(5*x)).simplify_exp() #deprecated
            self.ap = ZZ.random_element(-4,4) + yy
            self.bp = self.ap + QQ.random_element(1,4)
    ======= end of warning list ==========
    -------------------------------
    Instance of: E28E28_pdirect_001
    -------------------------------
    ==> Summary:
    Here one can write few words, keywords about the exercise.
    For example, the subject, MSC code, and so on.
    ==> Problem instance
    What is the primitive of e^{\left(6 \, x\right)} - 1 x + e^{\left(6 \, x\right)} - \frac{5}{4} ?
    ==> Answer instance
    prim1



Long computation? Two examples follow:

::
   
   sage: try:    
   ....:     meg.save(r'''
   ....: %Summary Long Computations Section; Example 1
   ....: Testing the production of exercises with long computations.
   ....:   
   ....: %Problem Long Computation Problem
   ....: What is the os.path.join(
            environ["MEGUA_EXERCISE_INPUT"],
            filename)long primitive of ap x + bp@() ?
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
   ....:         sleep(15)  #remove comment for tests
   ....:         pass
   ....: ''')
   ....: except KeyboardInterrupt:
   ....:     pass
   Exercise "E28E28_pdirect_001" is taking too long to make!
   Check make_random() routine or increase meg.max_computation_time.

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
   ....:         pass   
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

   sage: meg.catalog() #opens evince
   
   
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


Call siacua system (this module inherits from megsiacua.py):

::

   #TODO
   ssssage: meg.siacua(exname="E97K50_Laplace_001_siacua",ekeys=[1,2,5],sendpost=False,course="calculo2",usernamesiacua="jeremias")

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
#import tempfile
#import shutil
import sqlite3 #for row objects as result from localstore.py
import os
from os import environ
import subprocess
import random
import keyword
import re
import codecs
import random as randomlib #random is imported as a funtion somewhere
import warnings
import httplib, urllib


#For sagews files:
import json
from uuid import uuid4
def uuid():
    return unicode(uuid4())
MARKERS = {'cell':u"\uFE20", 'output':u"\uFE21"}
#end.

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
from megua.localstore import LocalStore
from megua.parse_ex import parse_ex
from megua.tounicode import to_unicode
from megua.jinjatemplates import templates
from megua.megsiacua import MegSiacua
from megua.csection import SectionClassifier
from megua.platex import pcompile, latexunderscore
#from xmoodle import MoodleExporter
#from xsphinx import SphinxExporter
#from xlatex import * #including PDFLaTeXExporter




class MegBook(MegSiacua):
    r"""
    A book of exercises of several markup languages.
    
    Implements:
    
    - MegSiacua: functions only for Siacua
    - MegLatex: (not yet) functions only for Latex
    
    """

    #TODO 1: increase docstring examples.

    #TODO 2: assure that there is a natlang folder in templates (otherwise put it in english). Warn for existing languages if specifies lan does not exist.


    def __init__(self,filename=None,natlang='pt_pt',markuplang='latex'): 
        r"""

        INPUT:
        
        - ``filename`` -- filename where the sqlite database is stored.

        """

        if not filename:
            filename = os.path.join(environ["MEGUA_EXERCISE_INPUT"],environ["PROJECT_DATABASE"])
    
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

        #Somes commands need an exercise.
        #see: set_current_exercise()
        self._current_unique_name = None

        ExerciseBase._megbook = self
        #print self.__repr__()

    def __str__(self):
        return "MegBook('%s')" % self.local_store_filename

    def __repr__(self):
        return "MegBook('%s')" % self.local_store_filename

    def set_current_exercise(self,pathname):
        """Receives a pathname. This pathname points to a file that
        contains an exercise. This routine extracts the filename and extension
        and produce the unique_name.
        
        INPUT:
        
        - ``pathname`` --  pathname to the exercise 
        
        Typical, this command must be called using
            meg.set_current_exercise(_file__)
        so argument pathname points to the file in execution.
        
        
        DEVELOPMENT NOTES:
        
            >>> os.path.splitext("ola.lko")
            ('ola', '.lko')
            >>> os.path.splitext(".lko")
            ('.lko', '')

        Parse file contents:
        
        1. find "class" line
        2. if "class" line contains the same name unique_name (see below) do nothing
        3. if "class" line contains a different name other than unique_name:
            - try to remove old unique_name from database
            - change text to the new name
            - produce a warning.

        TODO:
            When file does not exist, capture the "IOError" and produce a message.
            
        """
        
        (edir,filename) = os.path.split(pathname)
        (unique_name,ext) = os.path.splitext(filename)
        
        if ext == '.py':
            (unique_name,ext) = os.path.splitext(unique_name)
            assert(ext=='.sage')
            pathname = os.path.join(edir,unique_name+'.sage')
            #print "megbook.py: Corrected",pathname
        
        
        assert(ext) #See DEVEL notes above: ext<>''
        self._current_unique_name = None

        if not isidentifier(unique_name):
            print "Megbook.py: Filename is not a valid Python identifier."
            usage_new()
            raise SyntaxError
        


        #get file contents 
        unique_name_changed = False
        with codecs.open(pathname, mode='r', encoding='utf-8') as f:
            source_code = f.read()
            #Parse file contents. See above.
            PATTERN_STRING = ur'^class +([_A-Za-z][_a-zA-Z0-9]*)\((\w+)\):\s*'
            re_class_match = re.search(PATTERN_STRING,source_code,re.U|re.M)
            if re_class_match:
                old_unique_name = re_class_match.group(1)
                unique_name_changed = old_unique_name != unique_name
                    
        if unique_name_changed:
            #Try to rename, first in the database:
            # the new unique_name could already exist
            self.megbook_store.rename(old_unique_name,unique_name,warn=False)
            #Change source code
            new_source_code = re.sub(old_unique_name,unique_name,source_code,re.U|re.M)
            with codecs.open(pathname, mode='w', encoding='utf-8') as f:
                f.write(new_source_code)
            print "========================"
            print "Please, "
            print "1. Execute the above comand again using shift-enter ('meg.set_current_exercise(__file__)')."
            print ""
            print "Explanation:"
            print "1. The filename containing the exercise was renamed."
            print "2. The new name of the exercise is now: {}".format(unique_name)
            print "3. Confirm the new <name_of_exercise> in the line 'class <name>(...)'."
            print ""
            print "========================"
            raise IOError
                
        #To be used in all megbook commands
        self._current_unique_name = unique_name
        
        if environ["MEGUA_PLATFORM"]=='SMC':
            if environ["MEGUA_BASH_CALL"]=='on': #see megua bash script at megua/megua
                print "Opening exercise ", unique_name
            else: #sagews SALVUS
                from smc_sagews.sage_salvus import salvus
                salvus.html("<h4>{}</h4>".format(unique_name))
        elif environ["MEGUA_PLATFORM"]=='DESKTOP':
            print "Exercise {}".format(unique_name)
        else:
            print """MegBook module say: environ["MEGUA_PLATFORM"] must be properly configured at $HOME/.megua/mconfig.sh"""



    def new_exercise(self,filename):
        r"""
        Create a new file.
        
        INPUT:
        - `filename`: a name in form E12X34_SomeName_001_latex ou _siacua or _moodle and related extension *.sagews or *.sage.


        FUTURE IDEAS:
        
        Argument has two possibilities:
        
        - a "basename" of an existent file: in this case, an existent \
        filename is searched and a new filename with increased counter is created. 
        - a full filename, including extension and type.
        
        Type is:
        
           - fullname (com MSC, com número inicial, com _latex, _siacua): 
           procura existentes, adiciona a contagem, vai buscar um modelo baseado no anterior

           - args[0]: basename  (sem MSC e sem número final)
           - args[1]: sagews, sage, ...  #extraído do .megua/mconfig.sh MEGUA_EXERCISE_DEFAULTEXT
           - args[2]: latex, siacua, moodle #extraído do .megua/mconfig.sh MEGUA_EXERCISE_DESTINY
        
        Automatic Process:
        
            - megua check all | <some exercise> 
            - command meg.save() could try to adjust filename?
        
        """

        # Directory where exercises are stored

        fullpath = os.path.join(
            environ["MEGUA_EXERCISE_INPUT"],
            filename)
        
        if os.path.isfile(fullpath) :
            print "Megbook.py say: '%s' already exists. Choose another name" % filename
            return

        # =====
        # decision by file type
        # =====

        if filename[-7:] == '.sagews':

            # =====
            # decision by exercise type
            # =====

            if '_latex' in filename:
                
                htmlstr = u'<h4>%s (Latex)</h4>' % filename[0:-7]
                
                e_string = templates.render("megbook_exlatex.sagews",
                    unique_name=filename[0:-7],
                    megbookfilename=environ["PROJECT_FILENAME"], #self.local_store_filename,
                    uuid1=uuid(),
                    uuid2=uuid(),
                    uuid3=uuid(),
                    uuid4=uuid(),
                    marker_cell=MARKERS["cell"],
                    marker_output=MARKERS["output"],
                    html=htmlstr,
                    json_html=json.dumps({'html':htmlstr})
                )

                with codecs.open(fullpath, mode='w', encoding='utf-8') as f:
                    f.write(e_string)

            elif '_siacua' in filename:
                
                htmlstr = u'<h4>%s (Siacua)</h4>' % filename[0:-7]
                
                e_string = templates.render("megbook_exsiacua.sagews",
                    unique_name=filename[0:-7],
                    megbookfilename=environ["PROJECT_FILENAME"], 
                    uuid1=uuid(),
                    uuid2=uuid(),
                    uuid3=uuid(),
                    uuid4=uuid(),
                    uuid5=uuid(),
                    uuid6=uuid(),
                    uuid7=uuid(),
                    uuid8=uuid(),
                    course=environ["COURSE"],
                    usernamesiacua=environ["USERNAME_SIACUA"],
                    marker_cell=MARKERS["cell"],
                    marker_output=MARKERS["output"],
                    html=htmlstr,
                    json_html=json.dumps({'html':htmlstr})
                )

                with codecs.open(fullpath, mode='w', encoding='utf-8') as f:
                    f.write(e_string)

            else:
                
                print templates.render("megbook_new_exercise_usage.txt")
            
        elif filename[-5:] == '.sage':

            # =====
            # decision by exercise type
            # =====

            if '_latex' in filename:
                
                e_string = templates.render("megbook_exlatex.sage",
                    unique_name=filename[0:-5],
                    megbookfilename=self.local_store_filename,
                )

                with codecs.open(fullpath, mode='w', encoding='utf-8') as f:
                    f.write(e_string)

            elif '_siacua' in filename:
                
                e_string = templates.render("megbook_exsiacua.sage",
                    unique_name=filename[0:-5],
                    megbookfilename=self.local_store_filename,
                )

                with codecs.open(fullpath, mode='w', encoding='utf-8') as f:
                    f.write(e_string)

            else:
                
                print templates.render("megbook_new_exercise_usage.txt")
            
            
        else:

            print templates.render("megbook_new_exercise_usage.txt")
            #print "Megbook.py say: filename must be " 
            #    "a name in form E12X34_SomeName_001_latex ou "
            #    "_siacua or _moodle and related extension *.sagews or *.sage."
            return


        if environ["MEGUA_PLATFORM"]=='SMC':
            if environ["MEGUA_BASH_CALL"]=='on': #see megua bash script at megua/megua
                print "MegBook module say:  open ", fullpath
                #Does not work in SMC: subprocess.Popen(["/bin/open",CATALOG_PDF_PATHNAME])
                #Does not work using "sage -python": from smc_pyutil import smc_open
                #Works using: "python": from smc_pyutil import smc_open
                #                        smc_open.process([CATALOG_PDF_PATHNAME])
                #WORKS:subprocess.call(["openpdf.py",CATALOG_PDF_PATHNAME])
                #ANOTHER SOLUTION (http://stackoverflow.com/questions/3402168/permanently-add-a-directory-to-pythonpath)
                sys.path.append('/usr/local/lib/python2.7/dist-packages')
                from smc_pyutil import smc_open
                smc_open.process([fullpath])
            else: #sagews SALVUS
                from smc_sagews.sage_salvus import salvus
                salvus.open_tab(fullpath)
        elif environ["MEGUA_PLATFORM"]=='DESKTOP':
            print "MegBook module say: gvim ",fullpath
            subprocess.Popen(["gvim",fullpath])
        else:
            print """MegBook module say: environ["MEGUA_PLATFORM"] must be properly configured at $HOME/.megua/mconfig.sh"""


        
        
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
        #try:
        #First check: syntatic level ("megua" script)
        
        row =  parse_ex(to_unicode(uexercise))
        
        #print """megbook.py say: in save the type(row["summary_text"])=""",type(row["summary_text"])
        
        if not row:
            raise
            
        ex_instance = self.exerciseinstance(row,ekey=0)

            
        #Second check: syntatic and runtime  ("python/sagemath" script)
        ######
        #Third check: create contens (latex compilation, for example)
        ex_instance.print_instance()

#       except:
#           print "Exercise was not saved."
        
        
        #After all that, save it on database:                        
        self.megbook_store.insertchange(row)
        


    def new(self, unique_name=None, ekey=None, edict=None, returninstance=False):
        r"""Prints an exercise instance of a given type

        INPUT:

         - ``unique_name`` -- the class name.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.
         - ``returninstance`` -- if True, this function return a python object.

        OUTPUT:
            An instance of class named ``unique_name``.

        if ``unique_name`` is None then self._current_unique_name is used. 

        """
        
        if not unique_name:
            unique_name = self._current_unique_name
            
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(unique_name)
        if not row:
            print "%s cannot be accessed on database" % unique_name
            return
        
        #Create and print the instance
        ex_instance = self.exerciseinstance(row, ekey, edict)
        
        if returninstance:
            return ex_instance

        ex_instance.print_instance()

    

    
    def exerciseinstance(self, row, ekey=None, edict=None):
        r"""
        This function creates an instance of a class named in parameter row["unique_name"]. 
    
        INPUT:
    
         - ``row``-- a dictionary containing fields: 'summary_text', 'problem_text',  'answer_text'.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.
    
        OUTPUT:
            An instance of class named ``unique_namestring``.
    
        FIELDS in row:
    
        - row['unique_name']
        - row['sections_text']
        - row['suggestive_name']
        - row['summary_text']
        - row['problem_text']
        - row['answer_text']
        - row['class_text']

        DEVELOP:
    
        - http://docs.python.org/library/exceptions.html#exceptions.Exception
        - Note on python warnings: SageMath calls reset.... so use of warnings.filterwarnings('error') does not work with try...except.

        - To locate unicode problems in byte position 1508 use:
            - $ python -c "print hex(1508)"
            - $ hd E97H30_Equacaoliteral2_002_latex.sage

            TODO: escrever sobre isto
            http://stackoverflow.com/questions/1347791/unicode-error-unicodeescape-codec-cant-decode-bytes-cannot-open-text-file
                Unicode:
                 , errors="ignore"
                 warning: ur''' \underline{....} ''' generates an unicode error!
                 , errors='backslashreplace'
                
                >>> x = ur'\underline'
                  File "<stdin>", line 1
                SyntaxError: (unicode error) 'rawunicodeescape' codec can't decode bytes in position 0-1: truncated \uXXXX

                What does this mean?
                ##Author text must be <str> declared in a utf8.

                #See notes above. Avoid use of ur in strings 
                #because ur" \underline " causes error as \u is a command
                #Author text must be <str> declared in a utf8.
                #in cfilename the strings are saved like: r''' .... '''
                #so they must be converter to unicode again
                #This is to avoid ur''' \underline ''' make error because of \u !!!
                #The ExBase.update must then convert to unicode again!

        """
        
        code_string = templates.render("megbook_instance_new.sage",
            unique_name=row["unique_name"],
            class_text=row["class_text"],
            sumtxt=row['summary_text'],
            probtxt=row['problem_text'],
            anstxt=row['answer_text'],
            suggestivename=row['suggestive_name'],
            ekey = ekey,
            edict = edict
         )

        #Create if not exist: exercise working directory (images, latex,...)
        working_dir = os.path.join(environ["MEGUA_EXERCISE_OUTPUT"],row["unique_name"])
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        cfilename = os.path.join(working_dir,row["unique_name"]+'.sage')

        with codecs.open(cfilename, encoding='utf-8', mode='w') as f:
            f.write(code_string)

        try:
            with warnings.catch_warnings(record=True) as wlist:
                #See important notes about coding the contents of cfilename.
                load(cfilename) #sagemath load command
                
                if len(wlist)>0:
                    print 'MegBook.py say: exercise "%s" needs review! See below:' % row['unique_name']
                for w in wlist:
                    #print warnings.showwarning(w)
                    #Simple way of showing an warning: 
                    #print w
                    display_warning(w,code_string) #find in this file
                if len(wlist)>0:
                    print '======= end of warning list =========='

        except SyntaxError as s:
            print 'MegBook.py say: exercise "%s" causes a syntatical error and needs review! See below.' % row['unique_name']
            print 'See line %d in file "%s".' % (s.lineno,cfilename)
            display_syntaxerror(s,code_string)
            raise s
        
        
        
        return ex_instance #the value of ex_instance is created in load()
    
    



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



    def remove(self,unique_name,warn=True):
        r"""
        Removing an exercise from the database.

        INPUT:

        - ``unique_name`` -- the class name.
        - ``warn`` -- tell user if it was removed.        
        
        """
        assert(unique_name)

        #Get the exercise
        row = self.megbook_store.get_classrow(unique_name)
        
        if row:            
            e_string = templates.render("megbook_instance_new.sage",
                class_text=row['class_text'],
                unique_name=unique_name,
                sumtxt=row['summary_text'],
                probtxt=row['problem_text'],
                anstxt=row['answer_text'],
                suggestivename=row['suggestive_name'],
                sections=row['sections_text'],
                ekey=0
            )

            fname = os.path.join(environ["MEGUA_EXERCISE_INPUT"],"removed_"+unique_name+'.sage')
            
            #store it on a text file
            with codecs.open(fname, encoding='utf-8', mode='w') as f:
                f.write(e_string)
            print "Exercise '%s' has a backup in %s" % (unique_name,fname)

            #remove it
            self.megbook_store.remove_exercise(unique_name)
        elif warn:
            print "Exercise %s is not on the database." % unique_name




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
        r"""
        Writes exercises in an ordered fashion by sections.
        
        WARNING: Only working is what="all" and export="latex" for now.
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
                section = latexunderscore(s.sec_name)
                subsection = r""
                subsubsection = r""
                sname = latexunderscore(s.sec_name) #if exist _ => \_
                lts += u'\n\n\chapter{{{0} ({1})}}\n\n'.format(sname,len(s.exercises))
            elif s.level==1:
                subsection = latexunderscore(s.sec_name)
                subsubsection = r""
                sname = latexunderscore(s.sec_name) #if exist _ => \_
                lts += u'\n\n\section{{{0} ({1})}}\n\n'.format(sname,len(s.exercises))
            elif s.level==2:
                subsubsection = latexunderscore(s.sec_name)
                sname = latexunderscore(s.sec_name) #if exist _ => \_
                lts += u'\n\n\subsection{{{0} ({1})}}\n\n'.format(sname,len(s.exercises))
            else:
                sname = latexunderscore(s.sec_name) #if exist _ => \_
                lts += u'\n\n\subsubsection{{{0} ({1})}}\n\n'.format(sname,len(s.exercises))

            #Get the instances, if they exist on this section, subsection or subsubsection
            #TODO: image render mode to "filenameimage"
            lts += u'\n\nThis section has {0} exercises.\n\n'.format(len(s.exercises)) # {{ => }
            for unique_name in s.exercises:
                print "megbook.py say: producing %s" % unique_name
                ex = self.new(unique_name,ekey=0,returninstance=True)
                if ExLatex in ex.__class__.__bases__:
                    #TODO: incluir tipo no template e na section acima
                    ex_str = templates.render("megbook_catalog_instance.tex",
                                exformat="latex",
                                unique_name=unique_name,
                                unique_name_noslash = latexunderscore(unique_name),
                                summary = ex.summary(),
                                section=section,
                                subsection=subsection,
                                subsubsection=subsubsection,
                                suggestive_name = ex.suggestive_name(),
                                problem = ex.problem(),
                                answer = ex.answer()
                    )
                elif ExSiacua in ex.__class__.__bases__:
                    #TODO: incluir tipo no template e na section acima
                    ex_str = templates.render("megbook_catalog_instance.tex",
                                exformat="siacua",
                                unique_name=unique_name,
                                unique_name_noslash = latexunderscore(unique_name),
                                summary = ex.summary(),
                                section=section,
                                subsection=subsection,
                                subsubsection=subsubsection,
                                suggestive_name = ex.suggestive_name(),
                                problem = ExSiacua.to_latex(ex.problem()), #u'\\begin{verbatim}\n'+ex.problem()+'\n\\end{verbatim}\n',
                                answer = ExSiacua.to_latex(ex.answer()) #u'\\begin{verbatim}\n'+ex.answer()+'\n\\end{verbatim}\n'
                    )
                else:
                    #TODO: incluir tipo no template e na section acima
                    ex_str = templates.render("megbook_catalog_instance.tex",
                                exformat="textual (exbase)",
                                unique_name_noslash = latexunderscore(unique_name),
                                summary = ex.summary(),
                                section=section,
                                subsection=subsection,
                                subsubsection=subsubsection,
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

        latex_text =  templates.render("megbook_catalog_latex.tex",
                         exerciseinstanceslatex=lts)


        MEGUA_EXERCISE_CATALOG = environ["MEGUA_EXERCISE_CATALOG"]
        CATALOG_TEX_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOG,"catalog.tex")
        CATALOG_PDF_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOG,"catalog.pdf")


        #Compile two times because of TableOfContents  \toc
        pcompile(latex_text, MEGUA_EXERCISE_CATALOG, "catalog.tex")
        pcompile(latex_text, MEGUA_EXERCISE_CATALOG, "catalog.tex")


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



        
    def fast_exam_siacua(self, course="calculo2", concept_id=100, num_questions=10,siacuatest=True, exstate=""):
        r"""
        The command requests the Siacua system an exam with the following requirements:
        
        INPUT:
        
        - ``course'' : string  ("calculo2", "calculo3", "matbas", ...)
        - ``concept_id'': in the context of the course <3 digits>
        - ``num_questions'': number of questions
        - ``exstate`` : a string (empty or a combination of letters v,h,n, see below)
        
        OUTPUT:
        
        - Output a LaTeX file with an exam.
        - VERIFICAR SE O NUMERO DE EXCERCICIO É O PEDIDO OU ENTÃO AVISAR O PROFESSOR.
            
        The extate parameter receives a combination of letters meaning:

        - emtpy string (default) : requests the same as "vh";
        - "v": the exam can contain "visible" exercises (validated and visible);
        - "h": the exam can contain "hidden" exercises (validated but hidden);
        - "n": the exam can contain non validated (also hidden) exercises.


        DEVELOPMENT:    

        - TODO: warn when numberof questions is less then num_questions

        - The siacua.web.ua.pt returns:
        [["E44A10_TrLaplaceDef_002", 72, "v"],
         ["E44A10_TrLaplaceDef_002", 79, "v"],
         ["E44A10_TrLaplacePol1_001", 44, "v"],
         ["E44A10_TrLaplacePol2_002", 51, "v"],
         ["E44A10_TrLaplacePol2_002", 53, "v"],
         ["E44A10_TrLaplaceInv1_001", 829, "v"],
         ["E44A10_TrLaplaceInv2_002", 832, "v"],
         ["E44A10_TrLaplaceInv2_002", 837, "v"],
         ["E44A10_TrLaplaceInv4_004", 870, "v"],
         ["E44A10_TrLaplaceInv5_005",878, "v"]]
         <form name="formFastExam" method="post" action="./FastExam.aspx"
         ......

        TEM QUE SEGUIR ESTE FORMATO
        send_dict = { "course": "calculo2", "concept_id": 234, "num_questions": 10, "siacua_key": SIACUA_WEBKEY  }
           
        NO SIACUA:
        - de momento só vai buscar exercícios marcados como disponíveis para os alunos no siacua;  
        - Futuro: melhorar a catalogação para disponível/por rever/escondido para avaliação/ .....
        

        sage: from megua.all import *
        sage: meg.fast_exam_siacua(course="calculo2", concept_id=100, num_questions=10)

        About strings:        
        http://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string
        
        """
        
        #TODO Parameter Validation (improve this simple idea)
        
        exstate = exstate.lower() #  letters "VHN" to "vhn"
        exs = ''.join(exstate) #duplicate string
        exs = re.sub("[vhn]","",exs)
        if exs != "":
            print "Megbook.py say: exstate parameter must be a string with only 'vhn' chars."


        send_dict = { 
            "course": course, 
            "concept_id": concept_id, 
            "num_questions": num_questions, 
            "siacua_key": environ["SIACUA_WEBKEY"],
            "siacuatest": siacuatest,
            "exstate": exstate,
            
        }

        params = urllib.urlencode(send_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("siacuatest.web.ua.pt")
        if send_dict["siacuatest"]:
            conn = httplib.HTTPConnection("siacuatest.web.ua.pt")
        else:  
            conn = httplib.HTTPConnection("siacua.web.ua.pt")
        conn.request("POST", "/FastExam.aspx", params, headers)
        response = conn.getresponse()
        
        #print response.read()    
        if response.status!=200:
            print "Could not get an exam from server."
            print response.status, response.reason
            conn.close()
            return
            
        #print 'Sent to server:  "', send_dict["exname"], '" with ekey=', send_dict["ekey"] 
        #print response.status, response.reason
        #TODO: remove extra newlines that the user sees on notebook.
        data = response.read().strip()

        #parse response (see DEVELOPMENT notes above)
        pos = data.find("<")
        data = data[:pos] #remove <form ....> part!
        print "Response from Siacua:"
        print data
        print "========"


        #Join all questions
        lts = u'\\begin{enumerate}\n\n'            
        ex_list = eval(data) #creates the list

        for uniquename_ekey in ex_list:
            
            print "megbook.py module say: generating exercise %s." % uniquename_ekey 
            
            unique_name = uniquename_ekey[0]
            ekey = uniquename_ekey[1]
            ex = self.new(unique_name,ekey=ekey,returninstance=True)
            
            ex_str = templates.render("megbook_catalog_instance.tex",
                    exformat="siacua",
                    unique_name_noslash = unique_name.replace("_","\_"),
                    summary = ex.summary(),
                    suggestive_name = ex.suggestive_name(),
                    problem = ExSiacua.to_latex(ex.problem()), 
                    answer = ExSiacua.to_latex(ex.answer()) 
            )
            
            print "type of ex.summary() is", type( ex.summary() )
            lts += u'\n\\item '
            lts += ex_str
            
        lts += ur'\n\\end{enumerate}\n\n'
        
        latex_string =  templates.render("megbook_fastexam_latex.tex",
                         exerciseinstanceslatex=lts)


        MEGUA_EXERCISE_CATALOG = environ["MEGUA_EXERCISE_CATALOG"]
        CATALOG_TEX_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOG,"exam.tex")
        CATALOG_PDF_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOG,"exam.pdf")

        #Tirar isto
        f = codecs.open(CATALOG_TEX_PATHNAME+"lixo", mode='w+', encoding='utf8')
        f.write(ex.summary())
        f.close()


        f = codecs.open(CATALOG_TEX_PATHNAME, mode='w', encoding='utf-8')
        f.write(latex_string)
        f.close()

        #TODO: convert all os.system to subprocess.call or subprocess.Popen
        os.system("cd '%s'; pdflatex -interaction=nonstopmode %s 1> /dev/null" % (MEGUA_EXERCISE_CATALOG,"exam.tex") )
        os.system("cd '%s'; pdflatex -interaction=nonstopmode %s 1> /dev/null" % (MEGUA_EXERCISE_CATALOG,"exam.tex") )


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
            print """MegBook module say: in context of megbook.fast_exam_siacua() the environ["MEGUA_EXERCISE_CATALOG"] must be properly configured at $HOME/.megua/mconfig.sh"""



def m_get_sections(sectionstxt):
    r"""

    LINKS::

       http://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python?rq=1
    """
    s = "megua/"+sectionstxt.replace("; ","/") #case "; " by "/"
    return s.replace(";","/") #possible case without space: ";" by "/"


def display_warning(w,code_string):
    print w.message
    #print "Around line:",w.lineno #<-could be on runtime without line
    #print "Filename:",w.filename #<- always megbase.py ?
    code_list = code_string.split("\n")
    line = w.lineno
    if line>1:
        code_debug_str = '\n'.join(code_list[line-2:line+2])
    else:
        code_debug_str = '\n'.join(code_list[0:line+1])
    print code_debug_str 
        

def display_syntaxerror(s,code_string):
    print s.msg #specific error description
    print s.message #code where error is

    if '(unicode error)' in s.msg:
        print "Localte with" 
        print "   $ python -c \"print hex(<position of the byte>)\" "
        print "   $ hd <file.sage>"
        print "   and rewrite the full paragraph, maybe!"

    # strcuture of "s":    
    #'__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', 
    #'__getitem__', '__getslice__', '__hash__', '__init__', '__new__', '__reduce__', 
    #'__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', 
    #'__subclasshook__', '__unicode__', 'args', 'filename', 'lineno', 'message', 'msg', 
    #'offset', 'print_file_and_line', 'text']

def isidentifier(ident):
    """Determines, if string is valid Python identifier."""
    # http://stackoverflow.com/questions/12700893/how-to-check-if-a-string-is-a-valid-python-identifier-including-keyword-check
    return re.match("[_A-Za-z][_a-zA-Z0-9]*",ident) and not keyword.iskeyword(ident)

#end class MegBook


