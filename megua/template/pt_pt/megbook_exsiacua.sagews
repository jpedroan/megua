{#
{{marker_cell}}{{uuid1}}i{{marker_cell}}
%hide
%html
<img src=".OUTPUT/megua_dog.png"/>
{{marker_output}}{{uuid2}}{{marker_output}}{"hide":True,"html":\<html src=\".OUTPUT/megua_dog.png\"\>}{{marker_output}}
#}
{{marker_cell}}{{uuid3}}a{{marker_cell}}
%auto
#FAÇA SHIFT-ENTER NESTA CÉLULA PARA ACORDAR O MEGUA
from megua.all import *
meg.set_current_exercise(__file__)
{{marker_cell}}{{uuid4}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA ESCOLHER CHAVES ANTES DE ENVIAR
#meg.siacuapreview( ekeys=[0,1,2,3,4,5,6,7,8,9] )
{{marker_cell}}{{uuid5}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA ENVIAR PARA siacua.web.ua.pt
#meg.siacua(
#  ekeys=[0,1,2,3,4,5,6,7,8,9],
#  sendpost=True,
#  course='{{course}}',  #ALTERAR CURSO ??
#  usernamesiacua='{{usernamesiacua}}',  #ALTERAR USERNAME  ?
#  siacuatest=True,  #ALTERAR: True ou False  ?
#)
{{marker_cell}}{{uuid6}}{{marker_cell}}
{{marker_cell}}{{uuid7}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA VER O EXERCÍCIO
meg.save(r'''
%SUMMARY  Capítulo; Secção 1; Sub Secção 1.1; Sub sub Secção 1.1.1

Palavras-chave:

Lista de "concepts" para a árvore Siacua:

* são 3 dígitos (Assunto, Tema, Conceito) ;
* seguido do peso [0.0 a 1.0] e a soma deve dar 1.0;

SIACUAstart
level=1;  slip= 0.2; guess=0.25; discr = 0.3
concepts = [(123, 0.8),(124, 0.2) ]
SIACUAend

Autores:

Ano: 2017

Propósito do exercício:
 
%PROBLEM (colocar aqui o título desta obra, ex.: Caso dos Peixes Azuis)

<p>
Colocar aqui um enunciado para ser visionado na web com as várias opções e eventualmente imagens:
</p>

<center>
    <figure>
    fig1
    </figure>
</center>

<p>Escolha a opção correta:</p>
<multiplechoice>
<choice> Aqui a opção certa.</choice>
<choice> Aqui a opção errada 1.</choice>
<choice> Aqui a opção errada 2.</choice>
<choice> Aqui a opção errada 3.</choice>
</multiplechoice>


%ANSWER

Colocar aqui uma proposta de resolução para ser compilado com LaTeX usando notação matemática como
\[
x^2
\]



class {{unique_name}}(ExSiacua):

    def make_random(s,edict=None):

        pass #tirar este comando e adicionar o seu programa
        s.fig1 = s.static_image(url="https://www.ua.pt/images/40anos.png")

''')

{{marker_cell}}{{uuid8}}{{marker_cell}}

meg.new(ekey=10)

{# https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py #}









