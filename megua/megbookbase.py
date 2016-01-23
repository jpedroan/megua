r"""
MegBookBase -- Base class for build your own database of exercises on some markup language.

MegBookBase is ready for textual form exercises. See derivatives of this class for
other markup languages.


AUTHORS:

- Pedro Cruz (2012-06): initial version (based on megbook.py)
- Pedro Cruz (2016-01): version for SMC.

"""

# Abstract function
# raise NotImplementedError( "Should have implemented this" )


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#megua modules:
from mconfig import * #megua configuration file: server side settings.
from localstore import LocalStore,ExIter
from ex import *
from exerparse import exerc_parse


#Because sage.plot.plot.EMBEDDED_MODE
#This variable indicates if notebook is present.
#Trying no include now the EMBEDDED_MODE and wait for some place else:
from sage.all import *

#Python modules:
import sqlite3 #for row objects as result from localstore.py
import shutil
import os
import random 
#import codecs


# Jinja2 package
import jinja2
#from jinja2 import Environment, PackageLoader,FileSystemLoader,Template, TemplateNotFound
#Note on Jinja2:
# di = { 'ex_10_0_4': 10 }
# template.stream(di).dump('new.tex')
# print "Template folders are: " + str(env.loader.searchpath)


class MegBookBase:
    r"""
    Base routines for exercise templating. Abstract class.

    INPUT::

    - ``filename`` -- filename where the database is stored.

    This module provides a means to produce a database of exercises that can be seen as a book of some author or authors.

    Using exercices:

    - create, edit and delete exercises from a database.
    - search for an exercise or set of exercises.
    - create a random instance from a set or single exercise
    - create an instance based on specific parameters
    - create latex (and PDF) from a single or a set of exercises.


    Examples of use:

    .. test with: sage -python -m doctest megbook.py

    Create or edit a database::

       >>> from all import *
       >>> meg = MegBookBase(r'.testoutput/megbasedb.sqlite')
       MegBook opened. Execute `MegBook?` for examples of usage.
       Templates for 'pt_pt' language.


    Save a new or changed exercise::

       >>> txt=r'''
       ... %Summary Primitives
       ... Here one can write few words, keywords about the exercise.
       ... For example, the subject, MSC code, and so on.
       ...   
       ... %Problem
       ... What is the primitive of ap x + bp@() ?
       ... 
       ... %Answer
       ... The answer is prim+C, with C a real number.
       ... 
       ... class E28E28_pdirect_001(Exercise):
       ... 
       ...     def make_random(self):
       ...         self.ap = ZZ.random_element(-4,4)
       ...         self.bp = self.ap + QQ.random_element(1,4)
       ... 
       ...     def solve(self):
       ...         x=SR.var('x')
       ...         self.prim = integrate(self.ap * x + self.bp,x)
       ... '''
       >>> meg.save(txt,dest=r'.testoutput')
       Each problem can have a suggestive name. 
       Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.
       <BLANKLINE>
       Testing python/sage class 'E28E28_pdirect_001' with 100 different keys.
           No problems found in this test.
          Compiling 'E28E28_pdirect_001' with pdflatex.
          No errors found during pdflatex compilation. Check E28E28_pdirect_001.log for details.
       Exercise name E28E28_pdirect_001 inserted or changed.

    Search an exercise:

      >>> meg.search("primitive")
      Exercise name E28E28_pdirect_001
      <BLANKLINE>
      %problem 
      What is the primitive of ap x + bp@() ?
      <BLANKLINE>
      <BLANKLINE>
      <BLANKLINE>

    Remove an exercise:

       >>> meg.remove('E28E28_pdirect_001',dest=r'.testoutput')
       Exercise 'E28E28_pdirect_001' stored on text file .testoutput/E28E28_pdirect_001.txt.
       >>> meg.remove('E28E28_nonexistant',dest=r'.testoutput')
       Exercise E28E28_nonexistant is not on the database.
    """

    def __init__(self,filename=None,natlang='pt_pt',markuplang='text'): #TODO: utf-8 instead of asciitext?
        r"""

        INPUT::
        - ``filename`` -- filename where the database is stored.
        - ``natlang`` -- For example, 'pt_pt', for portuguese (of portugal), 'en_us' for english from USA.
        - ``markuplang`` -- 'latex' or 'web'.

        """
    
        #Sage and sagenotebook DATA variable is only defined after 
        #worksheet is opened so it cannot be imported to here.

        #Create or open the database
        try:
            self.megbook_store = LocalStore(filename=filename,natlang=natlang,markuplang=markuplang)
            self.local_store_filename = self.megbook_store.local_store_filename #keep record.
            print "Opened " + str(self)
        except sqlite3.Error as e:
            print "Filename couldn't be opened: " , e.args[0], "\n"
            raise e

        #Templating (with Jinja2)
        if os.environ.has_key('MEGUA_TEMPLATE_PATH'):
            TEMPLATE_PATH = os.environ['MEGUA_TEMPLATE_PATH']
        else:
            from pkg_resources import resource_filename
            TEMPLATE_PATH = os.path.join(resource_filename(__name__,''),'template',natlang)
        print "Templates for '%s' language at %s" % (natlang,TEMPLATE_PATH)
        #print "Templates in: " + TEMPLATE_PATH
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH))

        #For template. See template_create function.
        self.template_row = None

        Exercise.megbook = self


    def __str__(self):
        return "MegBookBase(%s) for natural language %s and markup language  %s." % (self.local_store_filename,self.natlang,self.markuplang)

    def __repr__(self):
        return "MegBookBase(%s)" % (self.local_store_filename)

    def template(self, filename, **user_context):
        """
        Returns HTML, CSS, LaTeX, etc., for a template file rendered in the given
        context.

        INPUT:

        - ``filename`` - a string; the filename of the template relative
          to ``sagenb/data/templates``

        - ``user_context`` - a dictionary; the context in which to evaluate
          the file's template variables

        OUTPUT:

        - a string - the rendered HTML, CSS, etc.

        BASED ON:

           /home/.../sage/devel/sagenb/sagenb/notebook/tempate.py

        """

        try:
            tmpl = self.env.get_template(filename)
        except jinja2.exceptions.TemplateNotFound:
            return "MegUA -- missing template %s"%filename
        r = tmpl.render(**user_context)
        return r


    def save(self,exercisestr,dest='.'):
        r"""
        Save an exercise defined on a `python string`_ using a specific sintax defined here_.

        INPUT::

        - ``exercisestr`` -- a `python string`_ text containing a summary, problem, answer and class according to meg exercise sintax.
        - ``dest`` -- directory where possible compilation will be done.

        OUTPUT::

            Textual messages with errors.
            Check ``dest`` directory (default is current) for compilation results.

        .. _python string: http://docs.python.org/release/2.6.7/tutorial/introduction.html#strings

        """

        #print "TYPE OF INPUT ", str(type(exercisestr))

        if type(exercisestr)==str:
            exercisestr = unicode(exercisestr,'utf-8')


        # ---------------------------------------
        # Check exercise syntax: 
        #    summary, problem, answer and class.
        # ---------------------------------------
        row = exerc_parse(exercisestr)

        if not row:
            print self.template('exercise_syntax.txt')
            print "==================================="
            print "Exercise was not saved on database."
            print "==================================="
            return

        # (0 owner_key, 1 txt_sections, 2 txt_summary, 3 txt_problem, 4 txt_answer, 5 txt_class)
        #row = {'owner_key': p[0], 'summary_text': p[2], 'problem_text': p[3], 'answer_text': p[4], 'class_text': p[5]}


        # -------------
        # Exercise ok?
        # -------------
        #TODO: what to do when latex or latex images have errors?
        #TODO: this is not good this way!
        if not self.is_exercise_ok(row,dest,silent=True):
            print "==================================="
            print "Exercise was not saved on database."
            print "==================================="
            return


        # ----------------------------
        # Exercise seems ok: store it.
        # ----------------------------
        #TODO: it should not be in database until a good instance is produced.
        inserted_row = self.megbook_store.insertchange(row)
        #Users don't like anoying messages: 
        #print "A problem is going to be generated with ekey=0"
        try:
            self.new(row['owner_key'], ekey=0)
        except e:
            print 'Problem name %s must be reviewed.' % inserted_row['owner_key']
            raise e


    def is_exercise_ok(self,row,dest,silent=True):
        r"""
        Check if exercise is ready for compilation and for python/sage errors.

        Developer note: derive this for other markups.
        """
        raise NotImplementedError


    def exercise_pythontest(self,row,start=0,many=5, edict=None,silent=False):
        r"""
        Test an exercise with random keys.

        INPUT:

         - ``row`` -- dictionary with class textual definitions.
         - ``start`` -- the parameteres will be generated for this random seed for start.
         - ``many`` -- how many keys to generate. 
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.

        OUTPUT:

            Printed message and True/False value.

        TODO: change this function name to exercise_test.
        """

        success = True

        
    
        #Testing for SyntaxErrors
        if not silent:
            print "Check '%s' for syntatical errors on Python code." % row['owner_key'] #TODO: add here a link to common syntatical error 

        try:
            #compiles and produces a class in memory (but no instance)
            exerciseclass(row)
            if not silent:
                print "    No syntatical errors found on Python code."
        except:
            success = False
        

        if success:

            #Testing for semantical errors
            if not silent:
                #print "Execute python class '%s' with %d different keys searching for semantical errors in the algorithm." % (row['owner_key'],many)
                print "Execute python class '%s' with %d different keys" % (row['owner_key'],many)

            try:

                for ekey in range(start,start+many):
                    if not silent:
                        print "    Testing for random key: ekey=",ekey
                    exerciseinstance(row,ekey=ekey,edict=edict)

            except: # Exception will be in memory.
                print "    Error on exercise '{0}' with parameters edict={1} and ekey={2}".format(row['owner_key'],edict,ekey)
                success = False #puxar para a frente
                #NOTES:
                #TODO: check http://docs.python.org/2/tutorial/errors.html 
                # ("One may also instantiate an exception first" ...)
                #TODO: remove this

            
        #Conclusion
        if not silent:
            if success:
                print "    No problems found in Python."
            else:
                print "    Please review the code '%s' based on the reported cases." % row['owner_key']

        return success




    def check_all(self,dest='.'):
        r""" 
        Check all exercises of this megbook for errrors.

        INPUT:

        OUTPUT:

            Printed message and True/False value.
        """

        all_ex = []
        for row in ExIter(self.megbook_store):
            if not self.is_exercise_ok(row,dest,silent=True):
                print "   Exercise '%s' have python/sage or compilation errors." % row['owner_key']
                all_ex.append(row['owner_key'])
        if all_ex:
            print "Review the following exercises:"
            for r in all_ex:
                print r
        else:
            print "No problem found."

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
        exlist = [row[1] for row in self.megbook_store.search(regex)] #row[0] is owner_key
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
        sname = 'Exercise name %s' % exrow['owner_key'].encode('utf8')
        print sname + '\n' + exrow['problem_text'].encode('utf8') + '\n'


    def remove(self,owner_keystring,dest='.'):
        r"""
        Removing an exercise from the database.

        INPUT:

        - ``owner_keystring`` -- the class name.
        """

        #Get the exercise
        row = self.megbook_store.get_classrow(owner_keystring)
        if row:            
            fname = os.path.join(dest,owner_keystring+'.txt')
            #store it on a text file
            f = open(fname,'w')
            f.write(row['summary_text'].encode('utf-8')) #includes %summary line
            f.write(row['problem_text'].encode('utf-8')) #includes %problem line
            f.write(row['answer_text'].encode('utf-8')) #includes %answer line
            f.write(row['class_text'].encode('utf-8'))
            f.close()
            print "Exercise '%s' stored on text file %s." % (owner_keystring,fname)

            #remove it
            self.megbook_store.remove_exercise(owner_keystring)
        else:
            print "Exercise %s is not on the database." % owner_keystring



    def new(self,owner_keystring, ekey=None, edict=None):
        r"""Prints an exercise instance of a given type

        INPUT:

         - ``owner_keystring`` -- the class name.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.

        OUTPUT:
            An instance of class named ``owner_keystring``.

        """
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(owner_keystring)
        if not row:
            print "%s cannot be accessed on database" % owner_keystring
            return None
        #Create and print the instance
        ex_instance = exerciseinstance(row, ekey, edict)
        self.print_instance(ex_instance)
        return None
        #return ex_instance #removed because makes too much "noise" in output



    def print_instance(self, ex_instance, show_output=False):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """
        #Derive this for other markups.

        summtxt =  ex_instance.summary()
        probtxt =  ex_instance.problem()
        answtxt =  ex_instance.answer()
        sname   =  ex_instance.name

        print '-'*len(sname)
        print sname 
        print '-'*len(sname)
        print summtxt.encode('utf8')
        print probtxt.encode('utf8')
        print answtxt.encode('utf8')


    def make_sws(self, dest='.'):
        sws = SWSExporter(self,dest)



#end class MegBookBase


