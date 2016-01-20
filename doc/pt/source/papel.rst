
.. http://sphinx-doc.org/markup/inline.html#ref-role
.. http://sphinx-doc.org/markup/inline.html

.. _papelsection:

Exercícios em papel
===================

Os exercícios em papel têm características diferentes dos exercícios para 
a :ref:`web <websection>` entre as quais salientamos:

* Usa-se o LaTeX para descrever os exercícios (não se usa HTML, como para os exercícios para a :ref:`web <websection>`).
* Cada ``worksheet`` (tal como no caso web) contém um exercício.

Já com uma base de dados construída, é depois possível:

* Apresentar exercícios de forma sequêncial, com numeração.
* As resoluções podem ou não constar do documento.
* Estas podem aparecer logo depois do exercício ou no final do documento (ao estilo "soluções").
* Podem criar-se brochuras de exercícios ou formato tipo exame.
* Pode-se exportar o LaTeX para edição no software de TeX no computador pessoal.

e outras características que se descrevem de seguida.



As etapas para criar bases de dados de exercícios são:

1. Criar um novo ``worksheet`` no Notebook (do Sage Mathematics).
2. Numa célula nova, abrir a base de dados (se não existir será criada). Pode indicar o seu username como nome ou o nome dum projeto.
3. Na célula seguinte, introduz-se o modelo do exercício.

Depois de se criar uma base de dados com os necessários exercícios podem-se criar os formatos (brochuras, exames, etc), usando uma nova ``worksheet``.



Exercício Completo
------------------

Ilustra-se agora um exercício completo para papel:

**Célula 1**

Copie e cole, na primeira célula, o conteúdo abaixo. Mude o NOME para o seu nome ou nome do projeto. Depois faça *shift enter* para a executar.

::
  
   #auto
   from megua.all import *
   meg = MegBook("/home/nbuser/NOME.sqlite")

Agora, na segunda célula vamos introduzir o primeiro exercício:


**Célula 2**

Copiar e colar e depois fazer *shift enter* para a executar.

::

    meg.save(r"""

    %SUMMARY Demonstração; Papel     

    Este exercício considera as quatro operações aritméticas.

    Classificação: 97F20 Pre-numerical stage, concept of numbers
     
    %PROBLEM Exemplo 

    Determine:
    \begin{enumerate}
    \item[(a)] $num1+den1$
    \item[(b)] $num1-den1$
    \item[(c)] $num1 \times den1$
    \item[(d)] $num1/den1$
    \end{enumerate}

    %ANSWER


    As soluções são
    \begin{enumerate}
    \item[(a)] $num1+den1=rsum$
    \item[(b)] $num1-den1=rdiff$
    \item[(c)] $num1 \times den1=rprod$
    \item[(d)] $num1/den1=rdiv$
    \end{enumerate}



    class E97F20_operacoes_001(Exercise):
        
        def make_random(s):
            s.num1 = ur.iunif(1,10)
            s.den1 = ur.iunif(1,10)

        def solve(s):
            s.rsum  = s.num1 + s.den1
            s.rdiff = s.num1 - s.den1
            s.rprod = s.num1 * s.den1
            s.rdiv = round(s.num1 / s.den1,3)


    """)

Após a execução da célula irá aparecer o 

**Resultado**

O resultado é um ficheiro `PDF` e um ficheiro ``tex``. Se estiver a user o Chrome como navegador pode ser visualizado com um *click* na primeira vez no pdf. Posteriores alterações podem ser vistas usando a tecla F5 que atualiza.

Pode abrir o tex e com copy/paste colocar no editor LaTeX do seu computador pessoal.



Descrição da estrutura
----------------------

TO DO!


Escolha de texto
----------------

Uma funcionalidade em exercícios que aglomeram vários casos num único texto surge a necessidade de **escolher texto**. 
Suponha que quer escrever *apenas* uma de duas frases na resolução detalhada ou outra parte do exercício:

* o limite não existe.
* o limite existe e o seu valor é $valor$.

Para estes casos, ou com mais hipóteses, use a sintaxe que é mostrada para o exemplo dado:


.. code-block:: html

   <showone variavel>
    <thisone Caso sem limite - caso 0 - (isto é comentário)>
        O limite não existe.
    </thisone>
    <thisone Caso em que o limite existe - caso 1 (isto é comentário)>    
        O limite existe e o seu valor é \$valor\$.
    </thisone>
   </showone>

posteriomente, na parte da programação, é necessário escolher qual das frases irá ser escolhida. Isso é feito dando um valor apropriado à variável ``s.variavel``:

