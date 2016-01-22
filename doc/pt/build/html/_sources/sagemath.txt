


.. _sagemath:

Sage Mathematics
================

Aquilo a que chamamos de "MEGUA" é um pacote de software que permite criar exercícios parametrizados recorrendo ao ambiente Sage Mathematics, sistema este que se descreve de seguida.

O Sage Mathematics é uma enorme biblioteca e também um sistema de acesso a bibliotecas de matemáticas já existentes. Grande parte dstas bibliotecas matemáticas foi desenvolvida para o sistema Linux pelo que a sua disponibilização em Windows ainda está em desenvolvimento. Se usa um computador Linux (distribuição Ubuntu, por exemplo), então é bastante fácil instalar e usar o Sage.


Porque, nos tempos atuais:

* a maioria usa computadores com Windows
* tablets
* e já existem hábitos de programação na nuvem (Cloud Computing and Archive)

então houve necessidade de criar o :ref:`Sage Notebook <sagenotebook>` que usamos no 
projeto MEGUA para de criação e reutilizaçao de exercícios parametrizados.

Já no decurso deste projeto surgiu uma versão muito modernizada e com filosofia de 
segurança e sistema de partilha de projetos diferente do notebook: 
chama-se `Sage Mathematics Cloud <https:cloud.sagemath.org>`_  (sigla SMC). Pode criar uma conta 
nesse sistema e usar as capacidades do Sage na nuvem, convidando os seus estudantes a fazer o mesmo. 

NOTA: o pacote MEGUA ainda não está disponível para esse sistema.


.. _sagenotebook:

Sage Notebook
-------------

O *Notebook* é a ferramenta que está a ser usada para criar os exercícios parametrizados com a vantagem de ver os resultados imediatamente e poder partilhar com os colegas ou outros autores.

O *notebook*, normalmente, serve para cálculo e exibição de resultados gráficos. Antes de começar um novo exercício pode usar esta potencialidade para testar comandos, ver gráficos, etc.

As caixas visíveis são chamadas de **células** e permitem a introdução de comandos.  
Estes comandos são "calculados" com **shift+enter**. 

Para  apagar uma caixa, apaga-se primeiro todo o seu conteúdo e depois usar o **backspace** no seu teclado.

Exemplos (onde está "sage:" é como se fosse uma célula):

::

   sage: 1+2  #fazer shift enter
   3

ou podemos criar um gráfico com::

   sage: plot(sin(x),x,figsize=(2,2))

.. image:: nb_sin.*


Pesquisa via google
-------------------

Se pretende encontrar uma solução que acha que deve existir ou simplesmente averiguar se já gluém explorou um dado tema deve procurar via google (claro que normalmente lembramo-nos de realizar esta tarefa mas curiosamente nem sempre recordamos isto para temas que são novos, como pode ser o caso de programação em Python ou LaTeX).

Assim, recomenda-se a pesquisa de termos em inglês começando por "sage math" seguido de outros termos. 
Seguem-se exemplos:

* `sage math plot axes <https://www.google.pt/search?q=sage+math+plot+axes>`_ para informação sobre gráficos e eixos coordenados.
* `sage math integration <https://www.google.pt/search?q=sage+math+integration>`_

Em resumo, este tutorial é um guia para produzir exercícios parametrizados que contem descrições muito resumido das largas capacidades do Sage Mathematics. A **pesquisa** de como realizar tarefas
de programação ou LaTeX **é um ato do dia a dia** do utilizador do Sage.


