import os
import codecs
import subprocess

from megua.platex import pcompile
from megua.jinjatemplates import templates
from megua.megoptions import *

def conf__siacua_send(self):
    print("ExSicua module say: firefox ",content.headers['Location'])
    subprocess.Popen(["firefox","-new-tab", content.headers['Location']])

def conf_siacuapreview(self):
    print("exsiacua.py: opening firefox ",html_full_path,"in the browser and press F5.")
    subprocess.Popen(["firefox","-new-tab", html_full_path])

def conf_set_current_exercise(self):
    print("Exercise {}".format(unique_name))

def conf_new_exercise(self):
    print("MegBook module say: gvim ",fullpath)
    subprocess.Popen(["gvim",fullpath])

def conf_replicate_exercise(self):
    print("MegBook module say: gvim ",fullpath)
    subprocess.Popen(["gvim",fullpath])

def conf_catalog(self):
    print("MegBook module say: evince ",CATALOG_PDF_PATHNAME)
    subprocess.Popen(["evince",CATALOG_PDF_PATHNAME])

def conf_latex_document(self):
    print("MegBook module say: evince ",DOC_PDF_PATHNAME)
    subprocess.Popen(["evince",DOC_PDF_PATHNAME])

def conf_fast_exam_siacu(self):
    print("MegBook module say: evince ",EXAM_PDF_PATHNAME)
    subprocess.Popen(["evince",EXAM_PDF_PATHNAME])

def conf_exlatex_print_instance(self):
    print("ExLaTeX module say: evince ",EXERCISE_PDF_PATHNAME)
    subprocess.Popen(["evince",EXERCISE_PDF_PATHNAME])

def conf_exsiacua_print_instance(self):
    print("ExSicua module say: firefox ",EXERCISE_HTML_PATHNAME)
    subprocess.Popen(["firefox","-new-tab", EXERCISE_HTML_PATHNAME])

def conf_examc_print_instance(self):
    print("ExAMC module say: evince ",EXERCISE_PDF_PATHNAME)
    subprocess.Popen(["evince",EXERCISE_PDF_PATHNAME])