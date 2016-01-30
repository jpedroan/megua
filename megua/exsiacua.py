# -*- coding: utf-8 -*-

r"""
ExSiacua -- build exercises for siacua.

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
  
from exbase import *


class ExSiacua(ExerciseBase):    
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
       ... class E28E28_pdirect_001(ExSiacua):
       ... 
       ...     def make_random(self,edict):
       ...         self.ap = ZZ.random_element(-4,4)
       ...         self.bp = self.ap + QQ.random_element(1,4)
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