.. code-block:: python

    class E12X34................
        s.variavel = 0 ou 1 para decidir sobre o texto apropriado.

Claro que podem existir mais que dois casos.


**Outra técnica para seleção de texto** com base numa variável inteira 
é o uso do comando ``variavel@c{"Texto 0","Texto 1","Texto 2"}``. 
O seguinte caso mostra um exemplo de aplicação em 
que ``casov`` define qual das três frases irá aparecer:

**NOTA:** esta versão do ``var@c{....}`` só funciona com letras e espaços. Não funciona com fórmulas ou outros símbolos.

Exemplo de texto:

|   Neste caso como $f(-x)$
|   casov@c{"é","é","não é"} igual
|   casov@c{"à própria função","ao simétrico da função","nem à função nem à sua simétrica"} então a função
|   casov@c{"é uma função par","é uma função ímpar","nem é uma função par nem ímpar"}.

O efeito para o primeiro caso, isto é, se ``casov == 0`` seleciona as frases ou palavras::

    "é" "à própria função" "é uma função par" 

e a frase gerada fica: "Neste caso como f(-x) é  igual à própria função então a função é uma função par."


.. TODO No caso do LaTeX, pode ainda optar por esconder texto usando a ideia do sinal de comentário "%". s.card = '' ou s.card='%'.




Gráficos
--------

Na versão atual consideramos apenas pacote TikZ para gráficos a 2D.

NOTA para quem usa a web: salienta-se que os gráficos TikZ são incluídos naturalmente no LaTex não precisando de marcadores <latex 100%> ... </latex>.

O `manual do Tikz <http://paws.wcu.edu/tsfoguel/tikzpgfmanual.pdf>`_ é um recurso algo longo. Mas existem `exemplos <http://www.texample.net/tikz/examples/>`_  muito atrativos de uso do TikZ em que muitos são auto explicados. 

Outra maneira de usar o TikZ é construir gráficos no Geogebra e exportar em TikZ para
o exercício. Depois basta substituir valores numéricos concretos pelos parâmetros.

Este é um caso:

.. code-block:: latex


    \definecolor{qqqqcc}{rgb}{0,0,0.8}
    \definecolor{qqqqff}{rgb}{0,0,1}
    \definecolor{ccqqqq}{rgb}{0.8,0,0}
    \definecolor{ttzzqq}{rgb}{0.2,0.6,0}

    \begin{tikzpicture}[line cap=round,line join=round,>=triangle 45,x=unx1@f{f}cm,y=uny1@f{f}cm]


    \draw[->,color=black] (v11@f{f},0) -- (v21@f{f},0) node [anchor=north east] { $x$};
    \foreach \x in {}
    \draw[shift={(\x,0)},color=black] (0pt,2pt) -- (0pt,-2pt) node[right,above] {\footnotesize $x$};
    \draw[->,color=black] (0,v12@f{f}) -- (0,v22@f{f}) node [anchor=north east] {$ y$};
    \draw[color=black] (0pt,-5pt) node[left] {\footnotesize $0$};


    \clip(v11@f{f},v12@f{f}) rectangle (v21@f{f},v22@f{f});

    \draw[color=ttzzqq,line width=1.2pt,smooth,samples=100,domain=ext1@f{f}:ext2@f{f}] plot(\x,{a1+b1/((1*\x)+d1)});
    \draw[color=qqqqcc,line width=1pt,smooth,samples=100,domain=ext1@f{f}:ext2@f{f}] plot(\x,{slopes1@f{f}*(\x-ix0)+iy0@f{f}});
    \draw[color=ccqqqq,line width=1pt,smooth,samples=100,domain=ext1@f{f}:ext2@f{f}] plot(\x,{slopet1@f{f}*(\x-ix0)+iy0@f{f}});

    \begin{scriptsize}
    \fill [color=qqqqff] (ix0,iy0@f{f}) circle (1.5pt);
    \draw[color=qqqqff] (labelA1,iy0@f{f}) node[left,below] {$A$};
    \fill [color=qqqqff] (ix1,iy1@f{f}) circle (1.5pt);
    \draw[color=qqqqff] (ix1,iy1@f{f}) node[right,above] {$B$};
    \end{scriptsize}
    \end{tikzpicture}

No exemplo acima existem imensos parâmetros em virtude da figura resultante ser complexa. 
Explicam-se alguns aspetos:

