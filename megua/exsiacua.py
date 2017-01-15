# coding=utf-8

r"""
ExSiacua -- Siacua exercises 

Siacua are single choice (also called multiple choice) exercises to be
used in siacua system (developed at Univ. Aveiro in a different project than
this MEGUA package).

AUTHORS:

- Pedro Cruz (2016-01): first modifications for use in SMC.


EXAMPLES:


A Siacua exercise in portuguese:

::

       sage: from megua.all import *
       sage: meg = MegBook(r'_input/megbook.sqlite') 
       sage: meg.save(r'''
       ....: %SUMMARY Probabilidade; Regra de Laplace
       ....:  
       ....:  
       ....: Este exercício é um problema básico de Regra de Laplace
       ....:  
       ....: SIACUAstart
       ....: level=1
       ....: slip=0.2
       ....: guess=0.25
       ....: discr=0.3
       ....: concepts = [(4731, 1)]
       ....: SIACUAend
       ....:  
       ....: %PROBLEM Exemplo
       ....:  
       ....: A Maria gravou v1 CD, v2 de música rock e v3 com 
       ....: música popular, mas esqueceu-se de identificar cada um deles. 
       ....: Qual é a probabilidade de ao escolher dois CD ao acaso, 
       ....: um ser de música rock e o outro ser de música popular?
       ....: 
       ....: <multiplechoice>
       ....: <choice> $$vresposta$$ </choice>
       ....: <choice> $$errada1$$ </choice>
       ....: <choice> $$errada2$$ </choice>
       ....: <choice> $$errada3$$ </choice>
       ....: </multiplechoice>
       ....:  
       ....: %ANSWER
       ....:  
       ....: A resposta é $vresposta$.<br>
       ....:  
       ....: Utilizaremos a Regra de Laplace
       ....: $$p(A)=\frac{\text{nº de casos favoráveis}}{\text{nº de casos possíveis}}$$
       ....: Nº de casos possíveis: $v1\times(v1-1)=cp$<br>
       ....:  
       ....: Nº de casos favoráveis: $2\times v2\times v3=cf$
       ....:  
       ....: $$P(A)=\frac{cf}{cp}=vresposta$$
       ....:  
       ....: class E97K50_Laplace_002(ExSiacua):
       ....:     _unique_name = "E97K50_Laplace_002"
       ....:     def make_random(s,edict=None):
       ....:         #problem 
       ....:         s.v1 = ur.iunif(5,15)
       ....:         s.v2 = ur.iunif(1,s.v1-2)
       ....:         s.v3 = s.v1-s.v2
       ....:         #answer
       ....:         s.cp=s.v1*(s.v1-1)
       ....:         s.cf=2*s.v2*s.v3
       ....:         s.vresposta = s.cf/s.cp
       ....:         #Opções Erradas
       ....:         s.errada1 = s.cp/s.cf
       ....:         s.errada2 = s.v1*s.v1/s.cp
       ....:         s.errada3 = s.cf/(s.cp/2)       
       ....: ''')
       Exsicua module say: firefox  _output/E97K50_Laplace_002/E97K50_Laplace_002.html
       sage: ex = meg.new("E97K50_Laplace_002", returninstance=True)
       sage: ex.print_instance()
       Exsicua module say: firefox  _output/E97K50_Laplace_002/E97K50_Laplace_002.html
       sage: ex.siacuapreview(ekeys=[10,20,30])
       Exsicua module say: firefox  _output/E97K50_Laplace_002/E97K50_Laplace_002_siacuapreview.html in the browser and press F5.


Another example that is sent to siacua system:
    
::

       sage: from megua.megbook import MegBook 
       sage: #from megua.exsiacua import ExSiacua
       sage: meg = MegBook(r'_input/megbook.sqlite') 
       sage: meg.save(r'''
       ....: %summary Regra de Laplace
       ....:  
       ....: SIACUAstart
       ....: level=1
       ....: slip=0.2
       ....: guess=0.25
       ....: discr=0.3
       ....: concepts = [(4731, 1)]
       ....: SIACUAend 
       ....:  
       ....: %problem Números Bolas e Caixas
       ....:  
       ....: Considera uma caixa com v1 bolas indestiguiveis ao tato, numeradas de 1 a v1.
       ....: Considera também um dado equilibrado com as faces numeradas de 1 a 6.
       ....: Lança-se o dado e tira-se, ao acaso, uma bola da caixa.
       ....: Qual é a probabilidade de os números saídos serem ambos menores que v2?  
       ....:  
       ....: <multiplechoice>
       ....: <choice> $$vresp$$ </choice>
       ....: <choice> $$err1$$ </choice>
       ....: <choice> $$err2$$ </choice>
       ....: <choice> $$err3$$ </choice>
       ....: </multiplechoice>
       ....:  
       ....: %answer
       ....:  
       ....: A resposta é $vresp$.
       ....:  
       ....: <br> Pretendemos saber a probabilidade de os números obtidos serem ambos menores que v2.<br>
       ....:  
       ....: <br> Para determinar a probabilidade pedida utilizaremos a Regra de Laplace 
       ....: $$P(\text{ambos os números menores que v2})=\frac{\text{nº de casos favoráveis}}{\text{nº de casos possíveis}}$$
       ....:  
       ....: Comecemos por construir uma tabela que nos permita verificar todas as hipóteses possíveis de resultado:<br>
       ....:  
       ....: $$\begin{array}{|a|a|c|c|c|c|c|}
       ....: \hline
       ....:     B/D & 1 & 2 & 3 & 4 & 5 & 6\\ \hline
       ....:      
       ....:     linhas
       ....: \end{array}$$
       ....:  
       ....: A caixa tem v1 bolas numeradas de 1 a v1 e o dado tem 6 faces também numeradas de 1 a 6. Portanto:
       ....:   
       ....:    $$\text{O número de casos possíveis é dado por: } v1 \times 6 = v3$$
       ....:  
       ....: Pretendemos saber a probabilidade de, ao retirar uma bola do saco e lançar o dado, 
       ....: obter dois numeros menores que v2.<br>
       ....: <br> Pela tabela podemos verificar que 
       ....:     $$\text{O número de casos favoráveis são } cf$$ 
       ....:      
       ....: Logo a probabilidade pedida é dada por:
       ....:     $$P(\text{ambos os números menores que v2}) = \frac{cf}{cp} = vresp$$  
       ....:  
       ....: class E97K50_Laplace_001(ExSiacua):
       ....:  
       ....:     def make_random(s):
       ....:  
       ....:         s.v1 = ur.iunif(6,10)
       ....:         s.v2 = ur.iunif(2,s.v1)
       ....:  
       ....:         #d={1:0,2:1,3:4,4:9,5:16,6:25,7:36}
       ....:         if s.v2<=7:
       ....:             s.cf = (s.v2-1)^2
       ....:         else:
       ....:             s.cf = 36 + 6*(s.v2 - 7)
       ....:         s.cp = 6*s.v1
       ....:         #s.cf = d[s.v1]
       ....:         s.vresp= round(s.cf/s.cp,2)
       ....:          
       ....:         s.linhas = ""
       ....:         for i in range(s.v1):
       ....:             linha = str(i+1) 
       ....:             for j in range(6):
       ....:                 linha = linha + s.C(i+1,j+1)
       ....:             s.linhas = s.linhas + linha + r" \\ \hline" 
       ....:         s.v3 = s.v1 * 6
       ....:          
       ....:         #Opções Erradas 
       ....:         s.err1 = round(s.vresp*0.9,2)
       ....:         s.err2 = round(s.vresp*1.2,2)
       ....:         s.err3 = round(s.vresp*1.3,2)
       ....:      
       ....:     def C(s,B,D):
       ....:         if B < s.v2 and D < s.v2:
       ....:             return '&(%d,%d)' % (B,D)
       ....:         else:
       ....:             return '& '
       ....:  
       ....: ''')
       Exsicua module say: firefox  _output/E97K50_Laplace_001/E97K50_Laplace_001.html
       sage: ex = meg.new("E97K50_Laplace_001", returninstance=True)
       sage: #ex.siacua(ekeys=[9],sendpost=True,course="matsec",usernamesiacua="f1183",siacuatest=True) #long output


DEVELOPER NOTES:


"""

