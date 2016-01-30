r"""
This module defines the base class for exercise templating.

To build a database of exercise templates read details of module ``megbook``.
 

AUTHORS:

- Pedro Cruz (2010-03-01): initial version
- Pedro Cruz (2011-05-06): redefining Exercise templating.
- Pedro Cruz (2011-08): documentation strings with tests


EXAMPLES:

This examples can be tested using ``sage -python -m doctest ex.py`` or ``sage -t ex.py``.

Defining a new exercise template::

   >>> from ur import * 
   >>> from ex import Exercise
   >>> class AddingTwoIntegers(Exercise):
   ...     def make_random(self):
   ...         self.a = ZZ.random_element(-10,11)
   ...         self.b = ZZ.random_element(-10,11)
   ...     def solve(self):
   ...         self.c = self.a + self.b 

Create an instance::

   >>> adding_template = AddingTwoIntegers(name="adding_integers",ekey=10,edict=None,summary="Adding Integers",problem="Calculate $ a + b = res?$",answer="Result is: $res=c$")
   >>> print adding_template
   {'a': -4, 'c': -3, 'b': 1, '_summary_text': 'Adding Integers', 'name': 'adding_integers', 'ekey': 10, '_answer_text': 'Result is: $res=c$', '_problem_text': 'Calculate $ a + b = res?$'}
   >>> print adding_template.summary()
   Adding Integers
   >>> print adding_template.problem()
   Calculate $ -4 + 1 = res?$
   >>> print adding_template.answer()
   Result is: $res=-3$

Changing randomly the set of parameters::

   >>> adding_template.update(ekey=15) #another set of random parameters
   >>> print adding_template.problem()
   Calculate $ 2 + 10 = res?$
   >>> print adding_template.answer()
   Result is: $res=12$

Changing randomly but setting one of them::
    
   >>> adding_template.update(ekey=15,edict={'a':99}) #another set of random parameters
   >>> print adding_template.problem()
   Calculate $ 99 + 10 = res?$
   >>> print adding_template.answer()
   Result is: $res=109$

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#MEGUA modules
from paramparse import parameter_change
from platex import pcompile
from mathcommon import *
from msc15 import * #algebra
from msc26 import *
from msc60 import * #probability
from msc62 import * #statistics
from msc65 import * #numerical


#Import the random generator object.
from ur import ur 
from cr import r_stem

#, edict=" + str(edict) + ")\n")
import tikzmod
import subprocess
import codecs

#Sage
from sage.all import *

#Warnings
# http://www.doughellmann.com/PyMOTW/warnings/
import warnings

import re
import tempfile
import os


class ExerciseBase:
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
        self.update(ekey,edict)

    def __str__(self):
        return str(self.__dict__)

    def _repr_(self): 
        return str(self.__class__) + r"(" + repr(self.__dict__) + ")"

    def _latex_(self): #sage _ repr _
        return "To be done"

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


    def make_random(self,edict=None):
        """
        Derive this function.
        """    
        pass


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


    def check(self, maxtime=None):
        pass
    
    
    def summary(self):
        """#, edict=" + str(edict) + ")\n")
        Use class text self._summary_text and replace for parameters on dictionary. Nothing is saved.
        #TODO: maybe summary does not need replacements!
        """
        return parameter_change(self._summary_text,self.__dict__)

    def problem(self,removemultitag=False):
        """
        Use class text self._problem_text and replace for parameters on dictionary. 
        Nothing is saved.

        If removemultitag=true, the tags <multiplechoice> ... </multiplechoice> are removed.
        """
        if removemultitag:
            text1 = self.remove_multiplechoicetag(self._problem_text)
        else:
            text1 = self._problem_text
        text2 = parameter_change(text1,self.__dict__)
        return self._change_text(text2)

    def answer(self,removemultitag=False):
        """
        Use class text self._answer_text and replace for parameters on dictionary. 
        Nothing is saved.

        If removemultitag=true, the tags <multiplechoice> ... </multiplechoice> are removed.
        """
        if removemultitag:
            text1 = self.remove_multiplechoicetag(self._answer_text)
        else:
            text1 = self._answer_text
        text2 = parameter_change(text1,self.__dict__)
        self.c_answer = self._change_text(text2)
        return self.c_answer


    def _change_text(self,text1):
        """Called after parameter_change call. See above."""
        text2 = self.rewrite(text1)
        if text2 is None:
            raise NameError('rewrite(s,text) function is not working.')
        text3 = self.latex_images(text2)
        text4 = self.show_one(text3)
        text5 = self.old_html(text4)
        self.multiplechoice_parser(text5)  #extract information but don't change text
        return text5



    def unique_name(self):
        return self._unique_name


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

        

    def sage_graphic(self,graphobj,varname,dimx=5,dimy=5):
        """This function is to be called by the author in the make_random or solve part.
        INPUT:

        - `graphobj`: some graphic object.

        - `varname`: user supplied string that will be part of the filename.

        - `dimx` and `dimy`: size in centimeters.

        """ 
        #Arrows #TODO: this is not working
        #if arrows:
        #    xmin = graphobj.xmin()
        #    xmax = graphobj.xmax()
        #    ymin = graphobj.ymin()
        #    ymax = graphobj.ymax()
        #    xdelta= (xmax-xmin)/10.0
        #    ydelta= (ymax-ymin)/10.0
        #    graphobj += arrow2d((xmin,0), (xmax+xdelta, 0), width=0.1, arrowsize=3, color='black') 
        #    graphobj += arrow2d((0,ymin), (0, ymax+ydelta), width=0.1, arrowsize=3, color='black') 

        gfilename = '%s-%s-%d'%(self.name,varname,self.ekey)
        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.

        #graphobj could be sage or matplotlib object.

        if type(graphobj)==sage.plot.graphics.Graphics:
            graphobj.save("images/"+gfilename+'.png',figsize=(dimx/2.54,dimy/2.54),dpi=100)
        else: #matplotlib assumed
            #http://stackoverflow.com/questions/9622163/matplotlib-save-plot-to-image-file-instead-of-displaying-it-so-can-be-used-in-b
            import matplotlib.pyplot as plt
            from pylab import savefig
            fig = plt.gcf() #Get Current Figure: gcf
            fig.set_size_inches(dimx/2.54,dimy/2.54)
            savefig("images/"+gfilename+'.png') #,figsize=(dimx/2.54,dimy/2.54),dpi=100)
            
        self.image_list.append(gfilename) 
        return r"<img src='images/%s.png'></img>" % gfilename



    def sage_staticgraphic(self,fullfilename,dimx=150,dimy=150):
        """This function is to be called by the author in the make_random or solve part.

        INPUT:

        - `fullfilename`: full filename for the graphic or picture.
        - `dimx` and `dimy`: display image in (dimx,dimy) pixels.

        NOTES:
            - see also ``s.sage_graphic``.
        """ 
        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.
        os.system("cp %s images" % fullfilename)
        gfilename = os.path.split(fullfilename)[1]
        #print "gfilename=",gfilename
        self.image_list.append(gfilename) 
        return r"<img src='images/%s' alt='%s' height='%d' width='%d'></img>" % (gfilename,self.name+' graphic',dimx,dimy)

    def latex_images(self,input_text):
        """When <latex percent%> ... </latex> is present, then 
        it is necessary to produce them.
        """

        #VER LATEXIMG.PY


        #important \\ and \{

        #old pattern:
        #tikz_pattern = re.compile(r'\\begin\{tikzpicture\}(.+?)\\end\{tikzpicture\}', re.DOTALL|re.UNICODE)

        #print "Group 0:",match.group(0) #all
        #print "Group 1:",match.group(1) #scale (see http://www.imagemagick.org/script/command-line-processing.php#geometry)
        #print "Group 2:",match.group(2) #what is to compile

        latex_pattern = re.compile(r'<\s*latex\s+(\d+%)\s*>(.+?)<\s*/latex\s*>', re.DOTALL|re.UNICODE)
        latex_error_pattern = re.compile(r"!.*?l\.(\d+)(.*?)$",re.DOTALL|re.M)

        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.

        #Cycle through existent tikz code and produce pdf and png files.
        graphic_number = 0
        match_iter = re.finditer(latex_pattern,input_text)#create an iterator
        for match in match_iter:
            #Graphic filename
            gfilename = '%s-%d-%02d'%(self.name,self.ekey,graphic_number)
            #print "=========="
            #print gfilename
            #print "=========="
            #Compile what is inside <latex>...</latex> to a image
            tikz_picture = match.group(2) 
            #TODO: mudar tikz_graphics para latex_image.tex
            #Note: compile only in a images/*.tex folder
            try:
                tikz_tex = Exercise.megbook.template("tikz_graphics.tex", 
                                pgfrealjobname=r"\pgfrealjobname{%s}"%self.name, 
                                beginname=r"\beginpgfgraphicnamed{%s}"%gfilename, 
                                tikz_picture=tikz_picture)
                pcompile(tikz_tex,'images','%s-%d-%02d'%(self.name,self.ekey, graphic_number))
                #convert -density 600x600 pic.pdf -quality 90 -resize 800x600 pic.png
                cmd = "cd images;convert -density 100x100 '{0}.pdf' -quality 95 -resize {1} '{0}.png' 2>/dev/null".format(
                    gfilename,match.group(1),gfilename)
                #print "============== CMD: ",cmd
                os.system(cmd)
                os.system("cp images/%s.tex ." % gfilename)
                graphic_number += 1
                self.image_list.append(gfilename) 
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
                    print "There was a problem with an latex image file."
                #if latex inside codemirror does not work
                #this is the best choice: 
                #print "You can download %s.tex and use your windows LaTeX editor to help find the error." % gfilename
                os.system("mv images/%s.tex ." % gfilename)

                #Using HTML and CodeMirror to show the error.
                print "You can open %s.html to help debuging." % gfilename
                tikz_html = Exercise.megbook.template("latex_viewer.html", 
                                pgfrealjobname=r"\pgfrealjobname{%s}"%self.name, 
                                beginname=r"\beginpgfgraphicnamed{%s}"%gfilename, 
                                tikz_tex=tikz_tex,
                                sname=self.name,
                                errmessage=match.group(0),
                                linenum=match.group(1)
                                )

                f = codecs.open(gfilename+'.html', mode='w', encoding='utf-8')
                f.write(tikz_html)
                f.close()
                print "================"
                raise Exception


        #Cycle through existent tikz code and produce a new html string .
        graphic_number = 0
        gfilename = '%s-%d-%02d'%(self.name,self.ekey,graphic_number)
        (new_text,number) = latex_pattern.subn(r"<img src='images/%s.png'></img>" % gfilename, input_text, count=1)
        while number>0:
            graphic_number += 1
            gfilename = '%s-%d-%02d'%(self.name,self.ekey,graphic_number)
            (new_text,number) = latex_pattern.subn(r"<img src='images/%s.png'></img>" % gfilename, new_text, count=1)
        
        #TODO: falta gravar as imagens na lista deste exercicio.

        return new_text



    def r_graphic(self, r_commands, varname,dimx=7,dimy=7): #cm
        """This function executes r_commands in a shell that should produce a plot (boxplot, etc) 
           to a file that will be located inside
           a "image/" directory.

        NOTE: the sage interface "r." is not capable of ploting at 
        least in version 5.2" because png was not compiled with R.
        This function uses an external (to Sage) fresh R instalation.

        INPUT:

            - `r_commands`: valid sequence of R commands to be executed that should produce a graphic.

            - `varname`: user supplied string that will be part of the filename.

            - `dimx` and `dimy`: size in centimeters.
        
        OUTPUT:

            - a graphic png boxplot inside directory "image/".

        """

        #base name for the graphic file
        gfilename = '%s-%s-%d'%(self.name,varname,self.ekey)
        #create if does not exist the "image" directory
        os.system("mkdir -p images") #The "-p" ommits errors if it exists.

        f = open("images/%s.R" % gfilename,"w")
        #f.write("setwd('images')")
        f.write("png('%s.png',width = %d, height = %d, units = 'cm', res=100)\n" % (gfilename,dimx,dimy) )
        f.write(r_commands + '\n')
        f.write("dev.off()\n")
        f.close()
        #os.system("/usr/bin/R --silent --no-save < images/%s.R" % gfilename)
        os.system("cd images; unset R_HOME; /usr/bin/R CMD BATCH --quiet --no-environ --no-save --slave -- %s.R" % gfilename)
        #os.system("/usr/bin/R --slave --no-save -f images/%s.R" % gfilename)

        #Check ex.py:sage_graphic(): this will add a new image to the exercise.
        self.image_list.append(gfilename) 
        return r"<img src='images/%s.png'></img>" % gfilename


    def multiplechoice_parser(self,input_text):
        """When <multiplechoice>...</multiplecoice> is present it parses them
        and puts each option in exercise fields: 

        * self.all_choices: list of all choices.
        * self.detailed_answer: full detailed answer.
        * self.has_multiplechoicetag: tell that choices came from this syntax

        This routine only extracts information
        Does not change the "answer" or "problem" part like the latex_images that
        needs to put <img ... fig filename>

        """

        if "CDATA" in input_text:
            print "#TODO: should issue warning when CDATA and multiplechoice are both present."
            return 


        #Find and extract text inside <multiplechoice>...</multiplechoice>
        choices_match = re.search(r'<\s*multiplechoice\s*>(.+?)<\s*/multiplechoice\s*>', input_text, re.DOTALL|re.UNICODE)
        
        if choices_match is None:
            return 
        #print "group 0=",choices_match.group(0)
        #print "group 1=",choices_match.group(1)

        #Text inside tags <multiplechoice> ... </multiplechoice>
        choice_text = choices_match.group(1)

        #Get all <choice>...</choice>
        choice_pattern = re.compile(r'<\s*choice\s*>(.+?)<\s*/choice\s*>', re.DOTALL|re.UNICODE)

        #Collects all <choice>...</choice> pairs
        match_iter = re.finditer(choice_pattern,choice_text) #create an iterator
        self.all_choices = [ match.group(1) for match in match_iter] #TODO: do this better
        #print "=========================="
        #print self.all_choices
        #print "=========================="
        

        #Find detailed answer and save it
        self.detailed_answer = input_text[choices_match.end():].strip("\t\n ")
        #print "=========================="
        #print "Detailed answer"
        #print self.detailed_answer
        #print "=========================="

        #For sending it's important to know where options are stored.
        self.has_multiplechoicetag = True

    def remove_multiplechoicetag(input_text):
        """When <multiplechoice>...</multiplecoice> removes it from input_text.
        It returns the text but no changes are made in fields.
        """

        if "CDATA" in input_text:
            return "% TODO: CDATA is present."

        #Find and extract text inside <multiplechoice>...</multiplechoice>
        m = re.search(
            r'<\s*multiplechoice\s*>(.+?)<\s*/multiplechoice\s*>', 
            input_text, 
            re.DOTALL|re.UNICODE)

        #TODO: command re.sub does not work in here above to replace at once. 
        #Only re.search (and re.finditer) works!
        if m:
            new_text = input_text[:m.start()] + input_text[m.end()+1:]
        else:
            new_text = input_text

        return new_text

    def collect_options_and_answer(self):
        r"""
        This routine applies when using <multiplechoice>...</multiplechoice>.
        """
        #Elements must be in same order as in function "_siacua_answer_extract"
        centered_all_choices = [ "<center>"+choice+"</center>" for choice in self.all_choices]
        l = centered_all_choices + [self.detailed_answer] #join two lists

        if len(l)<5:
            raise NameError('Missing of options in multiple choice question or full answer. At least 4 options must be given and the first must be the correct one. Also the full answer must be given.')

        #print "==========="
        #print "For _siacua_answer:",l
        #print "=========="
        return l

    def answer_extract_options(self):
        r"""
        Does the parsing of answer to extract options and complete answer.
        This routine applies when using moodle template with CDATA.
        """
        l = re.findall('<!\[CDATA\[(.*?)\]\]>', self.c_answer, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
        if len(l)<5:
            raise NameError('Missing of options in multiple choice question or full answer. At least 4 options must be given and the first must be the correct one. Also the full answer must be given.')
        return l



    def old_html(self,input_text):
        r"""Remove tags like the example and let
        only the "show" part between <center>.        

        EXAMPLE:: (testing this is not done with: sage -t ex.py)

            sage: from ex import *
            sage: ex = Exercise() #dummy
            sage: print ex.old_html(r'''
                <center>
                <div style="display: None">
                 closed set.
                </div>
                <div style="display: None">
                 closed set.
                </div>
                <div style="display: Show">
                open set 1.
                </div>
                <div style="display: None">
                open set 2.
                </div>
                </center> 
                ''')
            open set 1.

        """

        # Replace all "display: None" by empty string.
        (newtext1, nr) = re.subn(
            ur'<div style="display: None">(.+?)</div>', '', 
            input_text, count=0, flags=re.DOTALL|re.UNICODE|re.MULTILINE)

        #print "old_html():", nr

        # Replace all "display: Show" by \1.
        (newtext2, nr) = re.subn(
            ur'<div style="display: Show">(.+?)</div>', ur'\1', 
            newtext1, count=0, flags=re.DOTALL|re.UNICODE|re.MULTILINE)

        #print "old_html():", nr

        return newtext2

    def check_sagepythoncode(row,start=0,many=5, edict=None,silent=False):
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
            print "Check '%s' for syntatical errors on Python code." % row['unique_name'] #TODO: add here a link to common syntatical error 
    
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
                #print "Execute python class '%s' with %d different keys searching for semantical errors in the algorithm." % (row['unique_name'],many)
                print "Execute python class '%s' with %d different keys" % (row['unique_name'],many)
    
            try:
    
                for ekey in range(start,start+many):
                    if not silent:
                        print "    Testing for random key: ekey=",ekey
                    exerciseinstance(row,ekey=ekey,edict=edict)
    
            except: # Exception will be in memory.
                print "    Error on exercise '{0}' with parameters edict={1} and ekey={2}".format(row['unique_name'],edict,ekey)
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
                print "    Please review the code '%s' based on the reported cases." % row['unique_name']
    
        return success
    
    



    
#end of exbase.py
    