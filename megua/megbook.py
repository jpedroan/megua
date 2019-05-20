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
   MegBook.py say: making instances of the exercises.
   megbook.py say: producing E28E28_pdirect_001
   MegBook.py say: compiling latex file containing the instances of the exercises.
   MegBook module say: evince  _output/catalog.pdf

Search an exercise:

::

  sage: meg.search("primitive")
  Exercise name E28E28_pdirect_001
  What is the long primitive of ap x + bp@() ?
  <BLANKLINE>

Remove an exercise:

::

   sage: meg.remove('E28E28_pdirect_001')
   Exercise 'E28E28_pdirect_001' has a backup in _input/removed_E28E28_pdirect_001.sage
   sage: meg.remove('E28E28_nonexistant')
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
#from os import environ
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
from megua.megoptions import *
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
            filename = PROJECT_DATABASE_FULLPATH

        #Create or open the database
        try:
            self.megbook_store = LocalStore(filename=filename,natlang=natlang,markuplang=markuplang)
            self.local_store_filename = self.megbook_store.local_store_filename #keep record.
            #print "Opened " + str(self)
        except sqlite3.Error as e:
            print ("Filename couldn't be opened: " , e.args[0], "\n")
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


        TESTING "set_current_exercise" on bash:

              * pasta all/sandbox/megua
             $  gvim teste_current_unique.sage
             $  sage teste_current_unique.sage 
             $  mv teste_current_unique.sage teste_current_unique2.sage
             $  sqlitebrowser /home/jpedro/all/calculo2/.calculo2.sqlite
             $  sage teste_current_unique2.sage 

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
            print ("Megbook.py: Filename is not a valid Python identifier.")
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
            print ("========================")
            print ("Please, ")
            print ("1. Execute the above comand again using shift-enter ('meg.set_current_exercise(__file__)').")
            print ("")
            print ("Explanation:")
            print ("1. The filename containing the exercise was renamed.")
            print ("2. The new name of the exercise is now: {}".format(unique_name))
            print ("3. Confirm the new <name_of_exercise> in the line 'class <name>(...)'.")
            print ("")
            print ("========================")
            raise IOError

        #To be used in all megbook commands
        self._current_unique_name = unique_name

        if MEGUA_PLATFORM=='SMC':
            sys.path.append('/cocalc/lib/python2.7/site-packages')
            from smc_sagews.sage_salvus import salvus
            salvus.html("<h4>{}&nbsp;&nbsp;{}</h4><p>{}</p>".format(
                    unique_name,
                    "(The dog picture has been stolen. Reward of $100000, dead or alive.)",
                    #DOGSVG, #'<img src="https://cloud.sagemath.com/4531e156-82ac-4387-8f19-b066e940b28b/raw/stationary/small_megua_dog.png"/>',
                    '<a href="https://github.com/jpedroan/megua/wiki" target=_blank>MEGUA wiki for help</a> or email to dmat-siacua@ua.pt.'
                ))
        elif MEGUA_PLATFORM=='DESKTOP':
            print ("Exercise {}".format(unique_name))
        else:
            print ("megbook.py module say: MEGUA_PLATFORM must be properly configured at $HOME/.megua/conf.py")



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

        #print "megbook.py, new_exercise:",filename

        fullpath = os.path.join(
            MEGUA_EXERCISE_INPUT,
            filename)

        if os.path.isfile(fullpath) :
            print ("Megbook.py say: '%s' already exists. Choose another name" % filename)
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
                    megbookfilename=PROJECT_DATABASE_NAME, #self.local_store_filename,
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

            elif '_amc' in filename:

                htmlstr = u'<h4>%s (Latex for AMC)</h4>' % filename[0:-7]

                e_string = templates.render("megbook_examc.sagews",
                    unique_name=filename[0:-7],
                    megbookfilename=PROJECT_DATABASE_NAME, #self.local_store_filename,
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
                    megbookfilename=PROJECT_DATABASE_NAME, 
                    uuid1=uuid(),
                    uuid2=uuid(),
                    uuid3=uuid(),
                    uuid4=uuid(),
                    uuid5=uuid(),
                    uuid6=uuid(),
                    uuid7=uuid(),
                    uuid8=uuid(),
                    course=SIACUA_COURSENAME,
                    usernamesiacua=SIACUA_USERNAME,
                    marker_cell=MARKERS["cell"],
                    marker_output=MARKERS["output"],
                    html=htmlstr,
                    json_html=json.dumps({'html':htmlstr})
                )

                with codecs.open(fullpath, mode='w', encoding='utf-8') as f:
                    f.write(e_string)

            else:

                print (templates.render("megbook_new_exercise_usage.txt"))
                return
                
            
        elif filename[-5:] == '.sage':

            # =====
            # decision by exercise type
            # =====

            #TODO: improve this

            if '_latex' in filename:
                
                e_string = templates.render("megbook_exlatex.sage",
                    unique_name=filename[0:-5],
                    megbookfilename=self.local_store_filename,
                )

                with codecs.open(fullpath, mode='w', encoding='utf-8') as f:
                    f.write(e_string)

            elif '_amc' in filename:
                
                e_string = templates.render("megbook_examc.sage",
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
                
                print (templates.render("megbook_new_exercise_usage.txt"))
                return
            
            
        else:

            print (templates.render("megbook_new_exercise_usage.txt"))
            #print "Megbook.py say: filename must be " 
            #    "a name in form E12X34_SomeName_001_latex ou "
            #    "_siacua or _moodle and related extension *.sagews or *.sage."
            return

        if MEGUA_PLATFORM=='SMC':
            sys.path.append('/cocalc/lib/python2.7/site-packages')
            from smc_sagews.sage_salvus import salvus
            if salvus:
                print ("Worksheet")
                salvus.file(fullpath,show=True,raw=True); 
                print ("\n")
                salvus.open_tab(fullpath)
            else:
                print ("Command line")
                sys.path.append('/usr/local/lib/python2.7/dist-packages')
                from smc_pyutil import smc_open
                smc_open.process([fullpath])                
        elif MEGUA_PLATFORM=='DESKTOP':
            print ("MegBook module say: gvim ",fullpath)
            subprocess.Popen(["gvim",fullpath])
        else:
            print ("megbook.py module say: MEGUA_PLATFORM must be properly configured at $HOME/.megua/conf.py")


    def replicate_exercise(self,filename):
        r"""
        
        TODO TODO TODO: esta rotina não foi acabada. Muitos detalhes.
        
        Replicate contents of filename and only change the number, increasing it.

        INPUT:
        - `filename`: a name in form E12X34_SomeName_001_latex ou _siacua or _moodle and related extension *.sagews or *.sage.


        See def new_exercise() above.

        """

        # Directory where exercises are stored

        #print "megbook.py, new_exercise:",filename

        fullpath = os.path.join(
            MEGUA_EXERCISE_INPUT,
            filename)

        if not os.path.isfile(fullpath) :
            print ("Megbook.py say: '%s' does not exist. Choose another name to replicate" % filename)
            return

        # =====
        # decision by file type
        # =====

        if filename[-7:] == '.sagews':

            # =====
            # decision by exercise type
            # =====

            if '_latex' in filename:

                print ("megbook.py, replicate_exercise: not implemented for this case.")
                return

                htmlstr = u'<h4>%s (Latex)</h4>' % filename[0:-7]

                e_string = templates.render("megbook_exlatex.sagews",
                    unique_name=filename[0:-7],
                    megbookfilename=PROJECT_DATABASE_NAME, #self.local_store_filename,
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

            elif '_amc' in filename:

                print ("megbook.py, replicate_exercise: not implemented for this case.")
                return
                htmlstr = u'<h4>%s (Latex for AMC)</h4>' % filename[0:-7]

                e_string = templates.render("megbook_examc.sagews",
                    unique_name=filename[0:-7],
                    megbookfilename=PROJECT_DATABASE_NAME, #self.local_store_filename,
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

                # "_" is on -14:  '_siacua.sagews':
                # "0" is on -17:  '001_siacua.sagews':

                print (filename)
                #invert the string
                i_filename = filename[-15::-1]; print (i_filename)
                #find next "_"
                pos = i_filename.index("_")
                #get number
                nums = i_filename[0:pos][::-1]; print (nums)
                #get value
                value = int(nums)+1; print (value)
                newnums = "%03d" % value; print (newnums)
                #TODO: i'm here
                new_filename = filename[:-17] + newnums + "_siacua.sagews"; print (new_filename)

                fullpath_new = os.path.join( MEGUA_EXERCISE_INPUT, new_filename)

                shutil.copy(fullpath,fullpath_new)
                
            else:

                print (templates.render("megbook_new_exercise_usage.txt"))
                return
                
            
        elif filename[-5:] == '.sage':

            print ("megbook.py, replicate_exercise: not implemented for this case.")
            return

            # =====
            # decision by exercise type
            # =====

            #TODO: improve this

            if '_latex' in filename:
                
                e_string = templates.render("megbook_exlatex.sage",
                    unique_name=filename[0:-5],
                    megbookfilename=self.local_store_filename,
                )

                with codecs.open(fullpath, mode='w', encoding='utf-8') as f:
                    f.write(e_string)

            elif '_amc' in filename:
                
                e_string = templates.render("megbook_examc.sage",
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
                
                print (templates.render("megbook_new_exercise_usage.txt"))
                return
            
            
        else:

            print (templates.render("megbook_new_exercise_usage.txt"))
            #print "Megbook.py say: filename must be " 
            #    "a name in form E12X34_SomeName_001_latex ou "
            #    "_siacua or _moodle and related extension *.sagews or *.sage."
            return


        if MEGUA_PLATFORM=='SMC':
            sys.path.append('/cocalc/lib/python2.7/site-packages')
            from smc_sagews.sage_salvus import salvus
            if salvus:
                #salvus.file(fullpath_new,show=True,raw=True); print "\n"
                print (fullpath_new)
                print ("salvus.open_tab(fullpath_new)")
            else:
                sys.path.append('/usr/local/lib/python2.7/dist-packages')
                from smc_pyutil import smc_open
                smc_open.process([fullpath_new])
        elif MEGUA_PLATFORM=='DESKTOP':
            print ("MegBook module say: gvim ",fullpath)
            subprocess.Popen(["gvim",fullpath])
        else:
            print ("megbook.py module say: MEGUA_PLATFORM must be properly configured at $HOME/.megua/conf.py")


        
        
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
        #print "megbook.py: type(uexercise) is",type(uexercise)
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
            print ("%s cannot be accessed on database" % unique_name)
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

                <python> x = ur'\underline'
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
        working_dir = os.path.join(MEGUA_WORKDIR_FULLPATH,row["unique_name"])
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
                    print ('MegBook.py say: exercise "%s" needs review! See below:' % row['unique_name'])
                for w in wlist:
                    #print warnings.showwarning(w)
                    #Simple way of showing an warning: 
                    #print w
                    display_warning(w,code_string) #find in this file
                if len(wlist)>0:
                    print ('======= end of warning list ==========')

        except SyntaxError as s:
            print ('MegBook.py say: exercise "%s" causes a syntatical error and needs review! See below.' % row['unique_name'])
            if s.lineno is not None:
                print ('See line %d in file "%s".' % (s.lineno,cfilename))
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
        print (sname + '\n' + exrow['problem_text'].encode('utf8') + '\n')
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

            fname = os.path.join(MEGUA_EXERCISE_INPUT,"removed_"+unique_name+'.sage')
            
            #store it on a text file
            with codecs.open(fname, encoding='utf-8', mode='w') as f:
                f.write(e_string)
            print ("Exercise '%s' has a backup in %s" % (unique_name,fname))

            #remove it
            self.megbook_store.remove_exercise(unique_name)
        elif warn:
            print ("Exercise %s is not on the database." % unique_name)




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

            print ("Generating sample of",problem_name)

            #print "Write",(problem_name,ekey),"in thesis."

            #generate problem and answer text (choices are in the answer part)

            #Get summary, problem and answer and class_text
            row = self.megbook_store.get_classrow(problem_name)
            if not row:
                print ("meg.thesis(): %s cannot be accessed on database" % problem_name)
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


        print ('\nInstrucoes:\n1. Use o botao direito e "Save link as..." para guardar "thesis_problems.tex" no seu computador.')
        print ('2. Se houver imagens, o conteudo do ficheiro "images.zip" deve ser colocado numa pasta "images".')
        print ('3. Sera necessaria paciencia para finalizar a pre conversao de HTML para LaTeX em cada exercicio.')
        print ('4. Recomenda-se adaptar um exercicio de cada vez compilado um por um.')
    





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
        print ("MegBook.py say: making instances of the exercises.")
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
                print ("megbook.py say: producing %s" % unique_name)
                try:
                    ex = self.new(unique_name,ekey=0,returninstance=True)

                    #Copy images to CATALOG/IMG directory
                    for fp in ex.image_fullpathnames:
                        shutil.copy(fp,os.path.join(MEGUA_EXERCISE_CATALOGS,"IMG")) #TODO: autom. create IMG

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
                except:
                    ex_str = "Check problem with %s. It was not generated." % unique_name
                    print ("megbook.py: exercise %s was not generated for catalog. Please check it." % unique_name)


                lts += ex_str

                #Only for latex (was first version)
                #lts += u'\\bigskip\n\\textbf{{Unique Name {0}}} with ekey=0\n'.format(unique_name.replace("_","\_"))
                #lts += u'%{0}\n\n'.format(unique_name)
                #lts += u'\\textbf{{Summary}}\n\n\\begin{{verbatim}}\n{0}\n\\end{{verbatim}}\n\n'.format(ex.summary())
                #lts += u'\\textbf{{Problem {0}}}\n\n{1}\n\n'.format(
                #    ex.suggestive_name(),
                #    ex.problem())
                #lts += u'\\textbf{{Answer}}\n\n{0}\n\n'.format(ex.answer())


        print ("MegBook.py say: compiling latex file containing the instances of the exercises.")

        latex_text =  templates.render("megbook_catalog_latex.tex",
                         exerciseinstanceslatex=lts)


        CATALOG_TEX_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOGS,"catalog.tex")
        CATALOG_PDF_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOGS,"catalog.pdf")


        #Compile two times because of TableOfContents  \toc
        try:
            pcompile(latex_text, MEGUA_EXERCISE_CATALOGS, "catalog.tex")
            pcompile(latex_text, MEGUA_EXERCISE_CATALOGS, "catalog.tex")
        except:
            print ("="*30)
            print ("megbook.py: file catalog.tex need to be edited.")
            print (CATALOG_TEX_PATHNAME)
            print ("="*30)
            return


        if MEGUA_PLATFORM=='SMC':
            sys.path.append('/cocalc/lib/python2.7/site-packages')
            from smc_sagews.sage_salvus import salvus
            if salvus:
                salvus.file(CATALOG_PDF_PATHNAME,show=True,raw=True); 
                print ("\n")
                salvus.file(CATALOG_TEX_PATHNAME,show=True,raw=True); 
                print ("\n")
                salvus.open_tab(CATALOG_PDF_PATHNAME)
            else:
                sys.path.append('/usr/local/lib/python2.7/dist-packages')
                from smc_pyutil import smc_open
                smc_open.process([CATALOG_PDF_PATHNAME])
        elif MEGUA_PLATFORM=='DESKTOP':
            print ("MegBook module say: evince ",CATALOG_PDF_PATHNAME)
            subprocess.Popen(["evince",CATALOG_PDF_PATHNAME])
        else:
            print ("megbook.py module say: MEGUA_EXERCISE_CATALOGS must be properly configured at $HOME/.megua/conf.py")




    def latex_document(self, latexdocument, exercisetemplate=None, ofilename='latex_document.tex', ekey=None):
        r"""
        Create LaTeX documents. Exercises are obtained with  `{{ put_here(...) }}` commands.

        INPUT:

        - ``latexdocument``: (string) contains the LaTeX to be compiled. Each exercise is obtained from database with `{{ put_here(...) }}` commands.

        - ``exercisetemplate``: (string) defines how and what is to be shown from each exercise.

        - ``ofilename``: (string) output filename (without extension)

        - ``ekey``: if `{{ put_here(...) }}`` commands do not mention ekey then generate ekeys setting this. 

        EXAMPLE:

            sage: ltdoc = r'''\documentclass{article} ....  {{ put_here("E12X34_soma_001",10) }} ....'''
            sage: meg.latex_document(ltdoc)

        NOTES:
        
            - Another possibility: {{ put_here("E65D05_forwarddifference_001",ekey=10,meg.SUMMARY|meg.PROBLEM|meg.ANSWER|meg.CODE) }}

            - http://jinja.pocoo.org/docs/templates/#assignments

        """


        #Get unicode and make a jinja2 template
        utxt = unicode(latexdocument,'utf-8')
        latexdoc_template = jinja2.Template(utxt)

        #Set seed
        if ekey:
            ur.start_at(ekey)

        #Render output using the given template for each exercise.
        #get a value for self.template_row
        if exercisetemplate is None:
            try:
                self.template_row = templates.get_template("row_template.tex")
            except jinja2.exceptions.TemplateNotFound:
                return "megbook.py say: missing template %s"%filename
        else:
            #Check or convert rowtemplate to unicode
            try:
                self.rowtemplate = unicode(exercisetemplate,'utf-8')
            except TypeError:
                self.rowtemplate = exercisetemplate
            self.template_row = jinja2.Template(exercisetemplate)


        #Create a latex string s ready to compile.
        doc_latex = latexdoc_template.render(put_here=self.put_here)

        #Create new file and save string s.
        #fp = open(ofilename,'w')
        #fp.write( s.encode('utf-8') )
        #res = fp.close()

        DOC_LATEX_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOGS,ofilename+'tex')
        DOC_PDF_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOGS,ofilename+'.pdf')


        try:
            pcompile(doc_latex, MEGUA_EXERCISE_CATALOGS, ofilename)
        except:
            print ("="*30)
            print ("megbook.py: file %s need to be edited." % (ofilename+'.tex'))
            print (DOC_LATEX_PATHNAME)
            print ("="*30)
            return


        if MEGUA_PLATFORM=='SMC':
            sys.path.append('/cocalc/lib/python2.7/site-packages')
            from smc_sagews.sage_salvus import salvus
            if salvus:
                salvus.file(DOC_PDF_PATHNAME,show=True,raw=True); 
                print ("\n")
                salvus.file(DOC_LATEX_PATHNAME,show=True,raw=True); 
                print ("\n")
                salvus.open_tab(DOC_PDF_PATHNAME)
            else:
                sys.path.append('/usr/local/lib/python2.7/dist-packages')
                from smc_pyutil import smc_open
                smc_open.process([DOC_PDF_PATHNAME])
        elif MEGUA_PLATFORM=='DESKTOP':
            print ("MegBook module say: evince ",DOC_PDF_PATHNAME)
            subprocess.Popen(["evince",DOC_PDF_PATHNAME])
        else:
            print ("megbook.py module say: MEGUA_EXERCISE_CATALOGS must be properly configured at $HOME/.megua/conf.py")



    def put_here(self,unique_name, ekey=None, edict=None, elabel="NoLabel", em=True):
        r"""
        Create an instance based on a template with key=owner_keystring.
        This routine is used on templates only.

        INPUT:

        - ``owner_keystring`` -- the exercise key.
        - ``ekey`` -- random seed.
        - ``edict`` -- dictionary to be used after random initialization of ex parameters.
        - ``elabel`` -- to be used for "\label" or "\ref" in LaTeX.
        - ``automc`` -- automatic multiple choice (chooses possibilities and prints them) (true ou false).

        OUTPUT:
            text string.

        NOTES: to be used with `template_create`.

        """

        #Get summary, problem and answer and class_text
        #Field row['class_text'] is needed to render the template. See below.
        row = self.megbook_store.get_classrow(unique_name)        
        if not row:
            #TODO: passar a raise Error
            print ("%s cannot be accessed on database" % unique_name)
            return "\n\n\\vspace*{1cm}%s cannot be accessed on database.\n\n\\vspace*{1cm}\n\n" % latexunderscore(unique_name)

           
        #Get summary, problem and answer and class_text
        ex = self.new(unique_name,ekey,edict,returninstance=True)
        
        if ExLatex in ex.__class__.__bases__:
            #TODO: incluir tipo no template e na section acima
            ex_str = self.template_row.render(
                exformat="latex",
                unique_name=unique_name,
                unique_name_noslash = latexunderscore(unique_name),
                summary = to_unicode(ex.summary()),
                #section=section, #todo fields:
                #subsection=subsection,
                #subsubsection=subsubsection,
                suggestive_name = ex.suggestive_name(),
                problem = ex.problem(),
                answer = ex.answer(),
                #code                
                problemtemplate = to_unicode( ex_instance._problem_text ), 
                answertemplate  = to_unicode( ex_instance._answer_text ), 
                codetxt =  to_unicode( row['class_text'] ), 
                #what is this : elabel  =  elabel,
                ekey = ekey
            )
        elif ExSiacua in ex.__class__.__bases__:
            #TODO: incluir tipo no template e na section acima
            ex_str = self.template_row.render(
                exformat="siacua",
                unique_name=unique_name,
                unique_name_noslash = latexunderscore(unique_name),
                summary = to_unicode(ex.summary()),
                #section=section, #todo fields:
                #subsection=subsection,
                #subsubsection=subsubsection,
                suggestive_name = ex.suggestive_name(),
                problem = ExSiacua.to_latex(ex.problem()),  #u'\\begin{verbatim}\n'+ex.problem()+'\n\\end{verbatim}\n',
                answer = ExSiacua.to_latex(ex.answer()),    #u'\\begin{verbatim}\n'+ex.answer()+'\n\\end{verbatim}\n'
                #code                
                problemtemplate = to_unicode( ex._problem_text ), 
                answertemplate  = to_unicode( ex._answer_text ), 
                codetxt =  to_unicode( row['class_text'] ), 
                #what is this : elabel  =  elabel,
                ekey = ekey
            )
        else:
            #TODO: incluir tipo no template e na section acima
            ex_str = self.template_row.render(
                exformat="textual (exbase)",
                unique_name=unique_name,
                unique_name_noslash = latexunderscore(unique_name),
                summary = to_unicode(ex.summary()),
                #section=section,
                #subsection=subsection,
                #subsubsection=subsubsection,
                suggestive_name = ex.suggestive_name(),
                problem = u'\\begin{verbatim}\n'+ex.problem()+'\n\\end{verbatim}\n',
                answer = u'\\begin{verbatim}\n'+ex.answer()+'\n\\end{verbatim}\n',
                #code                
                problemtemplate = to_unicode( ex._problem_text ), 
                answertemplate  = to_unicode( ex._answer_text ), 
                codetxt =  to_unicode( row['class_text'] ), 
                #what is this : elabel  =  elabel,
                ekey = ekey
            )

        return ex_str



        
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


        Examples:

        (sage:) from megua.all import *
        (sage:) meg.fast_exam_siacua(course="calculo2", concept_id=100, num_questions=10)

        About strings:        
        http://stackoverflow.com/questions/24804453/how-can-i-copy-a-python-string

        """

        #TODO Parameter Validation (improve this simple idea)

        exstate = exstate.lower() #  letters "VHN" to "vhn"
        exs = ''.join(exstate) #duplicate stringnum_questions
        exs = re.sub("[vhn]","",exs)
        if exs != "":
            print ("Megbook.py say: exstate parameter must be a string with only 'vhn' chars.")

        send_dict = { 
            "course": course,
            "concept_id": concept_id,
            "num_questions": num_questions * 2, #requests more exercises because some
                                                #of them could be in siacua but on in database
            "siacua_key": SIACUA_WEBKEY,
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
            print ("Could not get an exam from server.")
            print (response.status, response.reason)
            conn.close()
            return
        #print 'Sent to server:  "', send_dict["exname"], '" with ekey=', send_dict["ekey"] 
        #print response.status, response.reason
        #TODO: remove extra newlines that the user sees on notebook.
        data = response.read().strip()

        #parse response (see DEVELOPMENT notes above)
        pos = data.find("<")
        data = data[:pos] #remove <form ....> part!
        #print "Response from Siacua:"
        #print data
        #print "========"
        s = "System siacua (or siacuatest) has randomly collected, according to bayesian tree with weigths, the following exercises:"
        print ("="*len(s))
        print (s)
        print ("="*len(s),"\n")
        

        #Join all questions
        lts = u'\\begin{enumerate}\n\n'
        ex_list = eval(data) #creates the list

        #requests more exercises because some of them could be in siacua but on in database
        count = 0 
        
        for uniquename_ekey in ex_list:


            #TODO: temporary while siacua unique_keys don't have "_siacua" at end
            #TODO: se no SIACUA, o unique_name for E12X34_nome_001_siauca_disciplina da mal. Deve ser "disciplina_nome_siacua"!
            if uniquename_ekey[0][-7:] == '_siacua':
                unique_name = uniquename_ekey[0]
            else:
                unique_name = uniquename_ekey[0]+'_siacua'

            ekey = uniquename_ekey[1]

            print ("megbook.py module say: generating exercise %s." % unique_name, "with ekey=",ekey, "\n\n")

            ex = self.new(unique_name,ekey=ekey,returninstance=True)

            #print ex
            
            if not ex:
                print ("megbook.fast_exam_siacua: exercise", unique_name, "is not on database.")
                continue

            ex_str = templates.render("megbook_catalog_instance.tex",
                    exformat ="siacua",
                    unique_name_noslash = unique_name.replace("_","\_"),
                    summary = ex.summary(),
                    suggestive_name = ex.suggestive_name(),
                    problem = ExSiacua.to_latex(ex.problem()), 
                    answer = ExSiacua.to_latex(ex.answer()) 
            )

            #print "type of ex.summary() is", type( ex.summary() )
            lts += u'\n\\item '
            lts += ex_str
            count = count + 1
            
            #requests more exercises because some of them could be in siacua but on in database
            if count == num_questions:
                break

        lts += ur'\n\\end{enumerate}\n\n'

        latex_string =  templates.render("megbook_fastexam_latex.tex",
                         exerciseinstanceslatex=lts)

        #SMC open_tab need the path to be relative to working directory:
        #EXAM_TEX_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOGS,"exam.tex")
        #EXAM_PDF_PATHNAME = os.path.join(MEGUA_EXERCISE_CATALOGS,"exam.pdf")
        EXAM_TEX_PATHNAME = "exam.tex"
        EXAM_PDF_PATHNAME = "exam.pdf"

        #Tirar isto
        f = codecs.open(EXAM_TEX_PATHNAME+"lixo", mode='w+', encoding='utf8')
        f.write(ex.summary())
        f.close()


        f = codecs.open(EXAM_TEX_PATHNAME, mode='w', encoding='utf-8')
        f.write(latex_string)
        f.close()

        #TODO: convert all os.system to subprocess.call or subprocess.Popen
        #os.system("cd '%s'; pdflatex -interaction=nonstopmode %s 1> /dev/null" % (MEGUA_EXERCISE_CATALOGS,"exam.tex") )
        #os.system("cd '%s'; pdflatex -interaction=nonstopmode %s 1> /dev/null" % (MEGUA_EXERCISE_CATALOGS,"exam.tex") )
        os.system("pdflatex -interaction=nonstopmode %s 1> /dev/null" % "exam.tex" )
        os.system("pdflatex -interaction=nonstopmode %s 1> /dev/null" % "exam.tex" )


        if MEGUA_PLATFORM=='SMC':
            sys.path.append('/cocalc/lib/python2.7/site-packages')
            from smc_sagews.sage_salvus import salvus
            if salvus:
                print ("Check exam PDF file:")
                salvus.file(EXAM_PDF_PATHNAME,show=True,raw=True); print "\n"
                print ("Save tex file to your computer to improve the text at",EXAM_TEX_PATHNAME)
                salvus.file(EXAM_TEX_PATHNAME,show=True,raw=True); print "\n"
                salvus.open_tab(EXAM_TEX_PATHNAME)
            else:
                sys.path.append('/usr/local/lib/python2.7/dist-packages')
                from smc_pyutil import smc_open
                smc_open.process([EXAM_TEX_PATHNAME])
        elif MEGUA_PLATFORM=='DESKTOP':
            print ("MegBook module say: evince ",EXAM_PDF_PATHNAME)
            subprocess.Popen(["evince",EXAM_PDF_PATHNAME])
        else:
            print ("megbook.py module say: in context of megbook.fast_exam_siacua() the MEGUA_EXERCISE_CATALOGS must be properly configured at $HOME/.megua/conf.py")



def m_get_sections(sectionstxt):
    r"""

    LINKS::

       http://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python?rq=1
    """
    s = "megua/"+sectionstxt.replace("; ","/") #case "; " by "/"
    return s.replace(";","/") #possible case without space: ";" by "/"


def display_warning(w,code_string):
    print (w.message)
    #print "Around line:",w.lineno #<-could be on runtime without line
    #print "Filename:",w.filename #<- always megbase.py ?
    code_list = code_string.split("\n")
    line = w.lineno
    if line>1:
        code_debug_str = '\n'.join(code_list[line-2:line+2])
    else:
        code_debug_str = '\n'.join(code_list[0:line+1])
    print (code_debug_str) 
        

def display_syntaxerror(s,code_string):
    print (s.msg) #specific error description
    #TODO: print s.message #code where error is

    if '(unicode error)' in s.msg:
        print ("Localte with")
        print ("   $ python -c \"print hex(<position of the byte>)\" ")
        print ("   $ hd <file.sage>")
        print ("   and rewrite the full paragraph, maybe!")

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


