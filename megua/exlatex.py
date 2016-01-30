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

  
from exbase import *

#Import the random generator object.
from ur import ur 
from cr import r_stem


class ExLaTeX(ExerciseBase):
    
    r"""

    .. test with: sage -python -m doctest exlatex.py


    Creation a LaTeX exercise::
        
       >>> meg.save(r'''
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
       ... class E28E28_pdirect_001(ExLaTeX):
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

     def update(self,ekey=None,edict=None):
        #reset image list for the new parameters
        #TODO: this can generate inconsistency if make_random or solve are called alone.
        self.image_list = []

        #Case when exercise is multiplechoice
        self.all_choices = []
        self.has_multiplechoicetag = None #Don't know yet.
        self.detailed_answer= None

        #Initialize all random generators.
        self.ekey = ur.set_seed(ekey)

        #Call user derived function to generate a set of random variables.
        self.make_random(edict)

        #Call user derived function to solve it.
        #TODO: warn that this is not to be used again
        self.solve()

        self.has_instance = True

    def problem(self,removemultitag=False):
        """
        Use class text self._problem_text and replace for parameters on dictionary. 
        Nothing is saved.

        If removemultitag=true, the tags <multiplechoice> ... </multiplechoice> are removed.
        """
        
        assert(self.has_instance)
            
        if removemultitag:
            text1 = self.remove_multiplechoicetag(self._problem_text)
        else:
            text1 = self._problem_text
        text2 = parameter_change(text1,self.__dict__)
        self.current_problem = self._change_text(text2)
        
        return self.current_problem
    def answer(self,removemultitag=False):
        """
        Use class text self._answer_text and replace for parameters on dictionary. 
        Nothing is saved.

        If removemultitag=true, the tags <multiplechoice> ... </multiplechoice> are removed.
        """

        assert(self.has_instance)

        if removemultitag:
            text1 = self.remove_multiplechoicetag(self._answer_text)
        else:
            text1 = self._answer_text
        text2 = parameter_change(text1,self.__dict__)
        
        self.current_answer = self._change_text(text2)

        return self.current_answer


    def change_text(self,text1):
        """Called after parameter_change call. See above."""
        text2 = self.rewrite(text1)
        if text2 is None:
            raise NameError('rewrite(s,text) function is not working.')
        text3 = self.latex_images(text2)
        text4 = self.show_one(text3)
        text5 = self.old_html(text4)
        self.multiplechoice_parser(text5)  #extract information but don't change text
        return text5




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

        
    def check(self):
        r"""
        Check if exercise is well written before saving it to the database.

        #TODO: what to do when latex or latex images have errors?
        #TODO: this is not good this way!

        #TODO: control the time and the process where it runs.

        """

        # --------------------------------
        # Testing the new python class for 
        # programming errors:
        #     syntax and few instances execution. 
        # -------------------------------
        assert(ExerciseBase.check(self))


        # --------------------------
        # Testing latex compilation.
        # --------------------------


        #Use jinja2 template to generate LaTeX.
        latex_string = Exercise.megbook.template("print_instance_latex.tex",
            sname=ex_instance.name,
            summtxt=ex_instance.summary(),
            probtxt=ex_instance.problem(),
            answtxt=ex_instance.answer(),
            ekey = ex_instance.ekey,
        )

        if not ExLaTeX.silent_compilation:
            print "Compiling '%s' with pdflatex." % self.row['unique_name']

        #TODO: put this in other place
        latex_error_pattern = re.compile(r"!.*?l\.\d+(.*?)$",re.DOTALL|re.M)

        try:
            pcompile(latex_string,dest,self.row['unique_name'])
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




    def print_instance(self):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        #Use jinja2 template to generate LaTeX.
        latex_string = Exercise.megbook.template(
            "print_instance_latex.tex",
            uname=self.unique_name(),
            summtxt=self.summary(),
            probtxt=self.problem(),
            answtxt=self.answer(),
            ekey=self.ekey)

        #Produce PDF file from LaTeX.
        pcompile(latex_string,'.',self.unique_name(), hideoutput=True)

