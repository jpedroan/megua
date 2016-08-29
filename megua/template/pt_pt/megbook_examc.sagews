{#
{{marker_cell}}{{uuid1}}i{{marker_cell}}

%html
{{html}}

{{marker_output}}{{uuid4}}{{marker_output}}{{json_html}}{{marker_output}}
#}
{{marker_cell}}{{uuid1}}i{{marker_cell}}
{{marker_cell}}{{uuid2}}a{{marker_cell}}
#FAÇA SHIFT-ENTER NESTA CÉLULA
from megua.all import *
meg.set_current_exercise(__file__)
{{marker_cell}}{{uuid3}}{{marker_cell}}
meg.save(r'''
%SUMMARY  Capítulo; Minha Secção 1; Minha Secção 2; Minha Secção 3

Palavras-chave:

Autores:

Ano: 

Propósito do exercício:

 
%PROBLEM (colocar aqui o título desta obra, ex.: Caso dos Peixes Azuis)


Colocar aqui um enunciado para ser compilado com LaTeX.


%ANSWER

Colocar aqui uma proposta de resolução para ser compilado com LaTeX usando notação matemática como
\[
x^2
\]


class {{unique_name}}(ExAMC):

    def make_random(s,edict=None):

        pass #tirar este comando e adicionar o seu programa

                        
''')

{{marker_cell}}{{uuid4}}{{marker_cell}}

meg.new(ekey={{ekey}})

{# https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py #}

{# {{marker_cell}}{{uuid2}}a{{marker_cell}} #}

