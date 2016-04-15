{{marker_cell}}{{uuid1}}i{{marker_cell}}
{# megbook.py #}
%html
{{html}}

{{marker_output}}{{uuid4}}{{marker_output}}{{json_html}}{{marker_output}}

{{marker_cell}}{{uuid2}}a{{marker_cell}}
from megua.all import *
#meg = MegBook('{{megbookfilename}}')
{{marker_cell}}{{uuid3}}{{marker_cell}}
meg.save(r'''
%SUMMARY  Minha Secção 1; Minha Secção 2; Minha Secção 3

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


class {{unique_name}}(Exlatex):

    def make_random(s,edict=None):

        pass #tirar este comando e adicionar o seu programa

                        
''')

{{marker_cell}}{{uuid4}}{{marker_cell}}

meg.new("{{unique_name}}",ekey={{ekey}})

{# https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py #}

{# {{marker_cell}}{{uuid2}}a{{marker_cell}} #}

