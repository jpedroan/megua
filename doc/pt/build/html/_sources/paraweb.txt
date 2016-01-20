

.. _websection:


Exercícios para a web
=====================


Um dos formatos comuns para uso na internet é criar exercícios de escolha múltipla: só uma resposta correta em todas as especificadas.
Nesta situação não dá muito jeito criar alíneas pelo que o problema colocado e a resolução detalhada é só uma, é a que conduz à única solução correta.

O outro estilo que o MEGUA disponibiliza é para :ref:`papel <papelsection>` e neste estilo as alíneas 
são naturalmente parte integrante. 


Exercício Completo
------------------

Ilustra-se agora um exercício completo para escolha múltipla:

**Célula 1**

Copie e cole, depois faça *shift enter* para a executar. 
O nome *mp2013web.sqlite* é o nome escolhido para os trabalhos de mestrado de 2013/2014. Use sempre este nome se está no mestrado.

::
  
   #auto
   from megua.all import *
   meg = MegBookWeb("/home/nbuser/mp2013web.sqlite")

Se ocorrer *Assert error* é porque deve usar *MegBookWeb*.


**Célula 2**

Copiar e colar e depois fazer *shift enter* para a executar.

::

    meg.save(r"""

    %summary Demonstração; Escolha múltipla     

    Este exercício considera as divisões.

     
    %problem Exemplo 

    O resultado de $av/bv$ é:

    %answer

    <multiplechoice>
    <choice> $$vresposta$$ </choice>
    <choice> $$errada1$$ </choice>
    <choice> $$errada2$$ </choice>
    <choice> $$errada3$$ </choice>
    </multiplechoice>

    A resposta é $vresposta$. Faltaria detalhar os passos de uma divisão para esta resposta ficar completa.

    class E12X34_numeros_001(Exercise):
        
        def make_random(s):
            s.av = ur.iunif(1,10)
            s.bv = ur.iunif(20,30)
        def solve(s):
            s.vresposta= (s.av / s.bv).n(digits=3) #arredonda a parte decimal a 3 algarismos.
            #Opções Erradas
            s.errada1 = s.vresposta*0.9
            s.errada2 = s.vresposta*1.2
            s.errada3 = s.vresposta*1.3

    """)

Após a execução da célula irá aparecer o:

**Resultado**

O resultado é um ficheiro `html` que pode ser visualizado com um *click* na primeira vez. Posteriores alterações podem ser vistas usando a tecla F5 que atualiza.



Descrição da estrutura
----------------------

A estrutura anterior tem várias componentes que vamos descrever.

O  bloco de **escolha múltipla** tem (agora) a seguinte sintaxe:

.. code-block:: xml

   <multiplechoice>
   <choice> $$vresposta$$ </choice>
   <choice> $$errada1$$ </choice>
   <choice> $$errada2$$ </choice>
   <choice> $$errada3$$ </choice>
   </multiplechoice>

com qualquer número de <choice> e em que a primeira é sempre a única correta!

Depois do bloco de escolha múltipla ocorre a parte da respsta completa escrita em LaTeX:

.. code-block:: latex

    A resposta é $vresposta$. Faltaria detalhar os passos de uma divisão para esta resposta ficar completa.




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

Podem existir mais que dois casos.



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



.. _graficosweb:


Gráficos
--------

Esta secção descreve ferramentas para se criarem objectos gráficos "dentro" dos exercícios, possivelmente como função dos 
parâmetros que os caracterizam. Para outro tipo de gráficos ou imagens consulte a secção `Imagens <staticimages>`_.

Para tal consideramos duas tecnologias para os construir:

* LaTeX e o pacote TikZ (2d e 3d).
* Gráficos do Sage Mathematics (2d e 3d).


Para utilizar os **gráficos do Sage** considere as duas etapas seguintes.

1. Em qualquer parte do texto coloque o nome do gráfico, por exemplo centrado:

.. code-block:: html

   <center>
   fig1
   </center>

2. Na parte da programação (make_random ou solve) faça:

.. code-block:: python

   s.param1 = ur.iunif(1,5) #um possível parâmetro.
   s.inf1 = -1 #limite inferior do domínio
   s.sup1 = 1 #limite superior do domínio
   g1 = plot(sin(s.param1*x),x, s.inf1, s.sup1, color='blue')
   g2 = plot(cos(s.param1*x),x, s.inf1, s.sup1,  color='red') 
   s.fig1 = s.sage_graphic( g1+g2, "fig1", dimx=7, dimy=7) #7cm

Desta maneira será produzido um gráfico parametrizado.  

Pode-se encontrar infomação sobre gráficos em Sage nestas duas páginas:

* `Plot 2d <http://www.sagemath.org/doc/reference/plotting/index.html>`_: gráficos de funções e construções gráficas;
* `Plot 3d <http://www.sagemath.org/doc/reference/plot3d/index.html>`_: o mesmo para 3d. No caso 3d nem todos os gráficos poderão ser bem convertidos em imagens de qualidade (por enquanto).



Para utilizar o **LaTeX** para criar imagens procede-se em dois passos.

1. Na parte do texto (%problem ou %answer ou opções) coloque:

::

   <latex 100%>
      COMANDOS LATEX OU COMANDOS TIKZ
      que possivelmente dependam de parâmetros.
   </latex>

2. Na parte da programação dar valores ao parâmetros (como habitual, isto é, não é necessário chamar nenhum comando especial).

O valor 100% indica que o desenho aparece na escala normal mas pode ser modificado, aumentando ou reduzindo, sendo que estas transformações podem sempre piorar um pouco a qualidade.

