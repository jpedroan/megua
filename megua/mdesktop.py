import os
import codecs
import subprocess

from megua.platex import pcompile
from megua.jinjatemplates import templates
from megua.megoptions import *

def desktop_exlatex_print_instance(self):
    """
    After producing an exercise template or requesting a new instance of some exercise
    this routine will print it on notebook notebook or command line mode. It also should
    give a file were the user can find text markup (latex or html, etc).
    """

    #Use jinja2 template to generate LaTeX.
    latex_string = self._latex_string()

    pcompile(latex_string,self.wd_fullpath,self.unique_name())

    EXERCISE_TEX_PATHNAME = os.path.join(self.wd_fullpath, self.unique_name()+'.tex')
    EXERCISE_PDF_PATHNAME = os.path.join(self.wd_fullpath, self.unique_name()+'.pdf')

    print ("exlatex module say: evince ",EXERCISE_PDF_PATHNAME)
    subprocess.Popen(["evince",EXERCISE_PDF_PATHNAME])

def desktop_exsiacua_print_instance(self):
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

    print("Exsicua module say: firefox ",EXERCISE_HTML_PATHNAME)
    subprocess.Popen(["firefox","-new-tab", EXERCISE_HTML_PATHNAME])

def desktop_examc_print_instance(self):
    """
    After producing an exercise template or requesting a new instance of some exercise
    this routine will print it on notebook notebook or command line mode. It also should
    give a file were the user can find text markup (latex or html, etc).
    """

    #Use jinja2 template to generate LaTeX.
    latex_string = templates.render("examc_print_instance.tex",
        unique_name=self.unique_name(),
        ekey = self.ekey,
        summtxt=self.summary(),
        probtxt=self.problem(),
        answtxt=self.answer(),
        )

    #copy amc.sty to the working dir:
    shutil.copy(os.path.join(MEGUA_TEMPLATE_DIR,"amcpt.sty"), self.wd_fullpath)
    
    pcompile(latex_string,self.wd_fullpath,self.unique_name())

    EXERCISE_TEX_PATHNAME = os.path.join(self.wd_fullpath, self.unique_name()+'.tex')
    EXERCISE_PDF_PATHNAME = os.path.join(self.wd_fullpath, self.unique_name()+'.pdf')

    print("ex_amc.py module say: evince ",EXERCISE_PDF_PATHNAME)
    subprocess.Popen(["evince",EXERCISE_PDF_PATHNAME])