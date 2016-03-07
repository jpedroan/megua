{# megua2smc.py (comment) #}{{marker_cell}}{{uuid1}}i{{marker_cell}}
%html
{{html}}

{{marker_output}}{{uuid4}}{{marker_output}}{{json_html}}{{marker_output}}

{{marker_cell}}{{uuid2}}a{{marker_cell}}
from megua.all import *
meg = MegBook('{{filename}}')
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

     if html:
            out += MARKERS['cell'] + uuid() + 'i' + MARKERS['cell'] + u'\n'
            out += '%html\n'
            out += html + u'\n'
            out += (u'\n' + MARKERS['output'] + uuid() + MARKERS['output'] +
                    json.dumps({'html':html}) + MARKERS['output']) + u'\n'

