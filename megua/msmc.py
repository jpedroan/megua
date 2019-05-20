import os
import sys
import codecs

from megua.exbase import ExerciseBase
from megua.jinjatemplates import templates
from megua.platex import html2latex, pcompile
from megua.megoptions import *

def conf__siacua_send(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    salvus.html("<a href='%s'>%s</a><br/>" %  (content.headers['Location'],  content.headers['Location']))

def conf_siacuapreview(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    #print "exsiacua.py: using salvus.link:"
    html_relative_path = os.path.join(self.wd_relative,self.unique_name()+'_siacuapreview.html')
    salvus.file(html_relative_path,raw=True)

def conf_set_current_exercise(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    salvus.html("<h4>{}&nbsp;&nbsp;{}</h4><p>{}</p>".format(
            unique_name,
            "(The dog picture has been stolen. Reward of $100000, dead or alive.)",
            #DOGSVG, #'<img src="https://cloud.sagemath.com/4531e156-82ac-4387-8f19-b066e940b28b/raw/stationary/small_megua_dog.png"/>',
            '<a href="https://github.com/jpedroan/megua/wiki" target=_blank>MEGUA wiki for help</a> or email to dmat-siacua@ua.pt.'
        ))

def conf_new_exercise(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    if salvus:
        print("Worksheet")
        salvus.file(fullpath,show=True,raw=True); 
        print("\n")
        salvus.open_tab(fullpath)
    else:
        print("Command line")
        sys.path.append('/usr/local/lib/python2.7/dist-packages')
        from smc_pyutil import smc_open
        smc_open.process([fullpath])                

def conf_replicate_exercise(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    if salvus:
        #salvus.file(fullpath_new,show=True,raw=True); print "\n"
        print(fullpath_new)
        print("salvus.open_tab(fullpath_new)")
    else:
        sys.path.append('/usr/local/lib/python2.7/dist-packages')
        from smc_pyutil import smc_open
        smc_open.process([fullpath_new])

def conf_catalog(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    if salvus:
        salvus.file(CATALOG_PDF_PATHNAME,show=True,raw=True); 
        print("\n")
        salvus.file(CATALOG_TEX_PATHNAME,show=True,raw=True); 
        print("\n")
        salvus.open_tab(CATALOG_PDF_PATHNAME)
    else:
        sys.path.append('/usr/local/lib/python2.7/dist-packages')
        from smc_pyutil import smc_open
        smc_open.process([CATALOG_PDF_PATHNAME])

def conf_latex_document(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    if salvus:
        salvus.file(DOC_PDF_PATHNAME,show=True,raw=True); 
        print("\n")
        salvus.file(DOC_LATEX_PATHNAME,show=True,raw=True); 
        print("\n")
        salvus.open_tab(DOC_PDF_PATHNAME)
    else:
        sys.path.append('/usr/local/lib/python2.7/dist-packages')
        from smc_pyutil import smc_open
        smc_open.process([DOC_PDF_PATHNAME])

def conf_fast_exam_siacu(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    if salvus:
        print("Check exam PDF file:")
        salvus.file(EXAM_PDF_PATHNAME,show=True,raw=True);
        print ("\n")
        print("Save tex file to your computer to improve the text at",EXAM_TEX_PATHNAME)
        salvus.file(EXAM_TEX_PATHNAME,show=True,raw=True);
        print ("\n")
        salvus.open_tab(EXAM_TEX_PATHNAME)
    else:
        sys.path.append('/usr/local/lib/python2.7/dist-packages')
        from smc_pyutil import smc_open
        smc_open.process([EXAM_TEX_PATHNAME])

def exlatex_print_instance(self):
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

    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    salvus.file(EXERCISE_PDF_PATHNAME,show=True,raw=True); 
    print("\n")
    salvus.file(EXERCISE_TEX_PATHNAME,show=True,raw=True);
    print("\n")
    salvus.open_tab(EXERCISE_PDF_PATHNAME)

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

    #print html_string

    EXERCISE_HTML_PATHNAME = os.path.join(self.wd_fullpath,uname+'.html')
    f = codecs.open(EXERCISE_HTML_PATHNAME, mode='w', encoding='utf-8')
    f.write(html_string)
    f.close()

    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    salvus.html(html_string)

def examc_print_instance(self):
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

    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    salvus.file(EXERCISE_PDF_PATHNAME,show=True,raw=True);
    print("\n")
    salvus.file(EXERCISE_TEX_PATHNAME,show=True,raw=True);
    print("\n")
    salvus.open_tab(EXERCISE_PDF_PATHNAME)