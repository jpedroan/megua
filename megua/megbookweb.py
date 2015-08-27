r"""
MegBookWeb -- Build your own database of exercises to the web.

AUTHORS:

- Pedro Cruz (2012-06): initial version.


"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#Python Modules
import re
import codecs
import random as randomlib #random is imported as a funtion somewhere
import json
import httplib, urllib


#Megua modules:
from megbookbase import *
from xc3web import C3WebExporter
from platex import pcompile
from xmoodle import MoodleExporter
from xsphinx import SphinxExporter
from xlatex import PDFLaTeXExporter
from mconfig import *


#TODO Is it necessary to import other libs?



class MegBookWeb(MegBookBase):
    r"""
    Set of routines for exercise templating to the web.

    INPUT::

    - ``filename`` -- filename where the database is stored.

    This module provides means to use a database of exercises that can be seen as a book of some author or authors.
    """

    def __init__(self,filename=None,natlang='pt_pt'):
        r"""

        INPUT::
        - ``filename`` -- filename where the database is stored.        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.exercise_template = self.megbook.env.get_template("moodle-cloze.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_cloze.xml"
            raise e

        - ``natlang`` -- natural language ('pt_pt', etc).

        """
        MegBookBase.__init__(self,filename=filename,natlang=natlang,markuplang='web')

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.problem_template = self.env.get_template("xc3web_problem.html")
            self.problemanswer_template = self.env.get_template("xc3web_problemanswer.html")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing templates 'xc3web_problem.html' or 'xc3web_problemanswer.html'."
            raise e

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.mchoice_template = self.env.get_template("moodle-mchoice.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_mchoice.xml"
            raise e

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.cloze_template = self.env.get_template("moodle-cloze.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_cloze.xml"
            raise e


    def __str__(self):
        return "MegBookWeb('%s') for %s and markup language %s" % (self.local_store_filename,self.megbook_store.natural_language,self.megbook_store.markup_language)


    def __repr__(self):
        return "MegBookWeb('%s')" % (self.local_store_filename)


    def is_exercise_ok(self,row,dest,silent=True):
        r"""
        Check if exercise is ready for compilation and for python/sage errors.
        """

        # --------------------------------
        # Testing the new python class for 
        # programming errors:
        #     syntax and few instances execution. 
        # -------------------------------
        if not self.exercise_pythontest(row,silent=silent):
            return False


        # --------------------------
        # Testing html compilation. TODO: how to do this?
        # --------------------------
        #if not self.exercise_htmltest(row,dest,silent=silent):
        #    return False

        # Exercise Ok
        return True



    def search_print_row(self,exrow):
        r"""
        This is an helper function of ``Meg.search`` function to print the contents of a search.
        Not to be called by meg user.

        INPUT:

        - ``exrow`` -- an sqlite row structure_ where fields are accessible by name.

        OUTPUT:

        - html or text.

        NOTES:
            unicode is in utf-8 -> string
            http://en.wikipedia.org/wiki/ISO/IEC_8859-1
            Sage html() requires string.
        """
    
        sname = 'Exercise name %s' % exrow['owner_key'].encode('utf8')
        if is_notebook():
            html('<b>' + sname + ': </b><br/>' + exrow['problem_text'].encode('utf8') + '<br/>')
        else:
            print sname + '\n' + exrow['problem_text'].encode('utf8') + '\n'

            

    def print_instance(self, ex_instance):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        summtxt =  ex_instance.summary()   
        probtxt =  ex_instance.problem()
        answtxt =  ex_instance.answer()
        sname   =  ex_instance.name

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
                sname=sname,
                summtxt=summtxt,
                probtxt=probtxt,
                answtxt=answtxt_woCDATA,
                ekey=ex_instance.ekey,
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
        f = codecs.open(sname+'.html', mode='w', encoding='utf-8')
        f.write(html_string)
        f.close()

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
    


    def make_index(self,where='.',debug=False):
        """
        Produce rst code files from the database and an index reading first line of the %summary field.

        Command line use: 
            The ``where`` input argument, when specified,  will contain all details of Sphinx compilation.

        LINKS:

        http://code.activestate.com/recipes/193890-using-rest-restructuredtext-to-create-html-snippet/

        """

        html_index = SphinxExporter(self,where,debug)
        print "Index is at: "+ html_index.htmlfile

        if is_notebook():
            if where == '.': 
                #To open a browser
                pos = html_index.htmlfile.find(".")
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            elif 'data' in where:
                #To open a browser
                pos = html_index.htmlfile.find("/home")
                pos2 = html_index.htmlfile.find("/home",pos+1)
                if pos2>=0:
                    pos = pos2
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            else:
                #print "Index is at: "+ html_index.htmlfile
                print "See index at Megua button at top."
        else:
            print "firefox -no-remote ", html_index.htmlfile

    def make_latex(self,where='.', exerset=None, debug=False):
        """
        Produce a pdflatex file from the database and an index reading first line of the %summary field.

        Command line use: 
            The ``where`` input argument, when specified,  will contain all details of Sphinx compilation.
        """

        PDFLaTeXExporter(self,where=where,exerset=exerset,debug=debug)

        #say to user download and compile 


    def make_c3web(self,where='.',debug=False):
        """
        Produce html files from the database based on the %summary field.

        Command line use: 
            The ``where`` input argument, when specified.

        LINKS:

        """
        html_index = C3WebExporter(self,where,debug)


    def make_moodlexml(self,where='.',debug=False):
        MoodleExporter(self, where, debug)  


    def siacuapreview(self,exname,ekeys=[]):
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

            problem = ex_instance.problem()
            answer = ex_instance.answer()
    
            #Adapt for appropriate URL for images
            #if ex_instance.image_list != []:
            #    problem = self._adjust_images_url(problem)
            #    answer = self._adjust_images_url(answer)
            #    self.send_images()
    
            #TODO: pass this to ex.py
            if ex_instance.has_multiplechoicetag:
                answer_list = self._siacua_answer_frominstance(ex_instance)
            else:
                print ex_instance.name,"has [CDATA] field. Please change to <showone> ... </showone> markers."
                answer_list = self._siacua_answer_extract(answer)

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




    def siacua(self,exname,ekeys=[],sendpost=False,course="calculo3",usernamesiacua="",grid2x2=0):
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
                    answer_list = [self._adjust_images_url(choicetxt) for choicetxt in self._siacua_answer_frominstance(ex_instance)]
                else:
                    answer_list = self._siacua_answer_frominstance(ex_instance)
            else:
                print ex_instance.name,"has [CDATA] field. Please change to <showone> ... </showone> markers."
                answer_list = self._siacua_answer_extract(answer)

            #Create images for graphics (if they exist) 
                #for problem
                #for each answer
                #collect consecutive image numbers.

            #build json string
            send_dict =  self._siacua_json(course, exname, e_number, problem, answer_list, concept_list)
            send_dict.update(dict({'usernamesiacua': usernamesiacua, 'grid2x2': grid2x2}))
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
        os.system("rm -r images")

        #While POST is working do not need this.
        #Ending _siacua_sqlprint
        #f.write(r"</body></html>")
        #f.close()
        #print r"Copy/paste of contents and send to Sr. Siacua using email. Merci."




    def send_images(self):
        """Send images to siacua: now is to put them in a drpobox public folder"""
        # AttributeError: MegBookWeb instance has no attribute 'image_list'
        #for fn in self.image_list:
        #    os.system("cp -uv images/%s.png /home/nbuser/megua_images" % fn)
        os.system("cp -ru images/*.png /home/nbuser/megua_images  > /dev/null") #TODO: check this


    def _adjust_images_url(self, input_text):
        """the url in problem() and answer() is <img src='images/filename.png'>
        Here we replace images/ by the public dropbox folder"""

        target = r"https://dl.dropboxusercontent.com/u/10518224/megua_images"
        img_pattern = re.compile(r"src='images/", re.DOTALL|re.UNICODE)

        (new_text,number) = img_pattern.subn(r"src='%s/" % target, input_text) #, count=1)
        #print "===> Replacement for %d url images." % number
        return new_text



    def _siacua_send(self, send_dict):
        params = urllib.urlencode(send_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
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

    def _siacua_answer_extract(self,answer_text):
        r"""
        Does the parsing of answer to extract options and complete answer.
        This routine applies when using moodle template with CDATA.
        """
        l = re.findall('<!\[CDATA\[(.*?)\]\]>', answer_text, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
        if len(l)<5:
            raise NameError('Missing of options in multiple choice question or full answer. At least 4 options must be given and the first must be the correct one. Also the full answer must be given.')
        return l


    def _siacua_answer_frominstance(self,ex):
        r"""
        This routine applies when using <multiplechoice>...</multiplechoice>.
        """
        #Elements must be in same order as in function "_siacua_answer_extract"
        centered_all_choices = [ "<center>"+choice+"</center>" for choice in ex.all_choices]
        l = centered_all_choices + [ex.detailed_answer] #join two lists

        if len(l)<5:
            raise NameError('Missing of options in multiple choice question or full answer. At least 4 options must be given and the first must be the correct one. Also the full answer must be given.')

        #print "==========="
        #print "For _siacua_answer:",l
        #print "=========="
        return l




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




    def c3web(self, exname, ename="e", rname="r", startnumber=1, many=10,  whatinside="E", ekey=0, edict={}, where='c3web'):
        """
        Save an exercse to aspx page.

	INPUT:

	- exname: string with exercise identification name.
	- many: how many samples (starting ekey generated key).
        - ename: filename prefix for file with exercise text.
        - rname: filename prefix for file with resolution text.
        - startnumber: number for filename.
        - whatinside: "E" for extrema, "L" for limits, whatever...
	- ekey: random values generation key.
	- edict: some values declared on make_random or solve functions of the exercise.

        EXAMPLES:

        Full use of parameters::

            sage: meg.c3web("E12A34_Aplic_DerivadasE1_002", many=10, ekey=100, edict={'a': 10})

        Less parameters::

            sage: meg.c3web("E12A34_Aplic_DerivadasE1_002", many=10 )

        NOTES:
          See C3WebExporter for saving full database.
        """

        #If does not exist create
        if not os.path.exists(where):
            os.makedirs(where)


        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        for e_number in range(many):

            #Continuous numeration of exercises
            exnr = startnumber + e_number

            #Create exercise instance
            ex_instance = exerciseinstance(row, ekey= ekey + e_number)


            #Print problem
            #Template fields:
            # {{ extitle }} Ex. Q.1
            # {{ exsmall }} Ex. L.1

            problem_html = self.problem_template.render(
                extitle = "Ex. %s. %d" % (whatinside,exnr),
                exsmall = "Ex. %s. %d" % (whatinside,exnr),
                problem = ex_instance.problem()
            )

            #ofile = open( os.path.join( self.c3web_folder, "e%02d-%02d-P%02d.aspx" % (sec_number+1,e_number+1,ekey+1) ), 'w')
            ofile = open( os.path.join( where, "%s%d.aspx" % (ename,exnr) ), 'w')
            ofile.write(problem_html.encode('latin1'))
            ofile.close()

            #Print problem and answer
            problemanswer_html = self.problemanswer_template.render(
                extitle = "Res. %s. %d" % (whatinside,exnr),
                exsmall = "Res. %s. %d" % (whatinside,exnr),
                problem = ex_instance.problem(),
                answer = ex_instance.answer()
            )

	    #ofile = open( os.path.join( self.c3web_folder, "e%02d-%02d-A%02d.aspx" % (sec_number+1,e_number+1,ekey+1) ), 'w')
            ofile = open( os.path.join(where, "%s%d.aspx"  % (rname,exnr) ), 'w')
            ofile.write(problemanswer_html.encode('latin1'))
            ofile.close()


        import subprocess
        subprocess.call("zip %s %s" % (where, where+r'/*'), shell=True)


    def moodle(self, exname, questiontype="mchoice", many=10,  ekey=0, where='.'):
        """
        Save an exercse to moodle xml file format.

	INPUT:

	- exname: string with exercise identification name.
	- questiontype: "mchoice" or "cloze"
	- many: how many samples (starting ekey generated key).
	- ekeys: random values generation key.
        - where: local folder to store data.

        EXAMPLES:

        Full use of parameters::

            sage: meg.moodle("E12A34_Aplic_DerivadasE1_002", "mchoice", many=10, ekey=100)

        Less parameters::

            sage: meg.moodle("E12A34_Aplic_DerivadasE1_002", many=10 )

        """

        #If does not exist create
        if not os.path.exists(where):
            os.makedirs(where)


        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        questions_xml = unicode('')

        for e_number in range(many):

            #Create exercise instance
            ex_instance = exerciseinstance(row, ekey= ekey + e_number)

            if questiontype=='mchoice':
                questions_xml += self.mchoice_template.render(
                    sections= m_get_sections(row['sections_text']),
		    exercisename = exname,
		    ekey = e_number,
                    problemname=row['suggestive_name'],
                    answertext = ex_instance.answer(),
                    problemtext = ex_instance.problem()
                )
            else:
                questions_xml += self.cloze_template.render(
                    sections= m_get_sections(row['sections_text']),
		    exercisename = exname,
		    ekey = e_number,
                    problemname=row['suggestive_name'],
                    answertext = ex_instance.answer(),
                    problemtext = ex_instance.problem()
                )


        # -----------------
        # output file
        # -----------------
        xmlfilename = "quiz-%s.xml" % exname
        xmlfile = codecs.open(xmlfilename, encoding='utf-8', mode='w')
        xmlfile.write('<?xml version="1.0" encoding="utf-8"?>\n<quiz>\n')
        xmlfile.write(questions_xml)
        xmlfile.write("\n</quiz>")
        xmlfile.close()


    def gallery(self,owner_keystring, ekey=None, edict=None):
        r"""Prints an exercise instance of a given type and output RST file for gallery.

        INPUT:

         - ``owner_keystring`` -- the class name.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.

        OUTPUT:
            An instance of class named ``owner_keystring`` and output RST file for gallery.

        """
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(owner_keystring)
        if not row:
            print "%s cannot be accessed on database" % owner_keystring
            return None
        #Create and print the instance
        ex_instance = exerciseinstance(row, ekey, edict)
        #generate one instance
        self.print_instance(ex_instance)
        #generate rst file

        summtxt =  ex_instance.summary()
        probtxt =  ex_instance.problem()
        answtxt =  ex_instance.answer()
        sname   =  ex_instance.name

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
                sname=sname,
                summtxt=summtxt,
                probtxt=probtxt,
                answtxt=answtxt_woCDATA,
                ekey=ex_instance.ekey)

        #Produce files for pdf and png graphics if any tikz code embed on exercise
        #Ver ex.py: now latex images are produced in ex.problem() and ex.answer()
        #html_string = self.publish_tikz(sname,html_string)


        #file with html to export (extension txt prevents html display).

        #To be viewed on browser
        #f = open(sname+'.html','w')
        #f.write(html_string.encode('latin1'))
        #f.close()
        f = codecs.open(sname+'.html', mode='w', encoding='utf-8')
        f.write(html_string)
        f.close()

        rst_string = self.template("rst_instance.rst",
                sname=sname,
                summtxt=summtxt,
                probtxt=probtxt,
                answtxt=answtxt_woCDATA,
                ekey=ex_instance.ekey)

        #Produce files for pdf and png graphics if any tikz code embed on exercise
        #Ver ex.py: now latex images are produced in ex.problem() and ex.answer()
        #html_string = self.publish_tikz(sname,html_string)

        #file with html to export (extension txt prevents html display).

        #To be viewed on browser
        #f = open(sname+'.html','w')
        #f.write(html_string.encode('latin1'))
        #f.close()
        f = codecs.open(sname+'.rst', mode='w', encoding='utf-8')
        f.write(rst_string)
        f.close()



    def amc(self,sheet_structure):
        r"""
        Generates a tex file ready to use in AMC for multiple choice 
        questions with:

        * "No one of the previous answers is correct",
        * groups or no groups of questions.

        INPUT:
        
        - `structure`: see below.

        Structure:
            Simple: no division in groups ("sections") in the final examination sheet.
            [ 
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
            ]

            Grouped: division in groups ("sections") in the final examination sheet.
            [ 
              [group_id,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
              ],
              [group_id,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
              ],
            ]


        """

        if type(sheet_structure[0]) == list:
            self.amc_grouped(sheet_structure)        
        else:
            self.amc_single(sheet_structure)
            
    def amc_grouped(self,problem_list):
        print "Not yet implemented: use only meg.amc( [exercise,ekey, exercise, ekey,... pairs] )"


    def amc_single(self,problem_list):
        r"""
        Generates a tex file ready to use in AMC for multiple choice 
        questions.
        See amc() first.

        Added options:
        * "No one of the previous answers is correct",

        INPUT:
        
        - `problem_list`: see below.

        Structure example:
            Simple: no division in groups ("sections") in the final examination sheet.
            [ 
                "E12X34_Calc_001", 10,  #specific problem key
                "E12X34_Calc_001", 20,  #specific problem key (repeat the template)
                "E12X34_Deriv_001"      #select a random key for this problem
            ]

        """

        #Build paired list (ex,ekey) adding a random ekey when
        #no key is given.
        i = 0
        n = len(problem_list)
        paired_list = []
        #print random.__module__
        rn = randomlib.randint(0,10**5) #if user did not supplied an ekey.
        while i < (n-1):
            if type(problem_list[i])==str and type(problem_list[i+1])==str: #two problems
                paired_list.append( (problem_list[i], rn) ) 
                i += 1 #advance to position i+1
            elif type(problem_list[i])==str and type(problem_list[i+1])!=str: #!= probably a number
                paired_list.append( (problem_list[i], problem_list[i+1]) )
                i += 2 #advance to position i+2, consuming the ekey
        if i < n: #add last problem 
            paired_list.append( (problem_list[i], rn) )



        #amc template without groups for each question
        allproblems_text = ''
        for (problem_name,ekey) in paired_list:

            #generate problem and answer text (choices are in the answer part)

            #Get summary, problem and answer and class_text
            row = self.megbook_store.get_classrow(problem_name)
            if not row:
                print "amc_single: %s cannot be accessed on database" % problem_name
                continue
            #Create and print the instance
            ex_instance = exerciseinstance(row, int(ekey) )

            summary =  ex_instance.summary() 
            problem = ex_instance.problem()
            answer = ex_instance.answer()
            problem_name =  ex_instance.name
    
            #Adapt for appropriate URL for images
            if ex_instance.image_list != []:
                problem = self._adjust_images_url(problem)
                answer = self._adjust_images_url(answer)
                #see siacua functions: self.send_images()


            #TODO: this lines are a copy of code in "siacua()".
            if ex_instance.has_multiplechoicetag:
                if ex_instance.image_list != []:
                    answer_list = [self._adjust_images_url(choicetxt) for choicetxt in self._siacua_answer_frominstance(ex_instance)]
                else:
                    answer_list = self._siacua_answer_frominstance(ex_instance)
            else:
                answer_list = self._siacua_answer_extract(answer)


            #TODO: os CDATA tem que ser recuperados neste ficheiro e os <choice> ja estao no campo ex.all_choices.

            #generate amc problemtext

            problem_string = self.template("amc_element.tex",
                    problem_name=problem_name,
                    problem_text=html2latex(problem),
                    correcttext=html2latex(answer_list[0]),
                    wrongtext1=html2latex(answer_list[1]),
                    wrongtext2=html2latex(answer_list[2]),
                    wrongtext3=html2latex(answer_list[3]),
                    summtxt=self._latexcommentthis(summary),
                    detailedanswer=latexcommentthis(html2latex(answer_list[4])) 
                      #expected at position 4 the full answer.
            )

            #Convert the link below to \includegraphics{images/E12A34_cilindricas_0001-fig4-10.png}
            #<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/E12A34_cilindricas_0001-fig4-10.png'></img>
            problem_string = re.subn(
                """<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/(.*?)'></img>""",
                r'\n\includegraphics{images/\1}\n', 
                problem_string, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]

            #add this to allproblems_text
            allproblems_text += problem_string


        #Make a latex file to be compiled using amc program (or pdflatex).
        latextext_string = self.template("amc_latexfile.tex",
            ungroupedamcquestions=allproblems_text
        )

        f = open('amc_test.tex','w')
        f.write(latextext_string.encode('utf8'))  #latin1  <-- another option
        f.close()

        f = open('amcpt.sty','w')
        f.write(self.template("amcpt.sty"))
        f.close()

        f = open('amc_instructions.html','w')
        f.write(self.template("amc_instructions.html").encode('utf8'))
        f.close()

        os.system("zip -r images images > /dev/null 2>&1")

        os.system("pdflatex -interact=nonstopmode {0} > /dev/null 2>&1".format("amc_test.tex"))
        os.system("rm amc_test.amc amc_test.log amc_test.aux > /dev/null 2>&1") 
        #os.system("rm -r images > /dev/null 2>&1")
    
     



    def thesis(self,problem_list):
        r"""
        Generates a tex file ready in standard LaTeX to put in a thesis.

        INPUT:
        
        - `problem_list`: see below.

        Structure example:
            Simple: no division in groups ("sections") in the final examination sheet.
            [ 
                "E12X34_Calc_001", 10,  #specific problem key
                "E12X34_Calc_001", 20,  #specific problem key (repeat the template)
                "E12X34_Deriv_001"      #select a random key for this problem
            ]

        """

        #Build paired list (ex,ekey) adding a random ekey when
        #no key is given.
        i = 0
        n = len(problem_list)

        for j in range(n):
            #if problem_list[i] is unicode convert to str 
            #for the next ifs
            if type(problem_list[j])==unicode:
                problem_list[j] = str(problem_list[j])

        paired_list = []
        #print random.__module__
        rn = randomlib.randint(0,10**5) #if user did not supplied an ekey.
        while i < (n-1):

            if type(problem_list[i])==str and type(problem_list[i+1])==str: #two problems
                paired_list.append( (problem_list[i], rn) ) 
                i += 1 #advance to position i+1
            elif type(problem_list[i])==str and type(problem_list[i+1])!=str: #!= probably a number
                paired_list.append( (problem_list[i], problem_list[i+1]) )
                i += 2 #advance to position i+2, consuming the ekey
        if i < n: #add last problem 
            paired_list.append( (problem_list[i], rn) )



        #amc template without groups for each question
        allproblems_text = ''
        for (problem_name,ekey) in paired_list:

            print "Generating sample of",problem_name

            #print "Write",(problem_name,ekey),"in thesis."

            #generate problem and answer text (choices are in the answer part)

            #Get summary, problem and answer and class_text
            row = self.megbook_store.get_classrow(problem_name)
            if not row:
                print "meg.thesis(): %s cannot be accessed on database" % problem_name
                continue
            #Create and print the instance
            ex_instance = exerciseinstance(row, int(ekey) )

            summary =  ex_instance.summary() 
            problem = ex_instance.problem()
            answer = ex_instance.answer()
            problem_name =  ex_instance.name
    
            #Adapt for appropriate URL for images
            if ex_instance.image_list != []:
                problem = self._adjust_images_url(problem)
                answer = self._adjust_images_url(answer)
                #see siacua functions: self.send_images()



            #TODO: this lines are a copy of code in "siacua()".
            if ex_instance.has_multiplechoicetag:
                if ex_instance.image_list != []:
                    answer_list = [self._adjust_images_url(choicetxt) for choicetxt in self._siacua_answer_frominstance(ex_instance)]
                else:
                    answer_list = self._siacua_answer_frominstance(ex_instance)
            else:
                answer_list = self._siacua_answer_extract(answer)


            #TODO: os CDATA tem que ser recuperados neste ficheiro e os <choice> ja estao no campo ex.all_choices.

            #generate amc problemtext

            problem_string = self.template("thesis_problem.tex",
                    problem_name=problem_name,
                    slashedproblem_name=latexunderscore(problem_name),
                    problem_text=html2latex(problem),
                    correcttext=equation2display( html2latex(answer_list[0]) ),
                    wrongtext1=equation2display( html2latex(answer_list[1]) ),
                    wrongtext2=equation2display( html2latex(answer_list[2]) ),
                    wrongtext3=equation2display( html2latex(answer_list[3]) ),
                    summtxt=latexcommentthis(summary),
                    detailedanswer=html2latex(answer_list[4]) 
                      #expected at position 4 the full answer.
            )

            #Convert the link below to \includegraphics{images/E12A34_cilindricas_0001-fig4-10.png}
            #<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/E12A34_cilindricas_0001-fig4-10.png'></img>
            problem_string = re.subn(
                """<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/(.*?)'></img>""",
                r'\n\\begin{center}\n\includegraphics[width=8cm]{images/\1}\n\end{center}\n', 
                problem_string, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]

            #add this to allproblems_text
            allproblems_text += problem_string


        os.system("zip -r images images > /dev/null 2>&1")


        #Apply to all "allproblems_text"
        
        r"""2. Convert
                \questao{ 
    
                 $\displaystyle 7.95$ 
                 }
            to 
                \questao{$\displaystyle 7.95$}
            but it does not work right with
                \questao{ 
 
                    \begin{center}
                    \includegraphics[width=8cm]{images/E97k40_grafico_tabela_001-fig1-9.png}
                    \end{center}
 
                 }
        """

        pos = 0
        new_allproblems_text = ''  #below pattern is not perfect because last } could match \begin{center} <-- this }
        for m in re.finditer(r'\\questao\{(.*?)\}', allproblems_text, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE):
            inside = m.group(1)
            inside,nc = re.subn("\n","",inside,re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
            new_allproblems_text += allproblems_text[pos:m.start(1)] + inside  
            pos = m.end(1)

        new_allproblems_text += allproblems_text[pos:]

        #Produce "Source Code" from each problem.
        PDFLaTeXExporter(self,where='.',exerset=paired_list,debug=False)
        f = codecs.open( "megua_ex.tex", encoding='latin1', mode='r') 
        #f = open("megua_ex.tex","r")
        source_code = f.read()
        #print "type=",type(source_code)
        f.close()

        #Make a latex file to be compiled using amc program (or pdflatex).
        latextext_string = self.template("thesis_latexfile.tex",
            ungroupedquestions=new_allproblems_text,
            sourcecode=source_code
        )


        f = open('thesis_problems.tex','w')
        f.write(latextext_string.encode('latin1')) #utf8 #latin1  <-- another option
        f.close()

        #os.system("pdflatex -interact=nonstopmode {0} > /dev/null 2>&1".format("thesis_problems.tex"))
        #os.system("rm thesis_problems.log thesis_problems.aux > /dev/null 2>&1") 
        #os.system("rm -r images > /dev/null 2>&1")


        print '\nInstrucoes:\n1. Use o botao direito e "Save link as..." para guardar "thesis_problems.tex" no seu computador.'
        print '2. Se houver imagens, o conteudo do ficheiro "images.zip" deve ser colocado numa pasta "images".'
        print '3. Sera necessaria paciencia para finalizar a pre conversao de HTML para LaTeX em cada exercicio.'
        print '4. Recomenda-se adaptar um exercicio de cada vez compilado um por um.'
    



def latexcommentthis(txt):
    """Put % signs in each line"""
    txt += '\n' #assure last line has "\n"
    tlist = re.findall('(.*?)\n', txt, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
    return '\n'.join( [ '%'+t for t in tlist] ) + '\n'
        


def latexunderscore(txt):
    """Put \_  in each underscore"""
    return re.subn("_","\_",txt)[0]

def equation2display(txt):
    """Put \displaystyle\$  in each $$"""
    return re.subn(r"\$\$(.*?)\$\$",r"$\displaystyle \1$",txt, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]
        



def html2latex(htmltext):
    r"""
    Replace:

    * \n\n\n by \n\n (reduce to much blank lines);
    * <p> by \n\n; </p> by empty string;
    * <center> by \n\n; </center> by empty string;
    """

    #No groups, direct replacements
    lr = [  (ur'(\d)%', ur'\1\%'),  # 3% --> 3\%
            (ur'(\d) %', ur'\1\%'),  # 3 % --> 3\%
            (ur'<br>', '\n\n'),
            (ur'<p>', '\n\n'),
            (ur'</p>', '\n'),
            (ur'<ul>', ur'\\begin{itemize}'),
            (ur'</ul>', ur'\\end{itemize}'),
            (ur'<ol>', ur'\\begin{enumerate}'),
            (ur'</ol>', ur'\\end{enumerate}'),
            (ur'<li>', ur'\\item '),    
            (ur'</li>', '\n\n'),    
            (ur'<center>', '\n\n'),
            (ur'</center>', '\n'),
            (ur'<style>(.*?)</style>', '\n'),
            (ur'<pre>(.*?)</pre>',ur'\n%Falta colocar linhas vazias em baixo\n\\begin{alltt}\n\1\n\\end{alltt}\n\n'), 
        ]

    newtext = htmltext
    for pr in lr:
        (newtext, nr) = re.subn(pr[0], pr[1], newtext, count=0, flags=re.DOTALL|re.UNICODE)

    #Convert from <table> to \begin{tabular}
    newtext = table2tabular(newtext)
    

    #Removing spaces and lots of blank lines.
    nr = 1
    while nr >= 1:
        (newtext, nr) = re.subn('\n\n\n', '\n\n', newtext, count=0, flags=re.UNICODE)
        #print "html2latex():", nr

    return newtext


def table2tabular(text):
    r"""Convert <table>...</table> to \begin{tabular} ... \end{tabular}"""

    lista = [
            (ur'<table(.*?)>', ur'\n\n\\begin{tabular}{...}\n'),
            (ur'</table>', ur'\n\end{tabular}\n'),
            (ur'<tr(.*?)>', ur'\n'),
            (ur'</tr>', ur' \\\\ \hline\n'), 
            (ur'<td(.*?)>', ' '),
            (ur'</td>', ' & '),
        ]

    newtext = text
    for pr in lista:
        (newtext, nr) = re.subn(pr[0], pr[1], newtext, count=0, flags=re.DOTALL|re.UNICODE)
    
    return newtext



def m_get_sections(sectionstxt):
    """

    LINKS::

       http://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python?rq=1
    """   
    s = "megua/"+sectionstxt.replace("; ","/") #case "; " by "/"
    return s.replace(";","/") #possible case without space: ";" by "/"



#end class MegBookWeb

