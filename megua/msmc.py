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
            self._current_unique_name,
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

def conf_exlatex_print_instance(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    salvus.file(EXERCISE_PDF_PATHNAME,show=True,raw=True); 
    print("\n")
    salvus.file(EXERCISE_TEX_PATHNAME,show=True,raw=True); 
    print("\n")
    salvus.open_tab(EXERCISE_PDF_PATHNAME)


def conf_exsiacua_print_instance(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    salvus.html(html_string)

def conf_examc_print_instance(self):
    sys.path.append('/cocalc/lib/python2.7/site-packages')
    from smc_sagews.sage_salvus import salvus
    salvus.file(EXERCISE_PDF_PATHNAME,show=True,raw=True); 
    print("\n")
    salvus.file(EXERCISE_TEX_PATHNAME,show=True,raw=True); 
    print("\n")
    salvus.open_tab(EXERCISE_PDF_PATHNAME)