Qualquer comando normal de LaTeX pode ser usado (incluindo uma demonstração inteira) ou então podem ser usados pacotes gráficos especializados 
como é o caso do `Tikz <http://paws.wcu.edu/tsfoguel/tikzpgfmanual.pdf>`_. Existem `exemplos <http://www.texample.net/tikz/examples/>`_ 
muito atrativos de uso do TikZ. Outra maneira de usar o TikZ é construir gráficos no Geogebra e exportar em TikZ para
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

No exemplo acima existem imensos parâmetros em virtude da figura resultante ser complexa. Explicam-se alguns aspetos:

* O TikZ requer números inteiros ou reais aproximados.
* São exemplos de parâmetros: *v11@f{f}* em que **@f{f}** indica que o número racional *v11* deve ser convertido à sua aproximação real.
* Também, são exemplos de parâmetros: *ix0*, ou ainda *labelA1*. Estes sem qualquer conversão.
* Todos os parâmetros são calculados na parte da programação.

Os gráficos do pacote TikZ são maioritariamente para 2D. Mas é ainda 
possível criar **gráficos para 3D** recorrendo a um complemento para o TikZ chamado de
`3dplot <ftp://ftp.tex.ac.uk/pub/tex/graphics/pgf/contrib/tikz-3dplot/tikz-3dplot_documentation.pdf>`_. Outros exemplos
sem recurso a este pacote podem ser encontrados `aqui <http://www.texample.net/tikz/examples/tag/3d/>`_.





.. _staticimages:

Imagens Estáticas
-----------------

Podem-se incluir imagens estáticas como fotos ou gráficos não parametrizados, produzidas no Sage ou provenientes
de outras fontes. Para as utilizar num exercício MEGUA siga as etapas seguintes:

1. Obtenha o ficheiro com o gráfico ou imagem e faça *upload* no Sage:

Notas:

* por baixo do nome do *worksheet*, no Sage Notebok, existe o menu "Data:" para realizar *uploads*;
* o gráfico pode ser gerado numa célula e gravado no Desktop para posterior *upload*. Consulte a secção `Gráficos <graficosweb>`_ sobre gráficos no Sage. 
* sugerem-se nomes na forma: ``user_planeta_terra_001.jpg`` (ou outra extensão).

2. É necessário saber o *filename* completo até ao ficheiro. Faça como no exemplo:

.. code-block:: python

   print DATA   #shift enter
   /home/sageserver/sage_notebook.sagenb/home/admin/163/data/

e junte o resultado ao nome do gráfico obtendo o caminho final::

   "/home/sageserver/sage_notebook.sagenb/home/admin/163/data/user_planeta_terra_001.jpg"


3. Em qualquer parte do texto do seu exercício coloque a variável que será substituída pelo gráfico, por exemplo, centrando:

.. code-block:: html

   <center>
   fig1
   </center>

4. Na parte da programação (make_random ou solve) faça:

.. code-block:: python

   s.fig1 = s.sage_staticgraphic("/home/sageserver/sage_notebook.sagenb/home/admin/163/data/user_planeta_terra_001.jpg",dimx=200, dimy=200) 
   # 200 x 200 pixeis



Desta maneira, será reproduzida a imagem em todas as instâncias do exercício.  



.. _tabelas:

Tabelas
-------

Podem-se criar tabelas em HTML ou LaTeX (convertidas numa imagem) mas usar o HTML é preferível quando se 
produzem exercícios para a web! 
Porém, se o exercício é uma reutilização de outro exercício que já utiliza tabelas em LaTeX 
pode-se, em geral, reutilizar a notação LaTeX (com eventual perda de alguma qualidade gráfica). 


Uma tabela em **HTML** tem o formato:

.. code-block:: html

   <table border="1">
   <tr> <td> a11 </td> <td> a12 </td> <td> a13 </td> </tr>
   <tr> <td> a21 </td> <td> a22 </td> <td> a23 </td> </tr>
   <tr> <td> a31 </td> <td> a32 </td> <td> a33 </td> </tr>
   </table>

em que os ``aij`` podem tomar qualquer forma. Os marcadores ``<tr>`` designam uma linha ("row") e 
os marcadores ``<td>`` designam as colunas. Para mais informação sugerimos a consulta de:

* http://truben.no/latex/table/
* http://www.w3schools.com/html/html_tables.asp

   

Em **LaTeX** e usando o **marcador** ``<latex 100%>`` podem também ser criadas tabelas (que serão convertidas em imagens). 
A tabela mencionada neste exemplo será convertida numa imagem:

.. code-block:: latex

    <latex 100%>
    \begin{tabular}{|c|c|c|}
    \hline
    par1 & par2 & par3 \\
    \hline
    \end{tabular}
    </latex>

em que *par1*, *par2*, e *par3* são parâmetros a serem calculados na parte da programação. Infelizmente há pelo
menos uma restrição: o marcador ``<latex 100%>`` não garante correta compilação de todas as expressões 
em LaTeX que usem ``\begin{array}`` (e poderão ocorrer outros casos).  


Ainda **LaTeX** mas sem usar o marcador acima, podem também ser criadas tabelas 
usando a notação matemática (o software `MathJAX <http://www.mathjax.org/>`_ é executado no 
seu *browser* e faz o serviço de conversão da notação LaTeX no objecto gráfico):

.. code-block:: latex

    \begin{array}{|c|c|c|}
    \hline
    par1 & par2 & par3 \\
    \hline
    \end{array}

em que *par1*, *par2*, e *par3* são parâmetros a serem calculados na parte da programação. A qualidade também pode não ser 
perfeita.

Sugere-se um possível gerador de tabelas em LaTeX e um documento muito completo sobre o tema:

* http://truben.no/latex/table/
* http://en.wikibooks.org/wiki/LaTeX/Tables






