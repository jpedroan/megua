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
#FAÇA SHIFT-ENTER NESTA CÉLULA PARA ACORDAR O MEGUA (primeira vez apenas)
from megua.all import *
meg.set_current_exercise(__file__)
{{marker_cell}}{{uuid4}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA ESCOLHER CHAVES ANTES DE ENVIAR
#meg.siacuapreview( ekeys=[0,1,2,3,4,5,6,7,8,9] )

{{marker_cell}}{{uuid5}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA ENVIAR PARA siacua.web.ua.pt (contacto dmat-siacua@ua.pt)

#meg.siacua(
#  ekeys=[0,10],  # Cada inteiro gera um exercício diferente.
#  course='{{course}}',  # Pode alterar o curso. Consulte o administrador do siacua.
#  usernamesiacua='{{usernamesiacua}}',  # Pode alterar o username.
#  level=1,     # I don't know what does this mean but it's an small integer number.
#  slip=0.05,   # The probability of knowing how to answer, commit a mistake.
#  guess=0.25,  # The probability of guessing the right option without any study.
#  discr=0.5,   # Parameter `discr` is the probability that a student knows how to find the right answer.
#  concepts= [ (0,   1)], # Uma lista como [(110, 0.3),(135, 0.7)] onde 0.3+0.7 = 1 e 110 e 135 são 3 dígitos (Assunto, Tema, Conceito).
#  grid2x2=False,  # Write exercise answering options in a 2x2 grid (useful for graphics).
#  siacuatest=False )  # If True, send data to a test machine.



{{marker_cell}}{{uuid6}}{{marker_cell}}
{{marker_cell}}{{uuid7}}{{marker_cell}}
#FAÇA SHIFT-ENTER PARA VER O EXERCÍCIO (e inserir na base de dados quando modificado)
meg.save(r'''
%SUMMARY  Capítulo; Secção 1; Sub Secção 1.1; Sub sub Secção 1.1.1

Palavras-chave: 


Autores: Your Name In Here; Other Previous Author

Modificado nos anos: 2011, 2017

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
<choice> Aqui a opção certa: RESPOSTA1 </choice>
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

        #Obrigatório usar s.variavel quando "variavel" ocorre no texto. Exemplos:
        s.VALORX = ur.iunif(-4,5)
        s.VALORY = ur.iunif_nonset(-5, 5,[0,1]) #de -5 a 5 mas sem o 0 ou o 1.

        #Exemplo de comando para imagens vindas na net:
        s.FigDaNet1 = s.static_image(url="https://www.ua.pt/images/40anos.png")

        #Exemplo de comando para imagens numa pasta 
        #Precisa de uma pasta ENUNCIADOS/IMAGENS e o upload de uma figura UmaImagemNoSMC.png.
        #s.FigPastaImagens1 = s.static_image(imagefilename='IMAGENS/UmaImagemNoSMC.png')

        #Exemplo de gráfico criado dentro do sagemath:
        p1 = plot(sin(x), x, xmin=-pi, xmax=pi, ymin=-1, ymax=1, color='blue',axes_labels=['$x$','$y$'])
        legenda1 = text( r'$y=%s$' % latex(sin(x)), (1,0.5) )
        s.PlotFeitoNoSage1 = s.sage_graphic( p1+legenda1, "PlotFeitoNoSage1", scr_pixels=(300,300))

        if s.VALORX > 10:
            s.RESPOSTA1 = 2 * s.VALORX
        else:
            s.RESPOSTA1 = s.VALORX^2

    #====================================================================
    #DEF SOLVE(): o solve já nao é preciso e esta linha pode ser apagada.
    #====================================================================


{#
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

    #alternativa: meg.new(ekey=10,pontocritico='máximo')

    #====================================================================
    #DEF SOLVE(): o solve já nao é preciso e esta linha pode ser apagada.
    #====================================================================
#}
    ''')

{{marker_cell}}{{uuid8}}{{marker_cell}}

meg.new(ekey=10)

{# https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py #}









