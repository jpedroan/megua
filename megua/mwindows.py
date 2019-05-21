import os
import codecs
import subprocess

from megua.platex import pcompile
from megua.jinjatemplates import templates
from megua.megoptions import *

def conf__siacua_send(self):
    print("Not implemented windows: conf__siacua_send")

def conf_siacuapreview(self):
    import webbrowser
    url = os.path.join(self.wd_fullpath,self.unique_name()+'_siacuapreview.html')
    webbrowser.open(url)

def conf_set_current_exercise(self):
    import requests
    import ipykernel
    import re
    from notebook.notebookapp import list_running_servers

    TOKEN = next(list_running_servers())['token']

    base_url = next(list_running_servers())['url']
    r = requests.get(
        url=base_url + 'api/sessions',
        headers={'Authorization': 'token {}'.format(TOKEN),})

    r.raise_for_status()
    response = r.json()

    kernel_id = re.search('kernel-(.*).json', ipykernel.connect.get_connection_file()).group(1)
    notebook_path = {r['kernel']['id']: r['notebook']['path'] for r in response}[kernel_id]

    self.set_current_exercise(notebook_path)
    print("Exercise {}".format(self._current_unique_name))
    
def conf_new_exercise(self):
    print("Not implemented windows: conf_new_exercise")
    
def conf_replicate_exercise(self):
    print("Not implemented windows: conf_replicate_exercise")
    
def conf_catalog(self):
    print("Not implemented windows: conf_catalog")
    
def conf_latex_document(self):
    print("Not implemented windows: conf_latex_document")
    
def conf_fast_exam_siacu(self):
    print("Not implemented windows: conf_fast_exam_siacu")

def conf_exlatex_print_instance(self):
    print("Not implemented windows: conf_exlatex_print_instance")

def conf_exsiacua_print_instance(self):
    from IPython.display import display, Markdown
    display(Markdown(html_string))

def conf_examc_print_instance(self):
    print("Not implemented windows: conf_examc_print_instance")