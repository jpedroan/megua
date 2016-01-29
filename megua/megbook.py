# -*- coding: utf-8 -*-

r"""
MegBook -- build your own database of exercises in several markup languages.

AUTHORS:

- Pedro Cruz (2012-06): initial version (based on megbook.py)
- Pedro Cruz (2016-01): first modifications for use in SMC.

"""

# Abstract function
# raise NotImplementedError( "Should have implemented this" )


#*****************************************************************************
#       Copyright (C) 2012,2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  
  
#megua configuration file: server side settings.
from mconfig import * 

#megua modules:
from localstore import LocalStore,ExIter
from ex import *
from parse_ex import parse_ex


#Because sage.plot.plot.EMBEDDED_MODE
#This variable indicates if notebook is present.
#Trying no include now the EMBEDDED_MODE and wait for some place else:
#from sage.all import * #REMOVE IS EVERYTHONG IS WORKING


#Python modules:
import sqlite3 #for row objects as result from localstore.py
import shutil
import os
import random

#import codecs

#Python Modules
import re
import codecs
import random as randomlib #random is imported as a funtion somewhere
import json
import httplib, urllib


#Megua modules:
from platex import pcompile
from xmoodle import MoodleExporter
from xsphinx import SphinxExporter
from xlatex import * #including PDFLaTeXExporter


# Jinja2 package
import jinja2
#from jinja2 import Environment, PackageLoader,FileSystemLoader,Template, TemplateNotFound
#Note on Jinja2:
# di = { 'ex_10_0_4': 10 }
# template.stream(di).dump('new.tex')
# print "Template folders are: " + str(env.loader.searchpath)


