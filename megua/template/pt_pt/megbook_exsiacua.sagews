{#
{{marker_cell}}{{uuid1}}i{{marker_cell}}
%html
{{html}}
{{marker_output}}{{uuid2}}{{marker_output}}{{json_html}}{{marker_output}}
#}
{{marker_cell}}{{uuid1}}i{{marker_cell}}
{{marker_cell}}{{uuid3}}a{{marker_cell}}
%auto
from megua.all import *
meg.set_current(__file__) #set filename as exercise name
{{marker_cell}}{{uuid4}}{{marker_cell}}
#PARA ESCOLHER CHAVES ANTES DE ENVIAR
meg.siacuapreview(
   ekeys=[0,1,2,3,4,5,6,7,8,9]
)
{{marker_cell}}{{uuid5}}{{marker_cell}}
#PARA ENVIAR 
meg.siacua(
  ekeys=[0,1,2,3,4,5,6,7,8,9],
  sendpost=True,
  course='{{course}}',  #ALTERAR CURSO ??
  usernamesiacua='{{usernamesiacua}}',  #ALTERAR USERNAME  ?
  siacuatest=True,  #ALTERAR: True ou False  ?
)
{{marker_cell}}{{uuid6}}{{marker_cell}}
{{marker_cell}}{{uuid7}}{{marker_cell}}
meg.save(r'''
%SUMMARY  Capítulo; Secção 1; Sub Secção 1.1; Sub sub Secção 1.1.1

Palavras-chave:

Autores:

Ano: 

Propósito do exercício:
 
%PROBLEM (colocar aqui o título desta obra, ex.: Caso dos Peixes Azuis)

Colocar aqui um enunciado para ser visionado na web

<p>Escolha a opção correta:</p>
<multiplechoice>
<choice> </choice>
<choice> </choice>
<choice> </choice>
<choice> </choice>
</multiplechoice>


%ANSWER

Colocar aqui uma proposta de resolução para ser compilado com LaTeX usando notação matemática como
\[
x^2
\]



class {{unique_name}}(ExSiacua):

    def make_random(s,edict=None):

        pass #tirar este comando e adicionar o seu programa

                        
''')

{{marker_cell}}{{uuid8}}{{marker_cell}}

meg.new(ekey=10)

{# https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py #}


