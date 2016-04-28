# coding: utf8


########################
# {{unique_name}}
########################

#For copy/paste use also this commands:
from megua.all import *
meg = MegBook('{{megbookfilename}}')

meg.save(r'''
%SUMMARY  {{sections}}

{{summary}}

 
%PROBLEM {{problem_name}}

{{problem}}

%ANSWER

{{answer}}


{{code}}    
                        
''')

{# megua2smc.py (comment) #}
