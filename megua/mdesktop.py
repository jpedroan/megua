import os
import codecs
import subprocess

from megua.platex import pcompile
from megua.jinjatemplates import templates
from megua.megoptions import *

def conf__siacua_send(self, content):
    print("ExSicua module say: firefox ",content.headers['Location'])
    subprocess.Popen(["firefox","-new-tab", content.headers['Location']])

def conf_siacuapreview(self, html_full_path):
    print("exsiacua.py: opening firefox ",html_full_path,"in the browser and press F5.")
    subprocess.Popen(["firefox","-new-tab", html_full_path])

def conf_set_current_exercise(self):
    print("Exercise {}".format(self._current_unique_name))

def conf_new_exercise(self, fullpath):
    print("MegBook module say: gvim ",fullpath)
    subprocess.Popen(["gvim",fullpath])

def conf_replicate_exercise(self, fullpath, fullpath_new):
    print("MegBook module say: gvim ",fullpath)
    subprocess.Popen(["gvim",fullpath])

def conf_catalog(self, CATALOG_PDF_PATHNAME, CATALOG_TEX_PATHNAME):
    print("MegBook module say: evince ",CATALOG_PDF_PATHNAME)
    subprocess.Popen(["evince",CATALOG_PDF_PATHNAME])

def conf_latex_document(self, DOC_PDF_PATHNAME, DOC_LATEX_PATHNAME):
    print("MegBook module say: evince ",DOC_PDF_PATHNAME)
    subprocess.Popen(["evince",DOC_PDF_PATHNAME])

def conf_fast_exam_siacua(self, EXAM_PDF_PATHNAME, EXAM_TEX_PATHNAME):
    print("MegBook module say: evince ",EXAM_PDF_PATHNAME)
    subprocess.Popen(["evince",EXAM_PDF_PATHNAME])

def conf_exlatex_print_instance(self, EXERCISE_TEX_PATHNAME, EXERCISE_PDF_PATHNAME):
    print("ExLaTeX module say: evince ",EXERCISE_PDF_PATHNAME)
    subprocess.Popen(["evince",EXERCISE_PDF_PATHNAME])

def conf_exsiacua_print_instance(self, html_string, EXERCISE_HTML_PATHNAME):
    print("ExSicua module say: firefox ",EXERCISE_HTML_PATHNAME)
    subprocess.Popen(["firefox","-new-tab", EXERCISE_HTML_PATHNAME])

def conf_examc_print_instance(self, EXERCISE_TEX_PATHNAME, EXERCISE_PDF_PATHNAME):
    print("ExAMC module say: evince ",EXERCISE_PDF_PATHNAME)
    subprocess.Popen(["evince",EXERCISE_PDF_PATHNAME])