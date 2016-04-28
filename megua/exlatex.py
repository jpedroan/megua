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
from os import environ
import subprocess


#MEGUA modules
from megua.platex import pcompile
from megua.exbase import ExerciseBase
from megua.jinjatemplates import templates
#tirar? from megua.mconfig import MEGUA_PLATFORM


class ExLatex(ExerciseBase):



    def _latex_string(self):

        lts = templates.render("exlatex_print_instance.tex",
            sname=self.unique_name(),
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

        EXERCISE_TEX_PATHNAME = os.path.join(self.working_dir, self.unique_name()+'.tex')
        EXERCISE_PDF_PATHNAME = os.path.join(self.working_dir, self.unique_name()+'.pdf')

        try:
            pcompile(latex_string,self.working_dir,self.unique_name(),hideoutput=True)
        except subprocess.CalledProcessError as err:
            print "Start ExLatex.print_instance() error message:"
            #Try to show the message to user
            #print "Error:",err
            #print "returncode:",err.returncode
            #print "output:",err.output
            #print "================"
            latex_error_pattern = re.compile(r"!.*?l\.\d+(.*?)$",re.DOTALL|re.M)
            match = latex_error_pattern.search(err.output) #create an iterator
            if match:
                print match.group(0)
            else:
                print "There was a problem with an latex file."

            print "You can download %s and use your windows LaTeX "\
                  "editor to help find the error." % EXERCISE_TEX_PATHNAME
            print "End ExLatex.print_instance()."
            raise

        if environ["MEGUA_PLATFORM"]=='SMC':
            if environ["MEGUA_BASH_CALL"]=='on': #see megua bash script at megua/megua
                print "Exlatex module say:  open ", EXERCISE_PDF_PATHNAME
                #dows not work: subprocess.Popen(["open",EXERCISE_PDF_PATHNAME])
                sys.path.append('/usr/local/lib/python2.7/dist-packages')
                from smc_pyutil import smc_open
                smc_open.process([EXERCISE_PDF_PATHNAME])
            else: #sagews SALVUS
                from smc_sagews.sage_salvus import salvus
                #Windows latin1 tex
                forwindows_fullpath = os.path.join(self.working_dir, 'windows-'+self.unique_name()+'.tex')
                salvus.file(forwindows_fullpath,show=True,raw=True); print ""
                #utf-8 tex
                salvus.file(EXERCISE_TEX_PATHNAME,show=True,raw=True); print ""
                #pdf file
                salvus.file(EXERCISE_PDF_PATHNAME,show=True,raw=True); print ""
                #salvus.pdf(fullpath)
                salvus.open_tab(EXERCISE_PDF_PATHNAME)
        elif environ["MEGUA_PLATFORM"]=='DESKTOP':
            print "Exlatex module say: evince ",EXERCISE_PDF_PATHNAME
            subprocess.Popen(["evince",EXERCISE_PDF_PATHNAME])
        else:
            print """Exlatex module say: environ["MEGUA_PLATFORM"] must be properly configured at $HOME/.megua/mconfig.sh"""

