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

SUMMARY:

- `make_random` receives `edict`: allow the author to control attributes.



EXAMPLES:


Test examples using:

::

    sage -t exbase.py
   
Defining a new exercise template:

::

       sage: from megua.exbase import *
       sage: class AddingTwoIntegers(ExerciseBase):
       ....:     #class variables   
       ....:     _unique_name  = "AddingTwoIntegers"
       ....:     _suggestive_name = "Adding Two Integers"
       ....:     _summary_text = "Adding two integers."
       ....:     _problem_text = "Calculate a1 + a2@()."
       ....:     _answer_text  = "Result is a1 + a2@() = r1."
       ....:     def make_random(self,edict=None):
       ....:         self.a1 = ZZ.random_element(-10,10+1)
       ....:         self.a2 = ZZ.random_element(-10,10+1)
       ....:         if edict:
       ....:            self.update_dict(edict)
       ....:         self.r1 = self.a1 + self.a2 
       sage: adding_template = AddingTwoIntegers(ekey=10)
       sage: print adding_template.summary()
       Adding two integers.
       sage: print adding_template.problem()
       Calculate -4 + 1.
       sage: print adding_template.answer()
       Result is -4 + 1 = -3.
       sage: print adding_template.unique_name()
       AddingTwoIntegers
    
    
Changing, randomly, the set of parameters:
    
::

       sage: adding_template.update(ekey=15) #another set of random parameters
       sage: print adding_template.problem()
       Calculate 2 + 10.
       sage: print adding_template.answer()
       Result is 2 + 10 = 12.

Changing randomly but setting one of them:

::

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

Call "old megua" solve(self) method, if exists:

::

       sage: class CallSolveTest(ExerciseBase):
       ....:     #class variables   
       ....:     _unique_name  = "AddingTwoIntegers"
       ....:     _suggestive_name = "Adding Two Integers"
       ....:     _summary_text = "Adding two integers."
       ....:     _problem_text = "Calculate a1 + a2@()."
       ....:     _answer_text  = "Result is a1 + a2@() = r1."
       ....:
       ....:     def make_random(self):
       ....:        self.a1 = ZZ.random_element(-10,10+1)
       ....:        self.a2 = ZZ.random_element(-10,10+1)
       ....:     def solve(self): #old megua uses def solve()
       ....:        self.r1 = self.a1 + self.a2 
       sage: adding_template = CallSolveTest(ekey=10)
       sage: print adding_template.answer()
       Result is -4 + 1 = -3.

Make a static, ie, non parameterized exercise:

::

       sage: class StaticExercise(ExerciseBase):
       ....:     #class variables   
       ....:     _unique_name  = "StaticExercise"
       ....:     _suggestive_name = "Adding Two Integers"
       ....:     _summary_text = "Adding two integers."
       ....:     _problem_text = "Calculate 10 + 20."
       ....:     _answer_text  = "Result is 30."
       ....:     # No make_random in this exercise.
       sage: adding_template = StaticExercise()
       sage: print adding_template.answer()
       Result is 30.



