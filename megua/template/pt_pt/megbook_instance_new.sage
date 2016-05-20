# coding: utf8

{# MegBook.py, def exerciseinstance(), called by save() and by new()  #}

from megua.all import *


{{class_text}}

#Sections: {{sections}}

{{unique_name}}._unique_name = "{{unique_name}}"

{{unique_name}}._summary_text = r"""{{sumtxt}}"""

{{unique_name}}._problem_text = r"""{{probtxt}}"""

{{unique_name}}._answer_text  = r"""{{anstxt}}"""

{{unique_name}}._suggestive_name = r"""{{suggestivename}}"""


ex_instance = {{unique_name}}(ekey={{ekey}},edict={{edict}})





