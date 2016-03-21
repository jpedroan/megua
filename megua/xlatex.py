# -*- coding: utf-8 -*-

r"""
xlatex.py -- export to pdflatex.

AUTHORS:

- Pedro Cruz (2014-10): initial version

TODO:
- break long lines to fit 80 chars in verbatim environment
- trim to much blank lines (only one for each)

NOTES:
- first version based on xsphinx.py module of megua

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  
  #megua modules:
from megbookbase import *
from platex import pcompile



#TODO: remover se não for precis
#from xsws import SWSExporter
#from xlatex import html2latex,latexcommentthis
#from xsphinx import SphinxExporter

#TODO: remover se não for precis
#from sage.all import *


#Sage modules:
#Check if sage.all includes this:
#from sage.misc.latex import JSMath, Latex, _run_latex_, _latex_file_
from sage.misc.latex import Latex, _run_latex_, _latex_file_

#TODO: rmove se não for preciso
from sage.misc.html import html

#Python modules:
#import sqlite3 #for row objects as result from localstore.py
#import shutil
#import os
#import StringIO
#from random import sample,randint
#import codecs



#python package
import os
import shutil
import codecs
import jinja2
from string import join
import re
import textwrap
import unicodedata

#megua package
from localstore import ExIter
from csection import SectionClassifier, Section

class PDFLaTeXExporter:
    """
    Produce LaTeX code files from the database and an index reading first line of the %summary field.

    """

    def __init__(self,megbook,where=".",exerset=None,debug=False):
        r"""

        INPUT:
        - ``megbook`` - 
        - ``where`      
        - ``exerset``
        
      
        #save megstore reference
        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store


        """

        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store
        self.xlatex_folder = where

        #Filter exerset to remove integers
        self.exerset = [c[0] for c in exerset]

        #for c in exerset:
        #    print type(c)
        #    if type(c)==str:
        #        self.exerset.append( c )

        #print "List of exercises:",self.exerset

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.exercise_template = self.megbook.env.get_template("xlatex_exercise.tex")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template xlatex_exercise.tex"
            raise e


        #Open file 
        #self.ofile = open( os.path.join(where,'megua_ex.tex'), 'w') 
        self.ofile = open( 'megua_ex.tex', 'w') 
        #self.ofile = codecs.open( os.path.join( self.xlatex_folder, "megua_ex.tex" ), encoding='utf-8', mode='w+')
        #self.ofile = codecs.open( "megua_ex.tex", encoding='utf-8', mode='w+') 
        #now see thesis_latexfile.texself.ofile.write(self.main_template.render().encode('latin1'))

        #Open pdflatex template

        #Create tree structure
        self.sc = SectionClassifier(self.megbook_store,exerset=self.exerset)
        
        #Save to files and build html.
        self._save_to_file()

        self.ofile.close()


    def _save_to_file(self):

        #Create index.rst from xsphinx_index.rst template.
        for sec_number,sec_name in enumerate(self.sc.contents):

            #Get Section with sec_name (see class Section from csection.py)
            section = self.sc.contents[sec_name]

            #Write 
            self.sec_print(section)

  

    def sec_print(self, section):

        if section.level==0: # \section
            self.ofile.write(r'\section{%s}' % section.sec_name.encode("latin1") + "\n\n")
        elif section.level==1: # \subsection
            self.ofile.write(r'\subsection{%s}' % section.sec_name.encode("latin1") + "\n\n")
        elif section.level==2: # \subsubsection
            self.ofile.write(r'\subsubsection{%s}' % section.sec_name.encode("latin1") + "\n\n")
        elif section.level==3: # \subsubsubsection
            self.ofile.write(r'\subsubsubsection{%s}' % section.sec_name.encode("latin1") + "\n\n")
        else: # it will just bold
            self.ofile.write(r'\textbf{%s}' % section.sec_name.encode("latin1") + "\n\n")


        for e in section.exercises:

            row = self.megbook_store.get_classrow(e) #e is exer name (same as unique_namestring)
            etxt = self.exercise_template.render(
                    problem_name=row['unique_name'],
                    slashedproblem_name=latexunderscore(row['unique_name']),
                    summary=textwrap.fill( perc_str_indent(row['summary_text']), 80,replace_whitespace=False).strip(),
                    problem=textwrap.fill( str_indent(row['problem_text']), 80,replace_whitespace=False).strip(),
                    answer=textwrap.fill( str_indent(row['answer_text']), 80,replace_whitespace=False).strip(),
                    sage_python=remove_accents(str_indent( row['class_text'] )).strip(),
                    sections_text = row["sections_text"],
                    suggestive_name= row["suggestive_name"]
            )

            self.ofile.write(etxt.encode("latin1"))
            self.ofile.write("\n\n")

        for subsection in section.subsections.itervalues():
            self.sec_print(subsection)


def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii



def latexunderscore(txt):
    """Put \_  in each underscore"""
    return re.subn("_","\_",txt)[0]

def str_indent(s):
    return "   " + s.replace("\n","\n   ")

def perc_str_indent(s):
    return "   " + s.replace("\n","\n   ")

def lang_set(s):
    if s == 'pt_pt':
        return 'pt_br'
    else:
        return s





    def put_here(self,unique_namestring, ekey=None, edict=None, elabel="NoLabel", em=True):
        r"""
        Create an instance based on a template with key=unique_namestring.
        This routine is used on templates only.

        INPUT:

        - ``unique_namestring`` -- the exercise key.
        - ``ekey`` -- random seed.
        - ``edict`` -- dictionary to be used after random initialization of ex parameters.
        - ``elabel`` -- to be used for "\label" or "\ref" in LaTeX.
        - ``automc`` -- automatic multiple choice (chooses possibilities and prints them) (true ou false).

        OUTPUT:
            text string.

        NOTES: to be used with `template_create`.

        """

        #Get summary, problem and answer and class_text
        #Field row['class_text'] is needed to render the template. See below.
        row = self.megbook_store.get_classrow(unique_namestring)        
        if not row:
            #TODO: passar a raise Error
            print "%s cannot be accessed on database" % unique_namestring
            return "%s cannot be accessed on database" % unique_namestring

        #Get summary, problem and answer and class_text
        ex_instance = exerciseinstance(row,ekey,edict)

        problem = ex_instance.problem(removemultitag=True)
        answer  = ex_instance.answer(removemultitag=True)


        #print "?================================"
        #print "ex_instance.has_multiplechoicetag"
        #print ex_instance.has_multiplechoicetag
        #print "?================================"

        if ex_instance.has_multiplechoicetag and em:
            
            """
               * cada exercicio E.M. pode ter mais que 4 opcoes: como fazer para selecionar ?
                    * igual ao siacua: tirar 3 a sorte, das erradas (que podem ser so tres)
                    * baralhar as opcoes
            """
            #create options and shuffle
            wrong_options_len = len(ex_instance.all_choices)-1
            wrong_options_set = sample(xrange(wrong_options_len),3)
            options_list = [ to_unicode(ex_instance.all_choices[i+1]) for i in wrong_options_set ]

            pos = randint(0,3)  
            options_list.insert( pos, ex_instance.all_choices[0] )

            utxt = self.template("em_question_template.tex",
                exname=unique_namestring,
                ekey=ekey,
                problem  = to_unicode( problem ), 
                option1  = options_list[0],
                comment1 = "wrong option:" if pos!=0 else "correct option:",
                option2  = options_list[1],
                comment2 = "wrong option:" if pos!=1 else "correct option:",
                option3  = options_list[2],
                comment3 = "wrong option:" if pos!=2 else "correct option:",
                option4  = options_list[3],
                comment4 = "wrong option:" if pos!=3 else "correct option:",
                answer   =  to_unicode( ex_instance.detailed_answer ),
            )            


        else:
            #See template_create for template_row definition.
            utxt = self.template_row.render(
                exname=unique_namestring,
                summary = to_unicode( ex_instance.summary() ), 
                problemtemplate = to_unicode( ex_instance._problem_text ), 
                answertemplate  = to_unicode( ex_instance._answer_text ), 
                codetxt =  to_unicode( row['class_text'] ), 
                problem =  to_unicode( problem ), 
                answer  =  to_unicode( answer ),
                elabel  =  elabel,
                ekey = ekey
                )

        return utxt


    def template_fromstring(self,templatestring, ekey=None, rowtemplate=None,filename=None):
        #Kept for compatibilty. See latex_document() below.
        self.latex_document(latexdocument=templatestring, exercisetemplate=rowtemplate, ofilename=filename, ekey=ekey)


    r""" Keep this until proven not needed.
    def template_fromfile(self,templefilename, ekey=None, rowtemplate=None):

        #Get template file and make a jinja2 template
        #NOTE: cannot use DATA variable.
        tfile = open(templefilename,'r')
        utxt = unicode(tfile.read(),'utf-8')
        tfile.close()
        template = jinja2.Template(utxt)

        #Create a new file for output on same folder of templefilename
        bname_ext = os.path.basename(templefilename)
        bname,ext_name = os.path.splitext(bname_ext)
        head,tail = os.path.split(templefilename)
        ofilename = os.path.join(head,bname+'_out.tex')

        self.template_create(ofilename, template, ekey, rowtemplate)
    """


    def latex_document(self, latexdocument, exercisetemplate=None, ofilename=None, ekey=None):
        r"""
        Create LaTeX documents. Exercises are obtained with  `{{ put_here(...) }}` commands.

        INPUT:

        - ``latexdocument``: (string) contains the LaTeX to be compiled. Each exercise is obtained from database with `{{ put_here(...) }}` commands.

        - ``exercisetemplate``: (string) defines how and what is to be shown from each exercise.

        - ``ofilename``: (string) output filename (some .tex filename)

        - ``ekey``: if `{{ put_here(...) }}`` commands do not mention ekey then generate ekeys setting this. 

        EXAMPLE:

            sage: ltdoc = r'''\documentclass{article} ....  {{ put_here("E12X34_soma_001",10) }} ....'''
            sage: meg.latex_document(ltdoc)

        NOTES:
        
            - Another possibility: {{ put_here("E65D05_forwarddifference_001",ekey=10,meg.SUMMARY|meg.PROBLEM|meg.ANSWER|meg.CODE) }}

            - http://jinja.pocoo.org/docs/templates/#assignments

        """


        #Get unicode and make a jinja2 template
        utxt = unicode(latexdocument,'utf-8')
        template = jinja2.Template(utxt)

        #Create a new file for output
        if not ofilename:
            ofilename = os.path.join(SAGE_TMP,'modelo_out.tex')

        #Set seed
        if ekey:
            ur.set_seed(ekey)

        #Render output using the given template for each exercise.
        if exercisetemplate is None:
            try:
                self.template_row = self.env.get_template("row_template.tex")
            except jinja2.exceptions.TemplateNotFound:
                return "MegUA -- missing template %s"%filename
        else:
            #Check or convert rowtemplate to unicode
            try:
                self.rowtemplate = unicode(exercisetemplate,'utf-8')
            except TypeError:
                self.rowtemplate = exercisetemplate
            self.template_row = jinja2.Template(exercisetemplate)


        #Create a latex string s ready to compile.
        s = template.render(put_here=self.put_here)

        #Create new file and save string s.
        fp = open(ofilename,'w')
        fp.write( s.encode('utf-8') )
        res = fp.close()


        if is_notebook():

            # ---------
            # Notebook.
            # ---------
    
            #TODO: converter ao platex !

            #Create filename for 
            (base, filename) = os.path.split(ofilename)

            filename = os.path.splitext(filename)[0]  # get rid of extension
            if len(filename.split()) > 1:
                raise ValueError, "filename must contain no spaces"
            #redirect=' 2>/dev/null 1>/dev/null '

            #Compile
            if self.latex_debug:
                lt = 'cd "%s" && sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex}' % (base, 'pdflatex', filename)
            else:
                lt = 'cd "%s"&& sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex} 2>/dev/null 1>/dev/null' % (base, 'pdflatex', filename)

            #lt = 'cd "%s"&& sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex} '%(base, 'pdflatex', filename)
            os.system(lt)

            #Show in output cell
            bname,ext_name = os.path.splitext(filename)
            shutil.move(ofilename,'.') #move tex file
            shutil.move(os.path.join(base,bname+'.pdf'),'.')

        else:

            # -------------
            # Command line.
            # -------------

            print "Compile using:   pdflatex %s" % ofilename
            os.system("pdflatex %s" % ofilename)
            #What for: shutil.copy(ofilename,'.')



    def template_class_question(self,students, questions, ofilename, file_header, student_template, includeanswer=False,ekey_start=0):
        r"""
        Create several exercises for each student.

        INPUT::
    
        - ``students`` -- number of students OR list of students in form `[ ['name1', 'number'], ['name2', 'number'] ]`.
        - ``questions`` -- list of exercises names (questions).
        - ``ofilename`` -- latex output file.
        - ``file_header`` -- global latex file header.
        - ``student_template`` -- each student latex header.
        - ``ekey_start`` -- number to add to each student number (will be the exercise key).


        IMPLEMENTATIONS NOTES:

        2. See template_create() for details about use of unicode and latin1.

        """

        #TODO: improve this function to use jinja2 templates.
        #TODO: converter ao platex, etc

        #Create new file from jinja2 template  
        fp = open(ofilename,'w')

        print "Output file: ", ofilename

        fp.write( file_header )
        fp.write( '\\begin{document}\n')


        #In case there is no list of students. Only number of them.
        if type(students)!=list:
            students = [ ['', str(nm+1)] for nm in range(students) ]

        #Write questions
        for (snum,s) in enumerate(students):

            #prepare student header with his name and number
            student_Template = jinja2.Template(student_template)
            try:
                sn = unicode(s[0],'latin1')
            except TypeError:
                sn = s[0]

            student_header = student_Template.render(sname=sn, snumber=s[1] )
            fp.write( student_header.encode('utf-8') )

            #prepare this student questions
            for (qnum, qpossible) in enumerate(questions):

                #print type(qpossible),qpossible

                if type(qpossible)==list:
                    #use snum to produce exercise choice from the list in qpossible.
                    #[i % 6 for i in range(35)]
                    l = len(qpossible)
                    qname = qpossible[snum % l]
                else:
                    qname = qpossible

                ex = self._classquestion_exercise(qname, ekey=ekey_start+snum)
                
                #aqui
                if includeanswer:
                    txt = u"\n\n\\noindent\\textbf{{ {qnumber} }}~{problem}\nResolu\c c\~ao:\n{answer}\n\\vspace{{1cm}}".format(\
                        qnumber=qnum+1, \
                        problem=ex.problem(), \
                        answer=ex.answer() \
                    )
                else:
                    txt = u"\n\n\\noindent\\textbf{{ {qnumber} }}~{problem}\n".format(qnumber=qnum+1,problem=ex.problem() )

                #fp.write(txt.encode('latin-1'))
                fp.write(txt.encode('utf-8'))

            #new page
            fp.write( '\\newpage' )



        #Write questions and answers
        fp.write( '\\end{document}\n')    
        fp.close()


        base, filename = os.path.split(ofilename)
        filename = os.path.splitext(filename)[0]  # get rid of extension
        if len(filename.split()) > 1:
            raise ValueError, "filename must contain no spaces"
        #redirect=' 2>/dev/null 1>/dev/null '
        lt =u'cd "%s"&& sage-native-execute %s \\\\nonstopmode \\\\input{%s.tex} '%(base, 'pdflatex', filename)
        os.system(lt)
        bname,ext_name = os.path.splitext(filename)


    def _classquestion_exercise(self,unique_name, ekey=None):
        r"""
        Create an instance based on a template with key=unique_name

        Ecxceptions list::

            http://docs.python.org/2/library/exceptions.html
        """
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(unique_name)
        if not row:
            raise NameError("'%s' cannot be accessed on database '%s'" % (unique_name,self.local_store_filename))

        return exerciseinstance(row,ekey=ekey)




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
                    answer_list = [self._adjust_images_url(choicetxt) for choicetxt in ex_instance.collect_options_and_answer()]
                else:
                    answer_list = ex_instance.collect_options_and_answer()
            else:
                answer_list = ex_instance.answer_extract_options()


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
    


# REMOVE
#
#    def to_latex(self,problem_name):
#        r"""
#        Generates a tex file ready in standard LaTeX to put in a thesis.
#
#        INPUT:
#        
#        - `problem_name`: problem name.
#
#        #TODO: os CDATA tem que ser recuperados neste ficheiro e os <choice> ja estao no campo ex.all_choices.
#        """
#
#        ofile = codecs.open(exercise_latex.html, mode='w', encoding='utf-8')
#
#        #amc template without groups for each question
#        exercise_text = u'<html>\n<body>\n\n'
#        exercise_text += u'meg.save(r"""\n'
#
#        #Get summary, problem and answer and class_text
#        row = self.megbook_store.get_classrow(problem_name)
#        if not row:
#            print "meg.to_latex(): %s cannot be accessed on database" % problem_name
#            return
#
#
#
#        exercise_text += u'""")\n'
#        exercise_text += u'</body>\n</html>\n'
#
#        ofile.write(html_string)
#        ofile.close()
#
#


def m_get_sections(sectionstxt):
    """

    LINKS::

       http://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python?rq=1
    """   
    s = "megua/"+sectionstxt.replace("; ","/") #case "; " by "/"
    return s.replace(";","/") #possible case without space: ";" by "/"

