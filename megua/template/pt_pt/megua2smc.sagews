{# megua2smc.py (comment) #}{{marker_cell}}{{uuid1}}i{{marker_cell}}
{{marker_cell}}{{uuid3}}a{{marker_cell}}
%auto
#FAÇA SHIFT-ENTER NESTA CÉLULA PARA ACORDAR O MEGUA (primeira vez apenas)
from megua.all import *
meg.set_current_exercise(__file__)
{{marker_cell}}{{uuid4}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA ESCOLHER CHAVES ANTES DE ENVIAR
#meg.siacuapreview( ekeys=[0,1,2,3,4,5,6,7,8,9] )

{{marker_cell}}{{uuid5}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA ENVIAR PARA siacua.web.ua.pt (contacto dmat-siacua@ua.pt)

{{send_siacua}}

{# {{marker_cell}}{{uuid6}}{{marker_cell}} #}

{{marker_cell}}{{uuid6}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA VER O EXERCÍCIO (e inserir na base de dados quando modificado)
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

meg.new(ekey=10)

{# https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py #}