"""


#*****************************************************************************
#       Copyright (C) 2011, 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#PYTHON modules
import warnings
#warnings.filterwarnings("error")
import re
import os
#remove: from os import environ

#SAGEMATH modules
from sage.all import SageObject 

try:
    #new sagemath (don't know version)
    from cysignals.alarm import AlarmInterrupt, alarm, cancel_alarm
except ImportError:
    #old sagemath (don't know version)
    from sage.ext.interrupt.interrupt import AlarmInterrupt
    from sage.misc.misc import alarm, cancel_alarm
    

#MEGUA modules
from megua.parse_param import parameter_change
from megua.ur import ur
from megua.ug import UnifiedGraphics
from megua.tounicode import to_unicode
from megua.megoptions import *




class ExerciseBase(SageObject,UnifiedGraphics):
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

    """


    # =======================
    # The following variables 
    #      ARE PART OF THE CLASS,
    # they receive values before instance is created.
    # - a derivation of class ``ExerciseBase`` will inherit the values below.
    # - a derivation of class ``ExerciseBase`` should change this class parameters to new ones.

    #All of the folowing variables must be set before __init__
    #They are set in MegBook.save()

    # This is set in MegBook
    _megbook = None

    # This are set in MegBook
    # by MegBook.exerciseclass() and 
    #   MegBook.exerciseinstance()
    #TODO: change _text to _source in all megua modules.
    _unique_name = None
    _summary_text = None
    _problem_text = None
    _answer_text  = None
    _suggestive_name = None


    def __init__(self,ekey=None, edict=None):

        #Considered part of the class definition and not the instance.
        #TODO: should author write each filed ? Can he leave empty fields?
        #TODO: assert or exit() ?
        if not self._unique_name:
            print("exbase.py: exercise should have a 'unique_name' stated in the class part.")
            #assert(self._unique_name)
            exit()
        if not self._summary_text:
            print("exbase.py: exercise '%s' should have a '%%summary' tag and text in it should not be empty." % self._unique_name)
            #assert(self._summary_text)
            exit()
        if not self._problem_text:
            print("exbase.py: exercise '%s' should have a '%%problem' tag and text in it should not be empty." % self._unique_name)
            #assert(self._problem_text)
            exit()
        if not self._answer_text:
            print("exbase.py: exercise '%s' should have an '%%answer' tag and text in it should not be empty." % self._unique_name)
            #assert(self._answer_text)
            exit()

        self.wd_relative = os.path.join(MEGUA_WORKDIR,self._unique_name)
        self.wd_fullpath = os.path.join(MEGUA_WORKDIR_FULLPATH,self._unique_name)

        UnifiedGraphics.__init__(self)

        self.has_instance = False
        self._current_problem = None
        self._current_answer = None
        self.update_timed(ekey,edict)


    def __str__(self):
        return "%s(edict=%s)" % (self._unique_name,str(self.__dict__))



    def _repr_(self): 
        return "%s(edict=%s)" % (self._unique_name,repr(self.__dict__))


    def update_timed(self,ekey=None,edict=None, render_method=None):
        r"""calls ex.update() but controls execution time.
        """
        self.has_instance = False

        #Check if class fields are in str or unicode
        self._summary_text    = to_unicode(self._summary_text)
        self._problem_text    = to_unicode(self._problem_text)
        self._answer_text     = to_unicode(self._answer_text)
        self._suggestive_name = to_unicode(self._suggestive_name)


        try:

            #Keep author in control of max time in megbook.

            #alarm: see import at top lines. 
            if not self._megbook:
                alarm(60)
            else:
                alarm(self._megbook.max_computation_time)

            self.update(ekey,edict,render_method)

        except AlarmInterrupt:
            print('Exercise "%s" is taking too long to make!' % self.unique_name())
            print('Check make_random() routine or increase meg.max_computation_time.')
            # if the computation finished early, though, the alarm is still ticking!
            # so let's turn it off below.
            raise AlarmInterrupt

        #Turn off alarm because make has been done in time.
        #cancel_alarm is from sage.misc.misc
        cancel_alarm()


    def update(self,ekey=None,edict=None, render_method=None):
        r"""Does this:
        - set random seed in module `ur`
        - initialize this exercise local variables
        - call make_random passing `edict` for author control

        It could be derive for other exercise base.

        DEVELOPER NOTES:

        - http://stackoverflow.com/questions/5268404/what-is-the-fastest-way-to-check-if-a-class-has-a-function-defined

        """

        #For debug:
        print(self.unique_name())

        #TODO: is this flag is being used ?
        self.has_instance = False

        #Each update produce a new set of filenames for images.
        #See ug.py
        #To avoid duplicated image names is used a set():
        self.image_relativepathnames = set()
        self.image_fullpathnames = set()

        #Graphics
        if render_method:
            self.render_method(render_method)

        #Initialize all random generators.
        self.ekey = ur.start_at(ekey) #get new if ekey=None

        #Call user derived function to generate a set of random variables.
        #See developer notes.
        make_random = getattr(self, "make_random", None)
        if callable(make_random):
            try:
                make_random(edict) #calls self.make_random(edict)
            except TypeError:
                make_random() #calls old self.make_random(), no args

        #        self.make_random(edict)

        #Call user derived function to solve it.
        #TODO: warn that this is not to be used again
        #self.solve()
        solve = getattr(self, "solve", None)
        if callable(solve):
            warnings.warn("exbase.py: 'def solve()' is deprecated. Use only 'def make_random(self,edict)' and configure ", DeprecationWarning) 
            self.solve()

        #create current problem and answer
        self._current_problem = self.search_replace(self._problem_text)
        self._current_answer = self.search_replace(self._answer_text)

        
        self.has_instance = True



    def update_dict(self,edict=None):
        """
        - make_random() can call this if author decides.
        - update the state of the exercise by changing all 
          or some parameters existing in edict.
        """
        if edict:
            self.__dict__.update(edict)



    def make_random(self,edict=None):
        """
        Derive this function and change behaviour.
        """    
        #The author of an exercise must program make_random.
        #The following instruction is optional and user can call it 
        #only when his algorithm decides.
        self.update_dict(edict)


    #See above: "def update()" method.
    #def solve(self):
    #    """
    #    Derive this function.
    #    """    
    #    warnings.warn("exbase.py: 'def solve()' is deprecated. Use only 'def make_random(self,edict)' and configure ", DeprecationWarning) 


    def rewrite(self,text):
        """
        Derive this function and implement rewritting rules to change latex expressions for example.

        Example::

           exp_pattern = re.compile(ur'e\^\{\\left\((.+?)\\right\)\}',re.U)
           out_text = re.sub(exp_pattern, r'e^{\1}', text)

        """
        return text


    def try_random_updates(self,maxiter=None):
        r"""This method is called by megbook.save() before
        an exercise is saved into database.
        """
        print("Trying several ekeys ...")

        start = 0 #TODO: choose a random start

        if not maxiter:
            maxiter = self._megbook.max_tried_instances

        for ekey in range(start,start+maxiter):
            print("    Testing for random key: ekey=",ekey)
            self.update_timed(ekey=ekey)


    def get_ekey(self):
        return self.ekey

    def unique_name(self):
        assert(self._unique_name)
        return self._unique_name


    def summary(self):
        assert(self._summary_text)
        return self._summary_text


    def problem(self):
        assert(self.has_instance)
        assert(self._current_problem)
        return self._current_problem


    def answer(self):
        assert(self.has_instance)
        assert(self._current_answer)
        return self._current_answer


    def suggestive_name(self):
        assert(self.has_instance)
        if self._suggestive_name:
            return self._suggestive_name #could be none or ""
        else:
            return u""


    def search_replace(self,text_source):
        """Change this routine in derivations"""
        text1 = parameter_change(text_source,self.__dict__)
        text2 = self.rewrite(text1)
        if text2 is None: 
            raise NameError('rewrite(s,text) function is not working.')

        #TODO: check if this is ok here
        text3 = self.show_one(text2)

        return text3


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

        print('-'*13 + '-'*len(uname))
        print("Instance of:", uname) 
        print('-'*13 + '-'*len(uname))
        print("==> Summary:")
        print(summtxt) #.encode('utf8')
        print("==> Problem instance")
        print(probtxt) #.encode('utf8')
        print("==> Answer instance")
        print(answtxt) #.encode('utf8')

    def show_one(self,input_text):
        """Find all <showone value>...</showone> tags and select proper <thisone>...</thisone>
        Change it in the original text leaving only the selected ... in <thisone>...</thisone>
        """

        showone_pattern = re.compile(r'<\s*showone\s+(\d+)\s*>(.+?)<\s*/showone\s*>', re.DOTALL|re.UNICODE)

        #Cycle through all <showone> tags
        match_iter = re.finditer(showone_pattern,input_text)#create an iterator
        new_text = ''
        last_pos = 0

        for match in match_iter:

            #Get list of possibilities
            #print "===>",match.group(2)
            possibilities = self._showone_possibilities(match.group(2))

            #Get selected possibility
            #TODO: check range and if group(1) is a number.
            pnum = int(match.group(1))
            #print "===>",pnum

            #Text to be written on the place of all options
            possibility_text = possibilities[pnum]

            #new_text = new_text[:match.start()] + possibility_text + new_text[match.end():] 
            new_text += input_text[last_pos:match.start()] + possibility_text
            last_pos = match.end()

        new_text += input_text[last_pos:]

        return new_text


    def _showone_possibilities(self,text_with_options):
        """Find all tags <thisone>...</thisone> and make a list with all `...`
        """

        thisone_pattern = re.compile(r'<\s*thisone.*?>(.+?)<\s*/thisone\s*>', re.DOTALL|re.UNICODE)

        #Cycle through all <showone> tags
        match_iter = re.finditer(thisone_pattern,text_with_options)#create an iterator
        options = []
        for match in match_iter:
            options.append( match.group(1) )

        return options

    
#end of exbase.py
    
