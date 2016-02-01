# coding=utf-8

r"""
ExerciseBase - This module defines the base class for exercise templating.

To build a database of exercise templates read details of module ``megbook``.
 

AUTHORS:

- Pedro Cruz (2010-03-01): initial version
- Pedro Cruz (2011-05-06): redefining Exercise templating.
- Pedro Cruz (2011-08): documentation strings with tests
- Pedro Cruz (2016-01): refactoring for SMC.

INSPIRATION:

- https://github.com/sagemath/sage/blob/master/src/sage/structure/sage_object.pyx
- https://github.com/sagemath/sage/blob/master/src/sage/games/quantumino.py

Test examples using::

   sage -t exbase.py
   
   
   sage -python -m doctest exbase.py

"""


#*****************************************************************************
#       Copyright (C) 2011, 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#SAGEMATH modules
from sage.all import SageObject  

#MEGUA modules
from megua.parse_param import parameter_change
from megua.ur import ur

#PYTHON modules
import warnings


class ExerciseBase(SageObject):
    """Class ``ExerciseBase`` is the base class for an exercise.


    Derivations of this class will be specific Exercise Templates. A template of an exercise depends on numerical parameters. 
    The template is defined by a summary, a question and an answer text containing question parameters and solution parameters.
    The data paramters of the class define the dictionary that contains all parameters needed for substitution.

    The Exercise Template allows the following operations:
    * Return the dictionary of a specific exercise
    * Generate an exercise dictionary from a key
    * Generate an exercise dictionary from a given set of parameters
    * Give a textual (semi-latex) representation of the dictionary (question and full, non pedagogical, answer).
    * Give a textual description of the template.
    
    EXAMPLES:
    
    Test examples using::
    
        
        sage -t exbase.py

        .. old: sage -python -m doctest exbase.py
    
    Defining a new exercise template::

       sage: from megua.exbase import *
       sage: class AddingTwoIntegers(ExerciseBase):
       ....:     #class variables   
       ....:     _unique_name  = "AddingTwoIntegers"
       ....:     _summary_text = "Adding two integers."
       ....:     _problem_text = "Calculate a1 + a2@()."
       ....:     _answer_text  = "Result is a1 + a2@() = r1."
       ....:
       ....:     def make_random(self,edict):
       ....:        self.a1 = ZZ.random_element(-10,10+1)
       ....:        self.a2 = ZZ.random_element(-10,10+1)
       ....:        if edict:
       ....:            self.update_dict(edict)
       ....:        self.r1 = self.a1 + self.a2 
       sage: adding_template = AddingTwoIntegers(ekey=10)
       sage: print adding_template.summary()
       Adding two integers.
       sage: print adding_template.problem()
       Calculate -4 + 1.
       sage: print adding_template.answer()
       Result is -4 + 1 = -3.
       sage: print adding_template.unique_name()
       AddingTwoIntegers
    
    
    Changing randomly the set of parameters::
    
       sage: adding_template.update(ekey=15) #another set of random parameters
       sage: print adding_template.problem()
       Calculate 2 + 10.
       sage: print adding_template.answer()
       Result is 2 + 10 = 12.
       
    Changing randomly but setting one of them::
        
       sage: adding_template.update(ekey=15,edict={'a1':99}) #another set of random parameters
       sage: print adding_template.problem()
       Calculate 99 + 10.
       sage: print adding_template.answer()
       Result is 99 + 10 = 109.
    
       sage: adding_template.update(ekey=15,edict={'a2':-5}) #another set of random parameters
       sage: print adding_template.problem()
       Calculate 2 + (-5).
       sage: print adding_template.answer()
       Result is 2 + (-5) = -3.

    """


    # =======================
    # The following variables 
    #      ARE PART OF THE CLASS,
    # they receive values before instance is created.
    # - a derivation of class ``ExerciseBase`` will inherit the values below.
    # - a derivation of class ``ExerciseBase`` should change this class parameters to new ones.


    # This is set in MegBook
    _megbook = None 

    # This are set in MegBook
    # by MegBook.exerciseclass() and 
    #   MegBook.exerciseinstance()
    _unique_name = None
    _summary_text = None
    _problem_text = None
    _answer_text  = None


    def __init__(self,ekey=None, edict=None):

        self.has_instance = False
        self.current_problem = None
        self.current_answer = None
        
        if ekey or edict:
            self.update(ekey,edict)

    def __str__(self):
        return "%s(%s)" % (self._unique_name,str(self.__dict__))



    def _repr_(self): 
        return "%s(%s)" % (self._unique_name,repr(self.__dict__))


    def update(self,ekey=None,edict=None):
        #Initialize all random generators.    
        self.ekey = ur.set_seed(ekey)


        #Call user derived function to generate a set of random variables.
        self.make_random(edict)

        #Call user derived function to solve it.
        #TODO: warn that this is not to be used again
        self.solve()

        self.has_instance = True


    def update_dict(self,edict):
        #make_random() can call this.
        #in another way.
        #Change all or some parameters existing in pdict.     
        if edict is not None:
            self.__dict__.update(edict) 



    def make_random(self,edict=None):
        """
        Derive this function and change behaviour.
        """    
        update_dict(edict)


    def solve(self):
        """
        Derive this function.
        """    
        warnings.warn("def solve() is deprecated. Use only def make_random(edict) and configure ", DeprecationWarning) 
        pass

    def rewrite(self,text):
        """
        Derive this function and implement rewritting rules to change latex expressions for example.
        
        Example::

           exp_pattern = re.compile(ur'e\^\{\\left\((.+?)\\right\)\}',re.U)
           out_text = re.sub(exp_pattern, r'e^{\1}', text)

        """
        return text


    def check(self):
        #TODO: test several keys for maxtime.
        #1. test code several times
        #2. test compilations, for example
        pass

 
    def unique_name(self):
        return self._unique_name


   
    def summary(self):
        """#, edict=" + str(edict) + ")\n")
        Use class text self._summary_text and replace for parameters on dictionary. Nothing is saved.
        #TODO: maybe summary does not need replacements!
        """
        #return parameter_change(self._summary_text,self.__dict__)
        return self._summary_text


    def problem(self):
        """
        Use class text self._problem_text and replace for parameters on dictionary. 
        Nothing is saved.

        If removemultitag=true, the tags <multiplechoice> ... </multiplechoice> are removed.
        """
        
        assert(self.has_instance)
            
        self.current_problem = parameter_change(self._problem_text,self.__dict__,latex_filter=False)
        
        return self.current_problem

    def answer(self):
        """
        Use class text self._answer_text and replace for parameters on dictionary. 
        Nothing is saved.

        If removemultitag=true, the tags <multiplechoice> ... </multiplechoice> are removed.
        """

        assert(self.has_instance)

        self.current_answer = parameter_change(self._answer_text,self.__dict__,latex_filter=False)
        
        return self.current_answer

    def print_instance(self):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """
        #Derive this for other markups.

        summtxt =  self.summary()
        probtxt =  self.problem()
        answtxt =  self.answer()
        uname   =  self.unique_name()

        print '-'*len(uname)
        print uname 
        print '-'*len(uname)
        print summtxt.encode('utf8')
        print probtxt.encode('utf8')
        print answtxt.encode('utf8')



    
#end of exbase.py
    