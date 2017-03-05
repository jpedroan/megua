


.. _sagemath:

Sage Mathematics
================

MEGUA é um pacote de software para o `SageMath <https://www.sagemath.org>`_ em máquinas linux e `SageMath Cloud <https://cloud.sagemath.com>`_  (sigla SMC) através da net ("cloud") que permite criar exercícios parametrizados recorrendo à linguagem Python e às bibliotecas de matemática do SageMath, sistema este que se descreve de seguida.

O Sage Mathematics (SageMath) usa a linguagem Python para aceder a uma enorme biblioteca de matemática. Grande parte dstas bibliotecas matemáticas foi desenvolvida para o sistema Linux. Se usa um computador Linux (distribuição Ubuntu, por exemplo), então é bastante fácil instalar e usar o SageMath. A sua disponibilização em Windows ainda está em desenvolvimento. 

As vantagens do uso do `SageMath Cloud <https://cloud.sagemath.com>`_  (SMC) são:

* a maioria usa computadores com Windows sendo difícil a instalação do SageMath;
* o uso tablets aponta no sentido da cloud;
* já existem hábitos de programação na nuvem;
* lógica de "projetos" com utilizadores -- em cada instante podem ser adicionados ou removidos utilizadores do projeto.
* um exercício será uma "worksheet" nesse projeto a que os participantes no projeto podem aceder

SMC "Worksheets"
----------------

As *Worksheets* (ficheiros de extensão *.sagews) são usadas para criar os exercícios parametrizados com a vantagem de ver os resultados imediatamente e poder partilhar com os colegas ou outros autores.

Uma *worksheets* serve, normalmente, para cálculo e exibição de resultados gráficos. Antes de começar um novo exercício pode usar esta potencialidade para testar comandos, ver gráficos, etc.

As linhas visíveis são chamadas de **células** e permitem a introdução de comandos.  
Estes comandos são "calculados/executados" com **shift+enter**. 

Para  apagar uma caixa, apaga-se primeiro todo o seu conteúdo.

Exemplos (onde está "sage:" é como se fosse uma célula):

::

   sage: 1+2  #fazer shift enter
   3

ou podemos criar um gráfico com::

   sage: plot(sin(x),x,figsize=(2,2))

.. image:: nb_sin.*


Pesquisa via google
-------------------

Se pretende encontrar uma solução que acha que deve existir ou simplesmente averiguar se já agluém explorou um dado tema deve procurar via google (claro que normalmente lembramo-nos de realizar esta tarefa mas curiosamente nem sempre recordamos isto para temas que são novos, como pode ser o caso de programação em Python ou LaTeX).

Assim, recomenda-se a pesquisa de termos em inglês começando por "sagemath" seguido de outros termos. 
Seguem-se exemplos:

* `sage math plot axes <https://www.google.pt/search?q=sage+math+plot+axes>`_ para informação sobre gráficos e eixos coordenados.
* `sage math integration <https://www.google.pt/search?q=sage+math+integration>`_

Em resumo, este tutorial é um guia para produzir exercícios parametrizados que contem descrições muito resumidas das largas capacidades do Sage Mathematics. A **pesquisa** de como realizar tarefas
de programação ou LaTeX **é um ato do dia a dia** do utilizador do SageMath.


