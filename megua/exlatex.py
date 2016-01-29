# -*- coding: utf-8 -*-

r"""
exlatex -- an exercise in LaTeX.

AUTHORS:

- Pedro Cruz (2016-01): first modifications for use in SMC.

"""

# Abstract function
# raise NotImplementedError( "Should have implemented this" )


#*****************************************************************************
#       Copyright (C) 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

  
from ex import *


class ExLaTeX(ExerciseCreator):
    
    r"""

    .. test with: sage -python -m doctest exlatex.py


    Creation a LaTeX exercise::
        
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
    """
          

    silent_compilation = True
    silent_python_test = True
    destination_folder = '.'      
    autosave = True
          
    def __init__(self,exercisestr):
        r"""
        
        INPUTS::

        .. _python string: http://docs.python.org/release/2.6.7/tutorial/introduction.html#strings
        
        """
                
        if type(exercisestr)==str:
            exercisestr = unicode(exercisestr,'utf-8')


        # ---------------------------------------
        # Check exercise syntax: 
        #    summary, problem, answer and class.
        # MegBook will use this row to save things in LocalStore
        # row variable components are:
        #   (0 owner_key, 1 txt_sections, 2 txt_summary, 3 txt_problem, 4 txt_answer, 5 txt_class)
        # row = {'owner_key': p[0], 'summary_text': p[2], 'problem_text': p[3], 'answer_text': p[4], 'class_text': p[5]}
        # ---------------------------------------
        self.row = exerc_parse(exercisestr)
        if not self.row:
            print "==================================="
            print "Exercise syntax has errors."
            print "==================================="
            return


        # -------------
        # Exercise ok?
        # -------------
        self.ex_instance = create_check_exercise()

        
        if self.autosave:
            Exercise.megbook.save(self.row)
            


    def _latex_string(self):

        %TODO: criar

        latex_string = Exercise.megbook.template("print_instance_latex.tex",
            sname=ex_instance.name,
            summtxt=ex_instance.summary(),
            probtxt=ex_instance.problem(),
            answtxt=ex_instance.answer(),
            ekey = ex_instance.ekey,
        )

        return latex_string         

        
    def create_check_exercise(self):
        r"""
        Check if exercise is well written before saving it to the database.

        #TODO: what to do when latex or latex images have errors?
        #TODO: this is not good this way!

        """

        # --------------------------------
        # Testing the new python class for 
        # programming errors:
        #     syntax and few instances execution. 
        # -------------------------------
        if not exercise_pythontest(self.row,silent=ExLaTeX.silent_python_test):
            return


        # --------------------------
        # Testing latex compilation.
        # --------------------------

        #create an instance
        ex_instance = exerciseinstance(self.row)

        #Use jinja2 template to generate LaTeX.
        latex_string = Exercise.megbook.template("print_instance_latex.tex",
            sname=ex_instance.name,
            summtxt=ex_instance.summary(),
            probtxt=ex_instance.problem(),
            answtxt=ex_instance.answer(),
            ekey = ex_instance.ekey,
        )

        if not ExLaTeX.silent_compilation:
            print "Compiling '%s' with pdflatex." % self.row['owner_key']

        #TODO: put this in other place
        latex_error_pattern = re.compile(r"!.*?l\.\d+(.*?)$",re.DOTALL|re.M)

        try:
            pcompile(latex_string,dest,self.row['owner_key'])
        except subprocess.CalledProcessError as err:
            #Try to show the message to user
            #print "Error:",err
            #print "returncode:",err.returncode
            #print "output:",err.output
            print "================"
            match = latex_error_pattern.search(err.output) #create an iterator
            if match:
                print match.group(0)
            else:
                print "There was a problem with an latex file."
            print "You can download %s.tex and use your windows LaTeX editor to help find the error." % self.name 
            print "================"
            return None

        return ex_instance



    def print_instance(self):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        #Use jinja2 template to generate LaTeX.
        latex_string = Exercise.megbook.template(
            "print_instance_latex.tex",
            sname=self.ex_instance.name,
            summtxt=self.ex_instance.summary(),
            probtxt=self.ex_instance.problem(),
            answtxt=self.ex_instance.answer(),
            ekey=self.ekey)

        #Produce PDF file from LaTeX.
        pcompile(latex_string,'.',sname, hideoutput=True)

