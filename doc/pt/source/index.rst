.. Tutorial do MEGUA 0.2 documentation master file, created by
   sphinx-quickstart on Sat Oct 19 20:15:05 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tutorial do MEGUA
=================


MEGUA é um pacote de software para o `SageMath <sagemath>`_ que permite criar exercícios parametrizados:

* recorrendo à linguagem Python
* à linguagem LaTeX e HTML dependendo do destino do exercício
* às bibliotecas de matemática do SageMath
* trabalho colaborativo no SageMath Cloud (SMC).

Os exercícios parametrizados podem fazer parte de:

* brochuras de exercícios em LaTeX para documentos PDF
* exercícios para o sistema online `siacua <http://siacua.web.ua.pt>`_
* destinos como Moodle e AMC estão previstos.

O exemplo seguinte ilustra os exercícios parametrizados para LaTeX e documento em PDF (ver `papel <papel>`_):

.. code-block:: python

   meg.save(r'''
   %summary 


   %problem 

   %answer

   class E12X34__(ExLatex):

       def make_random(s,edict=None):



   ''')


Conteúdo:

.. toctree::
   :maxdepth: 2

   rapido
   sagemath
   paraweb
   papel
   pythonsection
   rewrite
   randomvars 
   referencia 


Atualizações:

**2016/agosto/19**

* o MEGUA foi adaptado ao SMC e por conseguinte este guida teve que ser ajustado.

**2013/novembro/13**

* Adicionada secção sobre :ref:`tabelas`.
* Adicionado secção sobre :ref:`reescrita` de expressões.

**2013/novembro/02** 

* Na visualização do exercício criado vai aparecer "**Escolha:**" quando se visualizam as opções. Recorda-se que estas devem seguir sempre esta ordem: a **correta** e depois as **erradas** até 6 erradas, no máximo.
* Se vai usar logaritmos nos exercícios considere o uso duma nova função: faça ``logb?`` para ver exemplos dum logaritmo que mantém a base inicial e permite fatorização. O ``log`` do Sage e outros sistemas de computação algébrica convertem ``log(15,base=10)`` para ``log(15)/log(10)`` de imediato, sendo log=ln.



Índices e tabelas
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

