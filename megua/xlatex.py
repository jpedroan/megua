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

            row = self.megbook_store.get_classrow(e) #e is exer name (same as owner_keystring)
            etxt = self.exercise_template.render(
                    problem_name=row['owner_key'],
                    slashedproblem_name=latexunderscore(row['owner_key']),
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
        