class MegBook:
    r"""
    A book of exercises of several markup languages.
    
    This module provides a means to produce a database of exercises 
    that can be seen as a book of some author or authors.

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
       >>> meg = MegBook(r'.testoutput/megbasedb.sqlite')


    Save a new or changed exercise::

       >>> ex=ExLaTeX(r'''
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
       ... ''')
       Each problem can have a suggestive name. 
       Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.
       <BLANKLINE>
       Testing python/sage class 'E28E28_pdirect_001' with 100 different keys.
           No problems found in this test.
          Compiling 'E28E28_pdirect_001' with pdflatex.
          No errors found during pdflatex compilation. Check E28E28_pdirect_001.log for details.
       >>> meg.save(ex,dest=r'.testoutput')
       Exercise name E28E28_pdirect_001 inserted.

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

    #TODO 1: increase docstring examples.

    #TODO 2: assure that there is a natlang folder in templates (otherwise put it in english). Warn for existing languages if specifies lan does not exist.


    def __init__(self,filename=None): 
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


        ExerciseBase.megbook = self


    def __str__(self):
        return "MegBook('%s','%s','%s')" % (self.local_store_filename)

    def __repr__(self):
        return "MegBook('%s','%s','%s')" % (self.local_store_filename)


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
            return "MegBook: missing template %s"%filename
        r = tmpl.render(**user_context)
        return r




    def save(self,uexercise):
        r"""
        Save an exercise defined on a `python string`_ using a specific sintax defined here_.

        INPUT::

        - ``uexercise`` -- an exercise textual description (unicode string).

        OUTPUT::
        
        - Textual messages with errors.

        DESCRIPTION:
        
        - An exercise textual description must be processed.

        """

        #First check: syntatic level ("megua" script)
        row =  parse_ex(to_unicode(exercise))

    
        #Second check: syntatic and runtime  ("python/sagemath" script)
        ex_instance = self.exerciseinstance(row)            
            
        #Third check: creating several instances; create content.
        ex_instance.check(maxtime=3) #3 seconds


        #After all that, save it on database:                        
        self.megbook_store.insertchange(row)
        
        #Check if saved.
        try:
            self.new(row["unique_name"], ekey=0, returninstance=True).print_instance()
        except e:
            print 'Problem name %s must be reviewed.' % row["unique_name"]
            raise e





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
                print "   Exercise '%s' have python/sage or compilation errors." % row['unique_name']
                all_ex.append(row['unique_name'])
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



    def new(self,unique_name, ekey=None, edict=None, returninstance=False):
        r"""Prints an exercise instance of a given type

        INPUT:

         - ``unique_name`` -- the class name.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.
         - ``returninstance`` -- if True, this function return a python object.

        OUTPUT:
            An instance of class named ``unique_namestring``.

        """
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(unique_namestring)
        if not row:
            print "%s cannot be accessed on database" % unique_namestring
            return
        
        #Create and print the instance
        ex_instance = self.exerciseinstance(row, ekey, edict)
        ex_instance.print_instance()
        
        if returninstance:
            return ex_instance

    


    def exerciseclass(self, row):
        r"""
        Interpret the `exercise class` (not an object) from text fields.
        """
    
        #Create the class (not yet the instance)
    
        #TODO:
        #   put class in globals(). 
        #   Now ex_name is on global space ?? 
        #   or is in this module space?
        # TODO: control the time and the process
    
        try:
            #exec compile(sage_class,row["unique_name"],'eval')
            #TODO: http://www.sagemath.org/doc/reference/misc/sage/misc/sage_eval.html
            # and spread this for more points in code.
            sage_class = preparse(row['class_text'])
            exec sage_class
        except: 
            tmp = tempfile.mkdtemp()
            pfilename = tmp+"/"+row["unique_name"]+".sage"
            pcode = open(pfilename,"w")
            pcode.write("# -*- coding: utf-8 -*\nfrom megua.all import *\n" + row['class_text'].encode("utf-8") )
            pcode.close()
            errfilename = "%s/err.log" % tmp
            os.system("sage -python %s 2> %s" % (pfilename,errfilename) )
            errfile = open(errfilename,"r")
            err_log = errfile.read()
            errfile.close()
            #TODO: adjust error line number by -2 lines HERE.
            #....
            #remove temp directory
            #print "=====> tmp = ",tmp
            os.system("rm -r %s" % tmp)
            print err_log #user will see errors on syntax.
            raise SyntaxError  #to warn user #TODO: not always SyntaxError
    
    
        #Get class name
        ex_class = eval(row['unique_name']) #String contents row['unique_name'] is now a valid identifier.
    
        #class fields
        ex_class._summary_text = row['summary_text']
        ex_class._problem_text = row['problem_text']
        ex_class._answer_text  = row['answer_text']
    
        return ex_class
    
        
    
    def exerciseinstance(self, row, ekey=None, edict=None):
        r"""
        Instantiates the `exercise class` (not an object) from text fields.
        Then, creates an instance using  `exercise_instance` routine.
    
        This function creates an instance of a class named in parameter unique_namestring. That class must be already defined in memory.
    
        INPUT:
    
         - ``unique_namestring`` -- the class name (python string).
         - ``ex_class`` -- a class definition in memory.
         - ``row``-- the sqlite row containing fields: 'summary_text', 'problem_text',  'answer_text'.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.
    
        OUTPUT:
            An instance of class named ``unique_namestring``.
    
        NOTES:
    
            http://docs.python.org/library/exceptions.html#exceptions.Exception
    
        # TODO: control the time and the process

        """
    
        #Create the class (not yet the instance). See exerciseclass definition above.
        ex_class = exerciseclass(row)
    
        #Create one instance of ex_class
        try:
            ex_instance = ex_class(row['unique_name'],ekey,edict)
        except: 
            tmp = tempfile.mkdtemp()
            pfilename = tmp+"/"+row["unique_name"]+".sage"
            pcode = open(pfilename,"w")
            pcode.write("# -*- coding: utf-8 -*\nfrom megua.all import *\n" + row['class_text'].encode("utf-8")+"\n")
            pcode.write(row['unique_name'] + "(ekey=" + str(ekey) + ", edict=" + str(edict) + ")\n")
            pcode.close()
            errfilename = "%s/err.log" % tmp
            os.system("sage %s 2> %s" % (pfilename,errfilename) )
            errfile = open(errfilename,"r")
            err_log = errfile.read()
            errfile.close()
            #TODO: adjust error line number by -2 lines HERE.
            #....
            #remove temp directory
            #print "=====> tmp = ",tmp
            os.system("rm -r %s" % tmp)
            print err_log
            raise Exception  #to warn user #TODO: not always SyntaxError
        
        return ex_instance
    
    
    
    
        
        
#end class MegBook
        
        
