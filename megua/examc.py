# coding=utf-8

r"""
examc -- an exercise in LaTeX for use in AMC.



AUTHORS:

- Pedro Cruz (2016-03): first modifications for use in SMC.


EXAMPLES

::
  
    sage -t exlatex.py

Creation a LaTeX exercise:

::
        
       sage: from megua.all import *
       sage: meg = MegBook(r'_input/megbook.sqlite') 
       sage: meg.save(r'''
       ....: %Summary Primitives
       ....: Here one can write few words, keywords about the exercise.
       ....: For example, the subject, MSC code, and so on.
       ....:   
       ....: %Problem Primitive
       ....: Determine the primitive of 
       ....: \[
       ....:    ap x + bp@()
       ....: \]
       ....:  
       ....: %Answer
       ....: The answer is $prim1+C$, with C a real number.
       ....:  
       ....: class E28E28_pdirect_001(ExAMC):
       ....:  
       ....:     def make_random(self):
       ....:         # make a problem instance
       ....:         self.ap = ZZ.random_element(-4,4)
       ....:         self.bp = ur.iunif_nonset(-4,4,[0])
       ....:         # solving
       ....:         x=SR.var('x')
       ....:         self.prim1 = latex(integrate(self.ap * x + self.bp,x))
       ....: ''')
       exlatex module: open pdf file _output/E28E28_pdirect_001/E28E28_pdirect_001.pdf

"""


#*****************************************************************************
#       Copyright (C) 2011,2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#PYTHON modules
import re
import os
import subprocess


#MEGUA modules
from megua.platex import pcompile
from megua.exbase import ExerciseBase
from megua.jinjatemplates import templates
from megua.mconfig import MEGUA_PLATFORM


class ExAMC(ExerciseBase):
   

    def _latex_string(self):

        latex_string = templates.render("exlatex_print_instance.tex",
            sname=self.unique_name(),
            summtxt=self.summary(),
            probtxt=self.problem(),
            answtxt=self.answer(),
            ekey = self.ekey,
         )

        return latex_string         



    def print_instance(self):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        #Use jinja2 template to generate LaTeX.
        latex_string = self._latex_string()
        
        try:
            pcompile(latex_string,self.working_dir,self.unique_name(),hideoutput=True)
        except subprocess.CalledProcessError as err:
            #Try to show the message to user
            #print "Error:",err
            #print "returncode:",err.returncode
            #print "output:",err.output
            print "================"
            latex_error_pattern = re.compile(r"!.*?l\.\d+(.*?)$",re.DOTALL|re.M)
            match = latex_error_pattern.search(err.output) #create an iterator
            if match:
                print match.group(0)
            else:
                print "There was a problem with an latex file."
            print "You can download %s.tex and use your windows LaTeX editor to help find the error." % self.unique_name() 
            print "================"
            raise

        if MEGUA_PLATFORM=='sagews':
            fullpath = os.path.join(self.working_dir, 'utf8-'+self.unique_name()+'.tex')
            salvus.file(fullpath)
            fullpath = os.path.join(self.working_dir, self.unique_name()+'.tex')
            salvus.file(fullpath)
            fullpath = os.path.join(self.working_dir, self.unique_name()+'.pdf')
            salvus.file(fullpath)
        else: #MEGUA_PLATFORM=='commandline'
            fullpath = os.path.join(self.working_dir, self.unique_name()+'.pdf')
            print "exlatex module: open pdf file",fullpath