* O TikZ requer números inteiros ou reais aproximados.
* São exemplos de parâmetros: *v11@f{f}* em que **@f{f}** indica que o número racional *v11* deve ser convertido à sua aproximação real.
* Também, são exemplos de parâmetros: *ix0*, ou ainda *labelA1*. Estes sem qualquer conversão.
* Todos os parâmetros são calculados na parte da programação.

Os gráficos do pacote TikZ são maioritariamente para 2D. Mas é ainda 
possível criar **gráficos para 3D** recorrendo a um complemento para o TikZ chamado de
`3dplot <ftp://ftp.tex.ac.uk/pub/tex/graphics/pgf/contrib/tikz-3dplot/tikz-3dplot_documentation.pdf>`_. Outros exemplos
sem recurso a este pacote podem ser encontrados `aqui <http://www.texample.net/tikz/examples/tag/3d/>`_.


.. _tabelaslatex:

Tabelas em LaTeX
----------------

Podem-se criar tabelas em LaTeX usando várias formas, entre elas, o ``tabular`` em 
modo texto e ``array`` em modo matemático. 

Sugere-se um possível gerador de tabelas em LaTeX e um documento muito completo sobre o tema:


* http://truben.no/latex/table/
* http://en.wikibooks.org/wiki/LaTeX/Tables

Usando o marcador ``tabular``:

.. code-block:: latex

    \begin{tabular}{|c|c|c|}
    \hline
    par1 & par2 & par3 \\
    \hline
    \end{tabular}

em que *par1*, *par2*, e *par3* são parâmetros a serem calculados na parte da programação. 
Podem também ser criadas tabelas usando a notação matemática 
(o software `MathJAX <http://www.mathjax.org/>`_ é executado no seu *browser* e faz o 
serviço de conversão da notação LaTeX no objecto gráfico):

.. code-block:: latex

    $$
    \begin{array}{|c|c|c|}
    \hline
    par1 & par2 & par3 \\
    \hline
    \end{array}
    $$

em que *par1*, *par2*, e *par3* são parâmetros a serem calculados na parte da programação.



Brochuras e Testes
------------------

Após a concretização de uma base de exercícios podemos constituir brochuras ou testes conforme explicado no início desta secção.


Depois do autor saber o que pretende tem à sua disposição  comando ``template_fromstring`` para ajudar que necessita conhecer:

* o modo como se visualiza **cada** exercício;
* o formato do texto em geral e quais os exercícios selecionados.


**Que campos deseja?**

Um exercício é caracterizado por vários campos:

* nome (em class E12X34_nome_001)
* sumário
* secções
* nome ilustrativo do problema
* o enunciado do problema (antes da concretização)
* o enunciado do problema (depois de uma concretização)
* a resolução (antes da concretização)
* a resolução (depois de uma concretização)

Assim, a primeira tarefa é criar o texto que define o aspeto e campos a serem usados no texto. Para isso, numa nova célula do ``worksheet`` pode fazer-se, para visualizar **todos** os campos:

**Como se pretende visualizar?**

.. code-block:: python

    #Configuração completa: mostra todos os campos de um exercicio.

    modelo_exercicio = """\\textbf{Name:}~\\verb+{{ exname }}+ \
    \n\n \\textbf{Summary} \n\n {{ summary }} \
    \n\n \\textbf{Problem template} \n\n {{ problemtemplate }} \
    \n\n \\textbf{Answer template} \n\n {{ answertemplate }} \
    \n\n \\begin{verbatim}\n{{ codetxt }}\n\\end{verbatim} \
    \n\n \\textbf{Problem Example } \n\n {{ problem }} \
    \n\n \\textbf{Answer Example } \n\n {{ answer }} \
    \n\n"""

ou ainda, para visualizar apenas a concretização do problema e resolução:

.. code-block:: python

    #Configuração curta: mostra apenas problem e answer

    modelo_curto = """\
    \n\n \\textbf{Problem Example } \n\n {{ problem }} \
    \n\n \\textbf{Answer Example } \n\n {{ answer }} \
    \n\n"""

De seguida:


.. code-block:: python

    #
    # Exemplo de ficheiro latex a ser usado como molde.
    #

    ficha_de_trabalho = r"""
    \documentclass{article}

    \usepackage[utf8]{inputenc}

    \begin{document}
    {{ put_here("E26B05_DPpolinomio_001") }}

    {{ put_here("E26B05_DPexponencial_001") }}

    {{ put_here("E26B05_DPpotencia_001") }}

    {{ put_here("E26B05_DPlogaritmo_001") }}

    {{ put_here("E26B05_DPracional_001") }}

    \end{document}
    """


