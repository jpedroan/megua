# coding: utf8

# {{unique_name}}

from megua.all import *

meg.save(r'''
%SUMMARY  Minha Secção 1; Minha Secção 2; Minha Secção 3

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



class {{unique_name}}(Exsiacua):

    def make_random(s,edict=None):

        pass #tirar este comando e adicionar o seu programa

                        
''')


# meg.new("{{unique_name}}",ekey={{ekey}})


