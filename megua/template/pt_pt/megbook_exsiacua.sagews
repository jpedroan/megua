{#
    TODO: colocar o megua dog a funcionar e o botão replicate
{{marker_cell}}{{uuid1}}i{{marker_cell}}
%hide
%html
<img src=".OUTPUT/megua_dog.png"/>
{{marker_output}}{{uuid2}}{{marker_output}}{"hide":True,"html":\<html src=\".OUTPUT/megua_dog.png\"\>}{{marker_output}}
#}
{{marker_cell}}{{uuid3}}a{{marker_cell}}
%auto
#NA PRIMEIRA VEZ, FAÇA SHIFT-ENTER NESTA CÉLULA PARA ACORDAR O MEGUA
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
#FAÇA SHIFT-ENTER PARA VER O EXERCÍCIO (e inserir na base de dados quando modificado)
meg.save(r'''
%SUMMARY  Capítulo; Secção 1; Sub Secção 1.1; Sub sub Secção 1.1.1

Palavras-chave:

Lista de "concepts" para a árvore Siacua:

* são 3 dígitos (Assunto, Tema, Conceito) ;
* seguido do peso [0.0 a 1.0] e a soma deve dar 1.0;


Contacto para questões do SIACUA: dmat-siacua@ua.pt
SIACUAstart
level=1;  slip= 0.2; guess=0.25; discr = 0.3
concepts = [(123, 0.8),(124, 0.2) ]
SIACUAend

Autores: Your Name In Here

Ano: 2017

Propósito didático do exercício: ensinar a calcular integrais.

%PROBLEM (colocar aqui o título desta obra, ex.: Caso dos Peixes Azuis Que Sabiam Matemática)

<p>
Colocar aqui um enunciado para ser visionado na web com as várias opções e eventualmente imagens:
</p>

<center>
    <figure>
    FigDaNet1
    </figure>
</center>
<center>
    <figure>
    FigPastaImagens1
    </figure>
</center>
<center>
    <figure>
    PlotFeitoNoSage1
    </figure>
</center>
<center>
    <figure>
    <latex 100%>
    Aqui pode colocar-se \LaTeX\ para ser gerada uma imagem.\\
    Pode ser uma tabela ou TikZ ou equação complexa e com parâmetros.
    \[
        \begin{array}{|c|c|}
        \hline
        x & VALORX \\  \hline
        y & VALORY \\
        \hline
        \end{array}
    \]
    </latex>
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

    def make_random(s):
        r"""
        NOTAS: -- pode apagar esta notas.

        - `s`: é obrigatório ter o "s". Esta letra "s" deve preceder todas as variáveis
               a serem substituida no texto, como por exemplo: "s.valor1 = 10" faz com 
               que onde ocorra "valor1" vá aparecer 10.
        - Já não é preciso o "def solve()"
        """

        s.VALORX = ur.iunif(-4,5)
        s.VALORY = ur.iunif_nonset(-5, 5,[0,1]) #de -5 a 5 mas sem o 0 ou o 1.

        #exemplo de comando para imagens vindas na net
        s.FigDaNet1 = s.static_image(url="https://www.ua.pt/images/40anos.png")

        #exemplo de comando para imagens
        #Precisa de uma pasta ENUNCIADOS/IMAGENS e o upload de uma figura UmaImagemNoSMC.png.
        #s.FigPastaImagens1 = s.static_image(imagefilename='IMAGENS/UmaImagemNoSMC.png')

        #exemplo de plot com o sage
        p1 = plot(sin(x), x, xmin=-pi, xmax=pi, ymin=-1, ymax=1, color='blue',axes_labels=['$x$','$y$'])
        legenda1 = text( r'$y=%s$' % latex(sin(x)), (1,0.5) )
        s.PlotFeitoNoSage1 = s.sage_graphic( p1+legenda1, "PlotFeitoNoSage1", scr_pixels=(300,300))

    #Atenção: o solve já não é preciso e esta linha pode ser apagada.
    #DEF SOLVE(): o solve já nao é preciso e esta linha pode ser apagada.



    #===================================================================
    #As próximas linhas são "avançadas." Apagar caso não as queira usar.
    #===================================================================
    def make_random(s,pontocritico=None):
        r"""
        TIPOS DE EXERCÍCIOS:
        Suponha que este exercício serve para criar pontos críticos dos
        três tipos: 'máximo', 'ponto de sela', 'mínimo' ou ainda, 'não é ponto crítico'.

        NOTAS:
        - `s`: é obrigatório ter o "s". Esta letra "s" deve preceder todas as variáveis
               a serem substituida no texto, como por exemplo: "s.valor1 = 10" faz com 
               que onde ocorra "valor1" vá aparecer 10.
        - `pontocritico`: define que tipo de ponto se irá criar no exercício aleatório.
        - podem ser criadas quaisquer variáveis com quaisquer nomes (nomes tipo Python).
        """

        #Obrigatório quando há parâmetros como "pontocritico" no make_random:
        pontocritico = s.choose(pontocritico,['máximo', 'ponto de sela', 'mínimo', 'não é ponto crítico'])

        if pontocritico=='máximo':
            #gera um exercício para máximo
            pass #tirar este pass quando criar o exercício
        elif pontocritico=='mínimo':
            #gera um exercício para mínimo
            pass #tirar este pass quando criar o exercício
        elif pontocritico=='ponto de sela':
            #gera um exercício para ponto de sela
            pass #tirar este pass quando criar o exercício
        else:
            #gera um exercício para um ponto que não é crítico
            pass #tirar este pass quando criar o exercício

    #====================================================================
    #DEF SOLVE(): o solve já nao é preciso e esta linha pode ser apagada.
    #====================================================================

    ''')

{{marker_cell}}{{uuid8}}{{marker_cell}}

meg.new(ekey=10)
#alternativa: meg.new(ekey=10,pontocritico='máximo')

{# https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py #}









