import os
import codecs
import subprocess

from megua.platex import pcompile
from megua.jinjatemplates import templates
from megua.megoptions import *

def conf__siacua_send(self):
    print("conf__siacua_send")

def conf_siacuapreview(self):
    import webbrowser
    url = os.path.join(self.wd_fullpath,self.unique_name()+'_siacuapreview.html')
    webbrowser.open(url)

def conf_set_current_exercise(self):
    print("windows_conf_set_current_exercise")
    
def conf_new_exercise(self):
    print("windows_conf_new_exercise")
    
def conf_replicate_exercise(self):
    print("windows_conf_replicate_exercise")
    
def conf_catalog(self):
    print("windows_conf_catalog")
    
def conf_latex_document(self):
    print("windows_conf_latex_document")
    
def conf_fast_exam_siacu(self):
    print("windows_conf_fast_exam_siacu")

def exlatex_print_instance(self):
    print("windows_exlatex_print_instance")

def exsiacua_print_instance(self):
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
    EXERCISE_HTML_PATHNAME = os.path.join(self.wd_fullpath,uname+'.html')
    f = codecs.open(EXERCISE_HTML_PATHNAME, mode='w', encoding='utf-8')
    f.write(html_string)
    f.close()


    from IPython.display import display, Markdown
    display(Markdown(html_string))

def examc_print_instance(self):
    print("windows_examc_print_instance")