# -*- coding: utf-8 -*-

r"""
exlatex -- an exercise in LaTeX.

Implements parameterized exercises in LaTeX


AUTHORS:

- Pedro Cruz (2016-01): first modifications for use in SMC.


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
       ....: class E28E28_pdirect_001(ExLatex):
       ....:  
       ....:     def make_random(self):
       ....:         # make a problem instance
       ....:         self.ap = ZZ.random_element(-4,4)
       ....:         self.bp = ur.iunif_nonset(-4,4,[0])
       ....:         # solving
       ....:         x=SR.var('x')
       ....:         self.prim1 = latex(integrate(self.ap * x + self.bp,x))
       ....: ''')
       Exlatex module say: evince  _output/E28E28_pdirect_001/E28E28_pdirect_001.pdf
       
"""


#*****************************************************************************
#       Copyright (C) 2011,2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#PYTHON modules
import sys
import re
import os
from os import environ
import subprocess


#MEGUA modules
from megua.platex import pcompile
from megua.exbase import ExerciseBase
from megua.jinjatemplates import templates
from megua.megoptions import *

class ExLatex(ExerciseBase):

    #def __init__(self,ekey=None, edict=None):
    #    ExerciseBase.__init__(self,ekey, edict)


    def conf_print_instance(self):
        print("ExLaTeX module say: MEGUA_PLATFORM must be properly configured at $HOME/.megua/conf.py")

    def _latex_string(self):

        lts = templates.render("exlatex_print_instance.tex",
            unique_name=self.unique_name(),
            ekey = self.ekey,
            summtxt=self.summary(),
            probtxt=self.problem(),
            answtxt=self.answer()
         )

        return lts



    def print_instance(self):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        #Use jinja2 template to generate LaTeX.
        latex_string = self._latex_string()

        pcompile(latex_string,self.wd_fullpath,self.unique_name())

        EXERCISE_TEX_PATHNAME = os.path.join(self.wd_fullpath, self.unique_name()+'.tex')
        EXERCISE_PDF_PATHNAME = os.path.join(self.wd_fullpath, self.unique_name()+'.pdf')

        self.conf_print_instace()