#*****************************************************************************
#       Copyright (C) 2012,2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#PYTHON modules
import httplib, urllib
import os
import re
import codecs
import subprocess
import requests #TODO: passar tudo da web para este módulo

#import json
#Warnings
# http://www.doughellmann.com/PyMOTW/warnings/
#import warnings
#import tempfile



#SAGEMATH modules
#from sage.all import *


#MEGUA modules  
from megua.exbase import ExerciseBase
from megua.jinjatemplates import templates
from megua.platex import html2latex
from megua.megoptions import *



class ExSiacua(ExerciseBase):

    #TODO: is needed?
    #def __init__(self,ekey=None, edict=None):
    #    ExerciseBase.__init__(self,ekey, edict,rendermethod,dimx,dimy,dpi)

    def update(self,ekey=None,edict=None, render_method=None):


        #For multiplechoice
        self.all_choices = []
        self.has_multiplechoicetag = None #Don't know yet.

        #Extract, from summary, details about bayesian network
        #TODO: old mode of extracting bayesian parameters
        if 'SIACUAstart' in self._summary_text:
            print "exsiacua.py: please remove SIACUAStart...SIACUAend from %SUMMARY."
            print "exsiacua.py: Add those lines, separated by commas ',' to meg.siacua(....) commmand."
            self._siacua_extractparameters()

        #Call user derived function to generate a set of random variables.
        ExerciseBase.update(self,ekey,edict)

        if "multiplechoice" in self.problem():
            options_txt = self._update_multiplechoice(self.problem(),where="problem")
        else:
            options_txt = self._update_multiplechoice(self.answer(), where="answer")
            print self.unique_name()," has multiplechoice in answer part. CHANGE <multiplechoice> to the %problem"


        if "multiplechoice" in self.problem():
            options_txt = self._update_multiplechoice(self.problem(),where="problem")
        else:
            print self.unique_name()," has multiplechoice in answer part. CHANGE <multiplechoice> to the %problem"
            self._update_multiplechoice(self.answer(),where="answer")


        self.detailed_answer  = self._remove_multiplechoicetag(self.answer())
        self.formated_problem = self._remove_multiplechoicetag(self.problem()) + u'\n<br/>' + options_txt + u'\n<br/>' 



    def search_replace(self,input_text):
        """Called after parameter_change call. See above."""

        #Base tranformation
        text = ExerciseBase.search_replace(self,input_text)

        #Other transformations
        text = self.latex_render(text) #ver UnifiedGraphics
        text = self.show_one(text)
        text = _old_html(text)

        return text


    def print_instance(self):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).

        TODO: this view should be almost equal to view the exercise in siacua
        """

        summtxt =  self.summary()   
        probtxt =  self.problem()
        answtxt =  self.answer()
        uname   =  self.unique_name()



        html_string = templates.render("exsiacua_print_instance.html",
                uname=uname,
                summtxt=summtxt,
                probtxt=probtxt,
                answtxt=answtxt,
                formated_problem = self.formated_problem,
                detailed_answer  = self.detailed_answer,
                ekey=self.ekey,
                mathjax_header=MATHJAX_HEADER)

        #print html_string

        EXERCISE_HTML_PATHNAME = os.path.join(self.wd_fullpath,uname+'.html')
        f = codecs.open(EXERCISE_HTML_PATHNAME, mode='w', encoding='utf-8')
        f.write(html_string)
        f.close()


        if MEGUA_PLATFORM=='SMC':
            from smc_sagews.sage_salvus import salvus
            salvus.html(html_string)
        elif MEGUA_PLATFORM=='DESKTOP':
            print "Exsicua module say: firefox ",EXERCISE_HTML_PATHNAME
            subprocess.Popen(["firefox","-new-tab", EXERCISE_HTML_PATHNAME])
        else:
            print "Exsiacua module say: MEGUA_PLATFORM must be properly configured at $HOME/.megua/conf.py"



    def _update_multiplechoice(self,input_text,where):
        """
        Called by ExSiacua.update()

        Parses <multiplechoice>...</multiplecoice> and puts each option 
        in exercise fields: 

        * self.all_choices: list of all choices.
        * self.formated_problem
        * self.detailed_answer: full detailed answer.
        * self.has_multiplechoicetag: tell that choices came from this syntax

        This routine only extracts information
        Does not change the "answer" or "problem" part like the latex_images that
        needs to put <img ... fig filename>

        """

        #TODO: remove in a few revisions
        if "CDATA" in input_text:
            print "TODO: in %s, should issue warning when CDATA and multiplechoice are both present." % self.unique_name()
            self.detailed_answer = "Contains [CDATA]\n"
            self.all_choices = []
            raise SyntaxError("exsiacua module say:  {} should have <multiplechoice>...</multiplechoice> tags.".format(self.unique_name()))

        #Find and extract text inside <multiplechoice>...</multiplechoice>
        choices_match = re.search(r'<\s*multiplechoice\s*>(.+?)<\s*/multiplechoice\s*>', input_text, re.DOTALL|re.UNICODE)
        #print "group 0=",choices_match.group(0)
        #print "group 1=",choices_match.group(1)

        if choices_match is None:
            raise SyntaxError("exsiacua module: problem should have <multiplechoice>...</multiplechoice> tags.")

        #Text inside tags <multiplechoice> ... </multiplechoice>
        choice_text = choices_match.group(1)

        #Get all <choice>...</choice>
        choice_pattern = re.compile(r'<\s*choice\s*>(.+?)<\s*/choice\s*>', re.DOTALL|re.UNICODE)

        #Collects all <choice>...</choice> pairs
        match_iter = re.finditer(choice_pattern,choice_text) #create an iterator
        self.all_choices = [ match.group(1) for match in match_iter] #TODO: do this better
        #print "=========================="
        #print "exsiacua.py module say:", self.all_choices
        #print "=========================="

        siacuaoption_template = templates.get_template("exsiacua_previewoption.html")

        all_options = u'<table style="width:100%;">\n'

        for option in self.all_choices:
            option_html = siacuaoption_template.render(optiontext=option)
            all_options += option_html

        all_options += u'</table>\n'
        #For sending it's important to know where options are stored.
        self.has_multiplechoicetag = True

        return all_options





    def _remove_multiplechoicetag(self,input_text):
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


    def _collect_options_and_answer(self):
        r"""
        This routine applies when using <multiplechoice>...</multiplechoice>.
        """
        #Elements must be in same order as in function "_siacua_answer_extract"
        centered_all_choices = [ "<center>"+choice+"</center>" for choice in self.all_choices]
        l = centered_all_choices + [self.detailed_answer] #join two lists

        if len(l)<5:
            raise NameError('exsiacua modukle: missing of options in multiple choice question or full answer. At least 4 options must be given and the first must be the correct one. Also the full answer must be given.')

        #print "==========="
        #print "For _siacua_answer:",l
        #print "=========="
        return l


#TODO: remove this lines soon.
#    def _answer_extract_options(self):
#        r"""
#        Does the parsing of answer to extract options and complete answer.
#        This routine applies when using moodle template with CDATA.
#        """
#        l = re.findall('<!\[CDATA\[(.*?)\]\]>', self.answer(), re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
#        if len(l)<5:
#            raise NameError("""exsiacua: missing multiple choice options."""\
#               """At least 4 options must be given and the first must be """\
#               """the correct one. Also the full answer must be given.""")
#        return l






    def siacuapreview(self,ekeys):
        r"""

        INPUT:

        - ``ekeys``: list of numbers that generate the same problem instance.

        OUTPUT:

        - this command writes an html file with all instances.

        NOTE:

        - you can export between 3 and 6 wrong options and 1 right.

        EXAMPLE:

            sssssage: ex.siacuapreview(ekeys=[1,2,5])


        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.

        """

        siacuaoption_template = templates.get_template("exsiacua_previewoption.html")

        allexercises = u''

        for e_number in ekeys:

            #Create exercise instance
            self.update(ekey=e_number)


            #TODO: do like in print_instance()
            problem = self._problem_whitoutmc()#m.c. options here?
            answer  = self._answer_whitoutmc() #m.c. options here?
    
            #Adapt for appropriate URL for images
            #if ex_instance.image_list != []:
            #    problem = self._adjust_images_url(problem,course)
            #    answer = self._adjust_images_url(answer,course)
            #    self.send_images()
    
            assert(self.has_multiplechoicetag)
            answer_list = self._collect_options_and_answer()

            all_options = u'<table style="width:100%;">\n'

            for a in answer_list[:-1]:
                option_html = siacuaoption_template.render(optiontext=a)
                all_options += option_html

            all_options += u'</table>\n'



            #TODO: it's not working (see also templates/pt_pt/exsiacua_previewheader.html and exsiacua_previewoption.html)
            rendered_problem = "\n" + r"""<section class="bg-white txt-grey txt-left"><div class="container"><div class="question"><span id="LabelQuestao">%s</span></div>""" % problem + "\n"

            ex_text = u'<h3>Random {} with ekey={}</h3>'.format(self.unique_name(),e_number)
            ex_text += rendered_problem + u'<br/><hr /><br />'
            ex_text += all_options  + r"""</div></section>"""
            ex_text += u'\n<h4>Answer</h4>\n' + answer_list[-1]



            #Add one more instance with ekey
            allexercises += ex_text

        html_string = templates.render(
                "exsiacua_previewheader.html",
                uname = self.unique_name(),
                allexercises = allexercises,
                mathjax_header=MATHJAX_HEADER
        )

        (html_string,number) = re.subn(r"\.OUTPUT/\w+/(\w+)", r"\1", html_string, re.DOTALL|re.UNICODE)  #, count=1)

        
        #write all to an html file.
        html_full_path     = os.path.join(self.wd_fullpath,self.unique_name()+'_siacuapreview.html')
        f = codecs.open(html_full_path, mode='w', encoding='utf-8')
        f.write(html_string)
        f.close()


        if MEGUA_PLATFORM=='SMC':
            from smc_sagews.sage_salvus import salvus
            #print "exsiacua.py: using salvus.link:"
            html_relative_path = os.path.join(self.wd_relative,self.unique_name()+'_siacuapreview.html')
            salvus.file(html_relative_path,raw=True)
        elif MEGUA_PLATFORM=='DESKTOP':
            print "exsiacua.py: opening firefox ",html_full_path,"in the browser and press F5."
            subprocess.Popen(["firefox","-new-tab", html_full_path])
        else:
            print "exsiacua.py module say: MEGUA_PLATFORM must be properly configured at $HOME/.megua/conf.py"


    def _problem_whitoutmc(self):
        """
        The problem text without multiple choice tag.
        """
        assert(self.has_instance)
        return self._remove_multiplechoicetag(self.problem())


    def _answer_whitoutmc(self):
        """
        The answer text without multiple choice tag.
        """
        assert(self.has_instance)
        return self._remove_multiplechoicetag(self.answer())



    def siacua(self,
               ekeys=[],
               course="calculo3",
               usernamesiacua="(no username)",
               level=1,
               slip=0.05,
               guess=0.25,
               discr=0.5,
               concepts = [ (0,  1) ],
               grid2x2=False,
               siacuatest=False,
               sendpost=True
              ):
        r"""

        INPUT:

        - ``ekeys``: list of numbers that generate the same problem instance.

        - ``course``: Right now could be "calculo3", "calculo2". Ask siacua administrator for more.

        - ``usernamesiacua``: username used by the author in the siacua system.

        - ``level``: (usually 1) I don't know what does this mean but it's an small integer number.

        - ``slip``: (0,...,1) The probability of knowing how to answer, commit a mistake.

        - ``guess``: (usually 0.25) The probability of guessing the right option.

        - ``discr``: (0,...,1) Parameter `discr` is the probability that a student knows how to select the right answer.

        - ``concepts``: a list like [(110, 0.3),(135, 0.7)] where 0.3+0.7 = 1 and 110 and 135 are codes of concepts.

        - ``grid2x2``: (usually False) Write exercise answering options in a 2x2 grid (useful for graphics).

        - ``siacuatest``: (usually False) If True, send data to a test machine.

        - ``sendpost``: (usually True) If True send information to siacua, otherwise simulates to check problems.

        OUTPUT:

        - this command prints the list of sended exercises for the siacua system.

        NOTE:

        - you can export between 3 and 6 wrong options and 1 right.

        TODO: securitykey: implemenent in a megua-server configuration file.

        LINKS:
            http://docs.python.org/2/library/json.html
            http://stackoverflow.com/questions/7122015/sending-post-request-to-a-webservice-from-python

        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.

        TESTS:

            ~/Dropbox/all/megua/archive$ sage jsontest.sage

        """

        all_answers = []

        for e_number in ekeys:

            #Create exercise instance
            self.update_timed(ekey=e_number)

            #NOTE: inside self.update (many lines above) there is
            #extract parameters (old mode). This is the new mode:
            self.siacua_parameters = dict(level=level, slip=slip, guess=guess,discr=discr)
            self.siacua_concepts = concepts

            assert(self.has_multiplechoicetag)
            answer_list = self._collect_options_and_answer()

            #build json string
            send_dict =  self._siacua_json(course, self.unique_name(), e_number, self._problem_whitoutmc(), answer_list, self.siacua_concepts)
            send_dict.update(dict({'usernamesiacua': usernamesiacua, 'grid2x2': grid2x2, 'siacuatest': siacuatest}))
            send_dict.update(self.siacua_parameters)

            #Call siacua for store.
            if sendpost:
                send_dict.update(dict({'usernamesiacua': usernamesiacua}))
                print "exsiacua.py: send %s to siacua with ekey=%d."%(self.unique_name(),e_number)
                send_result = self._siacua_send(send_dict)
                all_answers += send_result
                if self.image_pathnames != []: #TODO: check how to avoid send images without exercise
                    self._send_images(siacuatest,course=course)
            else:
                print "Not sending to siacua. Dictionary is", send_dict

        if all_answers:
            print 'Exercícios a consultar no SIACUA: ' + ', '.join(all_answers) + '.'
            if sendpost:
                if siacuatest:
                    print "Abrir http://siacuatest.web.ua.pt depois de entrar no curso: Gestão Professor -- Botão 'Ler Questões'"
                else:
                    print "Abrir http://siacua.web.ua.pt depois de entrar no curso: Gestão Professor -- Botão 'Ler Questões'"
        #end


    def _send_images(self,siacuatest,course):
        """Send images to siacua: now is to put them in a drpobox public folder
        # AttributeError: MegBookWeb instance has no attribute 'image_list'
        #for fn in self.image_list:
        #    os.system("cp -uv _images/%s.png /home/nbuser/megua_images" % fn)
        #
        #TUNE this:os.system("cp -ru _images/*.png /home/nbuser/megua_images  > /dev/null") #TODO: check this
        #import request
        print "exsiacua.py: _send_images(): This are the images to be sent:"
        print self.image_pathnames
        print "end"
        """
        import requests

        if siacuatest:
            url = 'http://siacuatest.web.ua.pt/MeguaInsert2.aspx'
        else:
            url = 'http://siacua.web.ua.pt/MeguaInsert2.aspx'

        for f in self.image_pathnames:
            #print "Sending:",f
            files = {'file': (course+"_"+os.path.basename(f), open(f, 'rb')) }
            r = requests.post(url, files=files)
            #print "exsiacua.py: r.ok=",r.ok

        print "exsiacua.py: done, sending images."

    def _adjust_images_url(self, input_text, course):
        """the url in problem() and answer() is <img src='_images/filename.png'>
        Here we replace _images/ by the public dropbox folder

        OLD Dropbox code:
        #target = r"https://dl.dropboxusercontent.com/u/10518224/megua_images"
        #img_pattern = re.compile(r"src='_images/", re.DOTALL|re.UNICODE)

        #(new_text,number) = img_pattern.subn(r"src='%s/" % target, input_text) #, count=1)
        #print "===> Replacement for %d url images." % number
        #return new_text

        #TODO: adicionar o unique_name caso 
        # - E12X34_Teste_001-E12X34_Teste_001-00.png  (case 1)
        # - E12X34_Teste_001-1.png   (case 2)
        #For case 1: remove exceeding header name
        #(new_text,number) = re.subn("%s-(%s)"%(self.unique_name,self.unique_name), r"\1", new_text, re.DOTALL|re.UNICODE)  #, count=1)
        """

        (new_text,number) = re.subn(r"\.OUTPUT/\w+/(\w+)", r"../imagens/%s_\1"%course, input_text, re.DOTALL|re.UNICODE)  #, count=1)

        #print "exsiacua.py ===> Replacement for %d url images." % number
        #print new_text
        return new_text



    #def _send_images_dropbox(self):
    #    """Send images to siacua: now is to put them in a drpobox public folder"""
    #    # AttributeError: MegBookWeb instance has no attribute 'image_list'
    #    #for fn in self.image_list:
    #    #    os.system("cp -uv _images/%s.png /home/nbuser/megua_images" % fn)
    #    #
    #    #TUNE this:os.system("cp -ru _images/*.png /home/nbuser/megua_images  > /dev/null") #TODO: check this

    #def _adjust_images_url_dropbox(self, input_text):
    #    """the url in problem() and answer() is <img src='_images/filename.png'>
    #    Here we replace _images/ by the public dropbox folder"""
    #
    #    target = r"https://dl.dropboxusercontent.com/u/10518224/megua_images"
    #    img_pattern = re.compile(r"src='_images/", re.DOTALL|re.UNICODE)
    #
    #    (new_text,number) = img_pattern.subn(r"src='%s/" % target, input_text) #, count=1)
    #    #print "===> Replacement for %d url images." % number
    #    return new_text



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

            #TODO: format this output to extract only the <id> 3883 in siacua:
            #TODO: Resultado: <span id="resultado">Muito bem, melhorou o exercício, parabéns! id=3883</span>
            data = response.read()
            if "Muito bem, melhorou" in data:
                akword = "Improved:"
                choice_pattern = re.compile(r'id=(\d+)', re.DOTALL|re.UNICODE)
            else:
                choice_pattern = re.compile(r'id = (\d+)', re.DOTALL|re.UNICODE)
                akword = "New:"

            #print "exsiacua.py: data=",data
            match_iter = re.finditer(choice_pattern,data) 
            all_ids = [ "{} {}".format(akword,match.group(1)) for match in match_iter] #TODO: do this better

        else:

            print "Could not send exercise to the server: %s" % str(send_dict)
            print response.status, response.reason

        conn.close()

        #TODO: improve this because it's only one sent!
        #It's only one exercise sent, each call of this function
        if response.status==200:
            return all_ids
        else:
            return 'Not sent: ekey={}'.format(send_dict["ekey"])


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

        #Adapt for appropriate URL for images
        if self.image_pathnames != []:
            problem = self._adjust_images_url(problem,course)
            answer_list = [self._adjust_images_url(a,course) for a in answer_list]

        d.update( {
            "siacua_key": SIACUA_WEBKEY,
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



    def _siacua_extractparameters(self):
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

        concepts_match = re.search(
            r'SIACUAstart(.*?)SIACUAend', 
            self.summary(), 
            flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)

        if concepts_match is not None:
            #print "GROUP 1=", concepts_match.group(1)
            exec concepts_match.group(1)
            #[assert( w in globals()) for w in ['guess', 'slip', 'guess', 'discr', 'concepts'] ]
            print "Add this to meg.siacua: level=%d,slip=%f,guess=%f,discr=%f,concepts=%s" % (level, slip, guess, discr, concepts)



    #ExSiacua specific conversion
    TO_LATEX = [
        (u'<multiplechoice>', '\n\n'+r'\\begin{enumerate}'+'\n\n'),
        (u'</multiplechoice>', r'\\end{enumerate}'+'\n\n'),
        (u'<choice>', r'\\singleoption '),
        (u'</choice>', '\n\n'),
    ]


    #TODO: put this into develop manual
    @staticmethod
    def to_latex(txt):
        r"""Convert siacua text in problem or answer into latex.
        The following conversions are done:
        - the (simple) html used is converted to latex (html2latex procedure)
        - <multiplechoice> tag is converted to \begin{itemize}
        - <choice> is converted to macro \\singleoption  (an \item)

        INPUT:

        - ``txt``: siacua problem or answer problem.

        EXAMPLE::

        sage: from megua.exsiacua import ExSiacua
        sage: txt = ur'''
        ....: <center>CENTERED</center>
        ....: <multiplechoice>
        ....: <choice> 
        ....: $$f1=\sum_{n=0}^{+\infty}{ser1}, \quad x \in intc1$$
        ....: </choice>
        ....: <choice>  
        ....: $$f1=\sum_{n=0}^{+\infty}{ser1}, \quad x \in intw1$$
        ....: </choice>
        ....: <choice>  
        ....: $$\ln{\left(f11\right)}=\sum_{n=0}^{+\infty}{intser11}
        ....: card1 +lb1 , \quad x \in intw1$$
        ....: </choice>
        ....: </multiplechoice> '''
        sage: print ExSiacua.to_latex(txt)
        <BLANKLINE>
        \begin{center}
        CENTERED\end{center}
        <BLANKLINE>
        \begin{enumerate}
        <BLANKLINE>
        \singleoption  
        $$f1=\sum_{n=0}^{+\infty}{ser1}, \quad x \in intc1$$
        <BLANKLINE>
        \singleoption   
        $$f1=\sum_{n=0}^{+\infty}{ser1}, \quad x \in intw1$$
        <BLANKLINE>
        \singleoption   
        $$\ln{\left(f11\right)}=\sum_{n=0}^{+\infty}{intser11}
        card1 +lb1 , \quad x \in intw1$$
        <BLANKLINE>
        \end{enumerate}
        <BLANKLINE>
 
        """
        
        #Basic conversion
        #txt = txt.encode('utf8')
        newtext = html2latex(txt)
        
        for pr in ExSiacua.TO_LATEX: #see above, outside function
            (newtext, nr) = re.subn(pr[0], pr[1], newtext, count=0, flags=re.DOTALL|re.UNICODE)
        
        newtext = newtext.replace("\n\n","\n")
        
        return newtext


def _old_html(input_text):
    r"""Remove tags like the example below and let
    only the "show" part between <center>.        

    EXAMPLE:: (testing this is not done with: sage -t ex.py)

        sage: from megua.exsiacua import _old_html
        sage: print _old_html(r'''
        ....:    <center>
        ....:    <div style="display: None">
        ....:     closed set.
        ....:    </div>
        ....:    <div style="display: None">
        ....:     closed set.
        ....:    </div>
        ....:    <div style="display: Show">
        ....:    open set 1.
        ....:    </div>
        ....:    <div style="display: None">
        ....:    open set 2.
        ....:    </div>
        ....:    </center> 
        ....:    ''')
        <center>            open set 1.         </center>

    """

    # Replace all "display: None" by empty string.
    (newtext, nr) = re.subn(
        ur'<div style="display: None">(.+?)</div>', '', 
        input_text, count=0, flags=re.DOTALL|re.UNICODE|re.MULTILINE)

    (newtext, nr) = re.subn(
        u'\n', u'', 
        newtext, count=0, flags=re.DOTALL|re.UNICODE|re.MULTILINE)

    #print "old_html():", nr

    # Replace all "display: Show" by \1.
    (newtext, nr) = re.subn(
        ur'<div style="display: Show">(.+?)</div>', ur'\1', 
        newtext, count=0, flags=re.DOTALL|re.UNICODE|re.MULTILINE)

    #newtext = newtext.strip()

    #print "old_html():", nr

    return newtext

