# coding=utf-8

r"""
ExSiacua -- Siacua exercise.

AUTHORS:

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


r"""
TECHINCAL NOTES:

Test with:: 

    sage -python -m doctest exlatex.py


"""

#PYTHON modules
import httplib, urllib
import os
#import json


#MEGUA modules  
from megua.exbase import ExerciseBase
from megua.ur import ur 


#Import the random generator object.

#, edict=" + str(edict) + ")\n")
#import tikzmod
#import subprocess
#import codecs

#Sage
#from sage.all import *

#Warnings
# http://www.doughellmann.com/PyMOTW/warnings/
#import warnings

#import re
#import tempfile
#import os



class ExSiacua(ExerciseBase):    
    r"""

    Creation a LaTeX exercise::
        
       sage: meg = MegBook(r'_temp/megbook.sqlite') 
       sage: meg.save(r'''
       ....: %Summary Primitives
       ....: Here one can write few words, keywords about the exercise.
       ....: For example, the subject, MSC code, and so on.
       ....: 
       ....: %Problem
       ....: What is the primitive of ap x + bp@() ?
       ....: 
       ....: %Answer
       ....: The answer is prim+C, with C a real number.
       ....: 
       ....: class E28E28_pdirect_001(ExSiacua):
       ....: 
       ....:    def make_random(self,edict):
       ....:        self.ap = ZZ.random_element(-4,4)
       ....:        self.bp = self.ap + QQ.random_element(1,4)
       ....:        x=SR.var('x')
       ....:        self.prim = integrate(self.ap * x + self.bp,x)
       ....: ''')
       Each problem can have a suggestive name. 
       Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.
       <BLANKLINE>
       Testing python/sage class 'E28E28_pdirect_001' with 100 different keys.
           No problems found in this test.
          Compiling 'E28E28_pdirect_001' with pdflatex.
          No errors found during pdflatex compilation. Check E28E28_pdirect_001.log for details.
    """


    def __init__(self,ekey=None, edict=None):
        
        #Base class call
        ExerciseBase.__init__(self,ekey,edict)
        
        #Create a directory for images and compilation
        os.system("mkdir -p _images") #The "-p" ommits errors if it exists.

 
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





    def print_instance(self):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        summtxt =  self.summary()   
        probtxt =  self.problem()
        answtxt =  self.answer()
        uname   =  self.unique_name()

        #Use jinja2 template to generate LaTeX.
        if 'CDATA' in answtxt:
            answtxt_woCDATA = re.subn(
                '<!\[CDATA\[(.*?)\]\]>', r'\1', 
                answtxt, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]
        else:
            answtxt_woCDATA = re.subn(
                '<choice>(.*?)</choice>', r'<b>Escolha:</b><br>\1<hr>', 
                answtxt, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]



        html_string = self.template("print_instance_html.html",
                uname=uname,
                summtxt=summtxt,
                probtxt=probtxt,
                answtxt=answtxt_woCDATA,
                ekey=self.ekey,
                mathjax_link=mathjax_link)

        #Produce files for pdf and png graphics if any tikz code embed on exercise
        #Ver ex.py: now latex images are produced in ex.problem() and ex.answer()
        #html_string = self.publish_tikz(sname,html_string)


        #show in notebook
        #html(html_string.encode('utf-8'))

        #file with html to export (extension txt prevents html display).

        #To be viewed on browser
        #f = open(sname+'.html','w')
        #f.write(html_string.encode('latin1'))
        #f.close()

        #For megua 5.2
        f = codecs.open(uname+'.html', mode='w', encoding='utf-8')
        f.write(html_string)
        f.close()
        
        salvus.file(uname+'.html')
        
        salvus.html(html_string)
        

        #To be used on sphinx
        #TODO: move this somewhere.
        #f = codecs.open(sname+'.rst', mode='w', encoding='utf-8')
        #f.write(html_string)
        #f.close()

        #file with html to export.
        #f = open(sname+'.html','w')
        #f.write(html_string.encode('latin1'))
        #f.close()

        #Problems with many things:
        #html(html_string.encode('utf-8'))
    

    
    
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
        #os.system("mkdir -p _images") #The "-p" ommits errors if it exists.

        #graphobj could be sage or matplotlib object.

        if type(graphobj)==sage.plot.graphics.Graphics:
            graphobj.save("_images/"+gfilename+'.png',figsize=(dimx/2.54,dimy/2.54),dpi=100)
        else: #matplotlib assumed
            #http://stackoverflow.com/questions/9622163/matplotlib-save-plot-to-image-file-instead-of-displaying-it-so-can-be-used-in-b
            import matplotlib.pyplot as plt
            from pylab import savefig
            fig = plt.gcf() #Get Current Figure: gcf
            fig.set_size_inches(dimx/2.54,dimy/2.54)
            savefig("_images/"+gfilename+'.png') #,figsize=(dimx/2.54,dimy/2.54),dpi=100)
            
        self.image_list.append(gfilename) 
        return r"<img src='_images/%s.png'></img>" % gfilename



    def sage_staticgraphic(self,fullfilename,dimx=150,dimy=150):
        """This function is to be called by the author in the make_random or solve part.

        INPUT:

        - `fullfilename`: full filename for the graphic or picture.
        - `dimx` and `dimy`: display image in (dimx,dimy) pixels.

        NOTES:
            - see also ``s.sage_graphic``.
        """ 
        #create if does not exist the "image" directory
        #os.system("mkdir -p _images") #The "-p" ommits errors if it exists.
        os.system("cp %s _images" % fullfilename)
        gfilename = os.path.split(fullfilename)[1]
        #print "gfilename=",gfilename
        self.image_list.append(gfilename) 
        return r"<img src='_images/%s' alt='%s' height='%d' width='%d'></img>" % (gfilename,self.name+' graphic',dimx,dimy)

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
        #os.system("mkdir -p _images") #The "-p" ommits errors if it exists.

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
                pcompile(tikz_tex,'_images','%s-%d-%02d'%(self.name,self.ekey, graphic_number))
                #convert -density 600x600 pic.pdf -quality 90 -resize 800x600 pic.png
                cmd = "cd _images;convert -density 100x100 '{0}.pdf' -quality 95 -resize {1} '{0}.png' 2>/dev/null".format(
                    gfilename,match.group(1),gfilename)
                #print "============== CMD: ",cmd
                os.system(cmd)
                os.system("cp _images/%s.tex ." % gfilename)
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
                os.system("mv _images/%s.tex ." % gfilename)

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
        (new_text,number) = latex_pattern.subn(r"<img src='_images/%s.png'></img>" % gfilename, input_text, count=1)
        while number>0:
            graphic_number += 1
            gfilename = '%s-%d-%02d'%(self.name,self.ekey,graphic_number)
            (new_text,number) = latex_pattern.subn(r"<img src='_images/%s.png'></img>" % gfilename, new_text, count=1)
        
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
        #os.system("mkdir -p images") #The "-p" ommits errors if it exists.

        f = open("_images/%s.R" % gfilename,"w")
        #f.write("setwd('images')")
        f.write("png('%s.png',width = %d, height = %d, units = 'cm', res=100)\n" % (gfilename,dimx,dimy) )
        f.write(r_commands + '\n')
        f.write("dev.off()\n")
        f.close()
        #os.system("/usr/bin/R --silent --no-save < _images/%s.R" % gfilename)
        os.system("cd _images; unset R_HOME; /usr/bin/R CMD BATCH --quiet --no-environ --no-save --slave -- %s.R" % gfilename)
        #os.system("/usr/bin/R --slave --no-save -f _images/%s.R" % gfilename)

        #Check ex.py:sage_graphic(): this will add a new image to the exercise.
        self.image_list.append(gfilename) 
        return r"<img src='_images/%s.png'></img>" % gfilename


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



    def siacuapreview(self,ekeys=[]):
        r"""

        INPUT:

        - ``exname``: problem name (name in "class E12X34_something_001(Exercise):").

        - ``ekeys``: list of numbers that generate the same problem instance.

        OUTPUT:

        - this command writes an html file with all instances.

        NOTE:

        - you can export between 3 and 6 wrong options and 1 right.

        EXAMPLE:

            sage: meg.siacuapreview(exname="E12X34",ekeys=[1,2,5])


        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.

        """

        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        (concept_dict,concept_list) = self._siacua_extract(row['summary_text'])

        self.siacuaoption_template = self.env.get_template("siacuapreview_option.html")

        allexercises = u''

        for e_number in ekeys:

            #Create exercise instance
            ex_instance = exerciseinstance(row, ekey=e_number)

            problem = ex_instance.problem(removemultitag=True)
            answer  = ex_instance.answer(removemultitag=True)
    
            #Adapt for appropriate URL for images
            #if ex_instance.image_list != []:
            #    problem = self._adjust_images_url(problem)
            #    answer = self._adjust_images_url(answer)
            #    self.send_images()
    
            #TODO: pass this to ex.py
            if ex_instance.has_multiplechoicetag:
                answer_list = ex_instance.collect_options_and_answer()
            else:
                print ex_instance.name,"has [CDATA] field. Please change to <showone> ... </showone> markers."
                answer_list = ex_instance.answer_extract_options()

            all_options = u'<table style="width:100%;">\n'

            for a in answer_list[:-1]:
                option_html = self.siacuaoption_template.render(optiontext=a)
                all_options += option_html
            
            all_options += u'</table>\n'

            ex_text = u'<h3>Concretizac\xe3o: ekey=' + str(e_number) + '</h3>'
            ex_text += problem + '<br/>'
            ex_text += all_options 
            ex_text += answer_list[-1]

            #Add one more instance with ekey
            allexercises += ex_text

        self.siacuapreview_header = self.env.get_template("siacuapreview_header.html")

        all_html = self.siacuapreview_header.render(
                exname = exname,
                allexercises = allexercises
            )


        #write all to an html file.
        f = codecs.open(exname+'.html', mode='w', encoding='utf-8')
        f.write(all_html)
        f.close()

        os.system("rm *.tex")	




    def siacua(self,exname,ekeys=[],sendpost=False,course="calculo3",usernamesiacua="",grid2x2=0,siacuatest=False):
        r"""

        INPUT:

        - ``exname``: problem name (name in "class E12X34_something_001(Exercise):").

        - ``ekeys``: list of numbers that generate the same problem instance.

        - ``sendpost``: if True send information to siacua.

        - ``course``: Right now could be "calculo3", "calculo2". Ask siacua administrator for more.

        - ``usernamesiacua``: username used by the author in the siacua system.

        - ``grid2x2``: write user options in multiplechoice in a 2x2 grid (useful for graphics) values in {0,1}.

        OUTPUT:

        - this command prints the list of sended exercises for the siacua system.

        NOTE:

        - you can export between 3 and 6 wrong options and 1 right.

        EXAMPLE:

            sage: meg.siacua(exname="E12X34",ekeys=[1,2,5],sendpost=True,course="calculo2",usernamesiacua="jeremias")

        TODO:

        - securitykey: implemenent in a megua-server configuration file.

        LINKS:
            http://docs.python.org/2/library/json.html
            http://stackoverflow.com/questions/7122015/sending-post-request-to-a-webservice-from-python

        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.

        TESTS:
            ~/Dropbox/all/megua/archive$ sage jsontest.sage

        """

        if usernamesiacua=="":
            print "Please do 'meg.siacua?' in a cell for usage details."
            return

        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        (concept_dict,concept_list) = self._siacua_extract(row['summary_text'])

        #While POST is working do not need to print SQL statments in output.
        #For _siacua_sqlprint
        #f = codecs.open(exname+'.html', mode='w', encoding='utf-8')
        #f.write(u"<html><body><h2>Copy/paste do conte\xFAdo e enviar ao Sr. Si\xE1cua por email. Obrigado.</h2>")
        
        for e_number in ekeys:

            #Create exercise instance
            ex_instance = exerciseinstance(row, ekey=e_number)

            problem = ex_instance.problem()
            answer = ex_instance.answer()
    
            #Adapt for appropriate URL for images
            if ex_instance.image_list != []:
                problem = self._adjust_images_url(problem)
                answer = self._adjust_images_url(answer)
                self.send_images()
    

            #TODO: pass this to ex.py
            if ex_instance.has_multiplechoicetag:
                if ex_instance.image_list != []:
                    answer_list = [self._adjust_images_url(choicetxt) for choicetxt in ex_instance.collect_options_and_answer()]
                else:
                    answer_list = ex_instance.collect_options_and_answer()
            else:
                print ex_instance.name,"has [CDATA] field. Please change to <showone> ... </showone> markers."
                answer_list = ex_instance.answer_extract_options()

            #Create images for graphics (if they exist) 
                #for problem
                #for each answer
                #collect consecutive image numbers.

            #build json string
            send_dict =  self._siacua_json(course, exname, e_number, problem, answer_list, concept_list)
            send_dict.update(dict({'usernamesiacua': usernamesiacua, 'grid2x2': grid2x2, 'siacuatest': siacuatest}))
            send_dict.update(concept_dict)

            #Call siacua for store.
            if sendpost:
                send_dict.update(dict({'usernamesiacua': usernamesiacua}))
                self._siacua_send(send_dict)
            else:
                print "Not sending to siacua. Dictionary is", send_dict

            #While POST is working do not need this.
            #self._siacua_sqlprint(send_dict,concept_list,f)


        #When producing instances of exercise a folder images is created.
        #os.system("rm -r images")

        #While POST is working do not need this.
        #Ending _siacua_sqlprint
        #f.write(r"</body></html>")
        #f.close()
        #print r"Copy/paste of contents and send to Sr. Siacua using email. Merci."




    def send_images(self):
        """Send images to siacua: now is to put them in a drpobox public folder"""
        # AttributeError: MegBookWeb instance has no attribute 'image_list'
        #for fn in self.image_list:
        #    os.system("cp -uv _images/%s.png /home/nbuser/megua_images" % fn)
        os.system("cp -ru _images/*.png /home/nbuser/megua_images  > /dev/null") #TODO: check this


    def _adjust_images_url(self, input_text):
        """the url in problem() and answer() is <img src='_images/filename.png'>
        Here we replace _images/ by the public dropbox folder"""

        target = r"https://dl.dropboxusercontent.com/u/10518224/megua_images"
        img_pattern = re.compile(r"src='_images/", re.DOTALL|re.UNICODE)

        (new_text,number) = img_pattern.subn(r"src='%s/" % target, input_text) #, count=1)
        #print "===> Replacement for %d url images." % number
        return new_text



    def _siacua_send(self, send_dict):
        params = urllib.urlencode(send_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        if send_dict["siacuatest"]:
            conn = httplib.HTTPConnection("siacuatest.web.ua.pt")
        else:  
            conn = httplib.HTTPConnection("siacua.web.ua.pt")
        conn.request("POST", "/MeguaInsert.aspx", params, headers)
        response = conn.getresponse()
        #TODO: improve message to user.
        if response.status==200:
            #print 'Sent to server:  "', send_dict["exname"], '" with ekey=', send_dict["ekey"] 
            #print response.status, response.reason
            #TODO: remove extra newlines that the user sees on notebook.
            data = response.read()
            html(data.strip())
        else:
            print "Could not send %s exercise to the server." % send_dict["exname"]
            print response.status, response.reason

        conn.close()


    def _build_ekeys(self,ekeys,many=2):
        r"""From ekeys or many build a range of ekeys."""

        if ekeys is None or len(ekeys)==0:
            
            #generate incresing sequence of keys
            #start = random.randint(1,100000)
            start = ZZ.random_element(1,100000)
            return [start + i for i in range(many)]
        else:
            return ekeys


    def _siacua_json(self,course, exname, e_number, problem, answer_list,concept_list):
        r"""
        LINKS:
            http://docs.python.org/2/library/json.html
        """

        #Dictionary with fields
        d = {}

        #Wrong answers
        d.update( self._siacua_wronganswerdict(answer_list) )

        #USING JSON
        #d.update( {
        #    "exname": exname, 
        #    "ekey": str(e_number), 
        #    "problem":  json.dumps(problem.strip(), encoding="utf-8"), 
        #    "answer":   json.dumps(answer_list[-1].strip(), encoding="utf-8"),
        #    "rv":       json.dumps(answer_list[0].strip(), encoding="utf-8"),
        #    "nre": len(answer_list) - 2
        #    } )

        d.update( {
            "siacua_key": siacua_key,
            "course": course,
            "exname": exname, 
            "ekey": str(e_number), 
            "problem":  problem.strip().encode("utf-8"), 
            "answer":   answer_list[-1].strip().encode("utf-8"),
            "rv":       answer_list[0].strip().encode("utf-8"),
            "nre": len(answer_list) - 2
            } )

        #Concept list
        l = len(concept_list)
        if l>8:
            print "Number of concepts cannot exceed 8."
            return {}

        d["nc"] = l #number of concepts

        d["tc1"] =  concept_list[0][0] if l>=1 else ""
        d["tp1"] =  concept_list[0][1] if l>=1 else ""

        d["tc2"] =  concept_list[1][0] if l>=2 else ""
        d["tp2"] =  concept_list[1][1] if l>=2 else ""

        d["tc3"] =  concept_list[2][0] if l>=3 else ""
        d["tp3"] =  concept_list[2][1] if l>=3 else ""

        d["tc4"] =  concept_list[3][0] if l>=4 else ""
        d["tp4"] =  concept_list[3][1] if l>=4 else ""

        d["tc5"] =  concept_list[0][0] if l>=5 else ""
        d["tp5"] =  concept_list[0][1] if l>=5 else ""

        d["tc6"] =  concept_list[1][0] if l>=6 else ""
        d["tp6"] =  concept_list[1][1] if l>=6 else ""

        d["tc7"] =  concept_list[2][0] if l>=7 else ""
        d["tp7"] =  concept_list[2][1] if l>=7 else ""

        d["tc8"] =  concept_list[3][0] if l>=8 else ""
        d["tp8"] =  concept_list[3][1] if l>=8 else ""


        #TODO: colocar concepts_list no dict

        #return json.dumps(d,
        #    ensure_ascii=True, 
        #    encoding="utf-8")
        return d


    def _siacua_wronganswerdict(self,alist):
        r"""Wrong answer extraction"""

        nre = len(alist) - 2 # 2 = "correct option" + "detailed answer"
        #TODO: warn user from this maximum
        #assume(0<=nre<=6)

        d = dict()

        #Using JSON:
        #d["re1"] =  json.dumps(alist[1].strip(), encoding="utf-8") if nre>=1 else ""
        #d["re2"] =  json.dumps(alist[2].strip(), encoding="utf-8") if nre>=2 else ""
        #d["re3"] =  json.dumps(alist[3].strip(), encoding="utf-8") if nre>=3 else ""
        #d["re4"] =  json.dumps(alist[4].strip(), encoding="utf-8") if nre>=4 else ""
        #d["re5"] =  json.dumps(alist[5].strip(), encoding="utf-8") if nre>=5 else ""
        #d["re6"] =  json.dumps(alist[6].strip(), encoding="utf-8") if nre>=6 else ""

        d["re1"] =  alist[1].strip().encode("utf-8") if nre>=1 else ""
        d["re2"] =  alist[2].strip().encode("utf-8") if nre>=2 else ""
        d["re3"] =  alist[3].strip().encode("utf-8") if nre>=3 else ""
        d["re4"] =  alist[4].strip().encode("utf-8") if nre>=4 else ""
        d["re5"] =  alist[5].strip().encode("utf-8") if nre>=5 else ""
        d["re6"] =  alist[6].strip().encode("utf-8") if nre>=6 else ""

        return d

    def _siacua_sqlprint(self,send_dict, concept_list,f):
        """Print SQL INSERT instruction"""

        #Using JSON:
        #html_string = self.template("print_instance_sql.html",
        #        exname  = send_dict["exname"],
        #        ekey    = send_dict["ekey"],
        #        probtxt = json.loads(send_dict["problem"]),
        #        answtxt = json.loads(send_dict["answer"]),
        #        correct = send_dict["rv"], #"resposta verdadeira" (true answer)
        #        nwrong  = send_dict["nre"],
        #        wa1     = json.loads(send_dict["re1"]) if send_dict["re1"]!="" else "",
        #        wa2     = json.loads(send_dict["re2"]) if send_dict["re2"]!="" else "",
        #        wa3     = json.loads(send_dict["re3"]) if send_dict["re3"]!="" else "",
        #        wa4     = json.loads(send_dict["re4"]) if send_dict["re4"]!="" else "",
        #        wa5     = json.loads(send_dict["re5"]) if send_dict["re5"]!="" else "",
        #        wa6     = json.loads(send_dict["re6"]) if send_dict["re6"]!="" else "",
        #        level   = send_dict["level"],
        #        slip    = send_dict["slip"],
        #        guess   = send_dict["guess"],
        #        discr   = 0.3,
        #)

        html_string = self.template("print_instance_sql.html",
                exname  = send_dict["exname"],
                ekey    = send_dict["ekey"],
                probtxt = send_dict["problem"],
                answtxt = send_dict["answer"],
                correct = send_dict["rv"], #"resposta verdadeira" (true answer)
                nwrong  = send_dict["nre"],
                wa1     = send_dict["re1"] if send_dict["re1"]!="" else "",
                wa2     = send_dict["re2"] if send_dict["re2"]!="" else "",
                wa3     = send_dict["re3"] if send_dict["re3"]!="" else "",
                wa4     = send_dict["re4"] if send_dict["re4"]!="" else "",
                wa5     = send_dict["re5"] if send_dict["re5"]!="" else "",
                wa6     = send_dict["re6"] if send_dict["re6"]!="" else "",
                level   = send_dict["level"],
                slip    = send_dict["slip"],
                guess   = send_dict["guess"],
                discr   = send_dict["discr"],
	)

        f.write(html_string)

        for c in concept_list:

            html_string = self.template("print_instance_sql2.html",
                conceptid  = c[0],
                weight     = c[1],
            )

            f.write(html_string)



    def _siacua_extract(self,summary_text):
        """
        Extract from summary:
            SIACUAstart
            guess=2;  slip= 0.2; guess=0.25; discr=0.3
            concepts = [(1221, 1)]
            SIACUAend
        export to:
                level   = send_dict["level"],
                slip    = send_dict["slip"],
                guess   = send_dict["guess"],
        """

        #TODO: TERMINAR esta FUNcao

        concepts_match = re.search(
            r'SIACUAstart(.*?)SIACUAend', 
            summary_text, 
            flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)

        if concepts_match is not None:
            #print "GROUP 1=", concepts_match.group(1)
            exec concepts_match.group(1)
            #[assert( w in globals()) for w in ['guess', 'slip', 'guess', 'discr', 'concepts'] ]
        else:
            print "For the siacua system %SUMMARY needs the following lines:\nSIACUAstart\nguess=2;  slip= 0.2; guess=0.25; discr=0.3;\nconcepts = [(1221, 0.5),(1222, 1)]\nSIACUAend\n"
            raise ValueError

        return (dict(level=level, slip=slip, guess=guess,discr=discr), concepts)
