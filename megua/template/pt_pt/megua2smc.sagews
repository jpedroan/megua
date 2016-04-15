{# megua2smc.py (comment) #}{{marker_cell}}{{uuid1}}i{{marker_cell}}
%html
{{html}}

{{marker_output}}{{uuid4}}{{marker_output}}{{json_html}}{{marker_output}}

{{marker_cell}}{{uuid2}}a{{marker_cell}}
from megua.all import *
#meg = MegBook('{{megbookfilename}}')
{{marker_cell}}{{uuid3}}{{marker_cell}}
meg.save(r'''
%SUMMARY  {{sections}}

{{summary}}

 
%PROBLEM {{problem_name}}

{{problem}}

%ANSWER

{{answer}}


{{code}}    
                        
''')

{{marker_cell}}{{uuid4}}{{marker_cell}}

meg.new("{{unique_name}}",ekey=10)

{# https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py #}

