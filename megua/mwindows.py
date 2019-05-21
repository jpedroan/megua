import os
import codecs
import subprocess

from megua.platex import pcompile
from megua.jinjatemplates import templates
from megua.megoptions import *

def conf__siacua_send(self, content):
    print("Not implemented windows: conf__siacua_send")

def conf_siacuapreview(self, html_full_path):
    import webbrowser
    url = os.path.join(self.wd_fullpath,self.unique_name()+'_siacuapreview.html')
    webbrowser.open(url)


def set_current_exercise(self):
    import requests
    import ipykernel
    import re
    from notebook.notebookapp import list_running_servers
    from megbook import isidentifier

    TOKEN = next(list_running_servers())['token']

    base_url = next(list_running_servers())['url']
    r = requests.get(
        url=base_url + 'api/sessions',
        headers={'Authorization': 'token {}'.format(TOKEN),})

    r.raise_for_status()
    response = r.json()

    kernel_id = re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)
    pathname = {r['kernel']['id']: r['notebook']['path'] for r in response}[kernel_id]

    (edir,filename) = os.path.split(pathname)
    (unique_name,ext) = os.path.splitext(filename)

    if ext == '.py':
        (unique_name,ext) = os.path.splitext(unique_name)
        assert(ext=='.sage')
        pathname = os.path.join(edir,unique_name+'.sage')
        #print "megbook.py: Corrected",pathname

    assert(ext) #See DEVEL notes above: ext<>''
    self._current_unique_name = None

    if not isidentifier(unique_name):
        print("Megbook.py: Filename is not a valid Python identifier.")
        usage_new()
        raise SyntaxError


    #get file contents 
    unique_name_changed = False
    with codecs.open(pathname, mode='r', encoding='utf-8') as f:
        source_code = f.read()
        #Parse file contents. See above.
        PATTERN_STRING = ur'class +([_A-Za-z][_a-zA-Z0-9]*)\((\w+)\):\s*'
        re_class_match = re.search(PATTERN_STRING,source_code,re.U|re.M)
        if re_class_match:
            old_unique_name = re_class_match.group(1)
            unique_name_changed = old_unique_name != unique_name

    if unique_name_changed:
        #Try to rename, first in the database:
        # the new unique_name could already exist
        self.megbook_store.rename(old_unique_name,unique_name,warn=False)
        #Change source code
        new_source_code = re.sub(old_unique_name,unique_name,source_code,re.U|re.M)
        with codecs.open(pathname, mode='w', encoding='utf-8') as f:
            f.write(new_source_code)
        print("========================")
        print("Please, ")
        print("1. Execute the above comand again using shift-enter ('meg.set_current_exercise(__file__)').")
        print("")
        print("Explanation:")
        print("1. The filename containing the exercise was renamed.")
        print("2. The new name of the exercise is now: {}".format(unique_name))
        print("3. Confirm the new <name_of_exercise> in the line 'class <name>(...)'.")
        print("")
        print("========================")
        raise IOError

    #To be used in all megbook commands
    self._current_unique_name = unique_name

    self.conf_set_current_exercise()


def conf_set_current_exercise(self):
    print("Exercise {}".format(self._current_unique_name))
    
def conf_new_exercise(self, fullpath):
    print("Not implemented windows: conf_new_exercise")
    
def conf_replicate_exercise(self, fullpath, fullpath_new):
    print("Not implemented windows: conf_replicate_exercise")
    
def conf_catalog(self, CATALOG_PDF_PATHNAME, CATALOG_TEX_PATHNAME):
    print("Not implemented windows: conf_catalog")
    
def conf_latex_document(self, DOC_PDF_PATHNAME, DOC_LATEX_PATHNAME):
    print("Not implemented windows: conf_latex_document")
    
def conf_fast_exam_siacua(self, EXAM_PDF_PATHNAME, EXAM_TEX_PATHNAME):
    print("Not implemented windows: conf_fast_exam_siacu")

def conf_exlatex_print_instance(self, EXERCISE_TEX_PATHNAME, EXERCISE_PDF_PATHNAME):
    print("Not implemented windows: conf_exlatex_print_instance")

def conf_exsiacua_print_instance(self, html_string, EXERCISE_HTML_PATHNAME):
    from IPython.display import display, Markdown
    display(Markdown(html_string))

def conf_examc_print_instance(self, EXERCISE_TEX_PATHNAME, EXERCISE_PDF_PATHNAME):
    print("Not implemented windows: conf_examc_print_instance")