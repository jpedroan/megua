.. main:

MEGUA package for SageMath and SageMath Cloud
=============================================



MEGUA is a package for SageMath for creating parametrized exercises in HTML+MathJAX or LaTeX+PDF files (more formats are planned). 

This tutorials are being revised but now they give a good ideia of the topics of this project:

* `Tutorial em português <http://megua.readthedocs.io/pt/latest/>`_
* `Tutorial in english <http://megua.readthedocs.io/en/latest/>`_ 
* Contact: pedrocruz@ua.pt

Development state: `alpha version <https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha>`_


Instalation procedures:

1. (português) Sistema SIACUA com uma conta Free no SMC 
2. Free account in SMC `<https://cloud.sagemath.com>`_
3. Payed account on SMC  `<https://cloud.sagemath.com>`_
4. Ubuntu/linux desktop

SageMath Cloud (SMC) is `<https://cloud.sagemath.com>`_

.. contents:: Contents and Instalation procedures
    :depth: 2



.. _siacua:

MEGUA para o sistema SIACUA (português)
---------------------------------------

As instruções seguintes são para o sistema SIACUA (siacua.web.ua.pt) e usando uma conta não paga no SMC `<https://cloud.sagemath.com>`_. Se tiver uma conta paga siga primeiro as instruções para esse caso mencionadas acima.

Neste tipo de conta, o usuário não tem acesso direto à internet estando dentro da máquina virtual do SMC. Neste caso deve baixar o ficheiro do "MEGUA package" para o seu computador a partir deste site `PYPi <https://pypi.python.org/pypi/megua>`_ e depois fazer o "upload" desse ficheiro no sistema SMC como se descreve de seguida nas detalhadas instruções.

**Importante**: o sistema `SIACUA <http://siacua.web.ua.pt>`_ requer uma conta no sistema e um "curso" que para os exercicios. Contacte luisd@ua.pt para essa informação antes de avançar. Pode sempre adiar a configuração destes passos e começar a desenvolver exercícios.


1. Baixar o "MEGUA package" para o seu computador de `PYPi <https://pypi.python.org/pypi/megua>`_ usando o botão VERDE. Guarde o ficheiro no seu computador.
::


2. Crie uma conta no SMC `<https://cloud.sagemath.com>`_, 
::


- depois crie um projeto; 
- outros usuários que queiram paricipar do projeto devem criar uma conta;
- o "dono" do projeto deve depois adicioná-los (botão Settings).


3. Criar um "terminal" com o nome BASH
::


- Pressione o botão "+NEW"
- Mude o nome para "BASH" (onde esta uma data e hora comprida)
- Pressione o botão ">_Terminal"


4. Hora de carregar o pacote MEGUA: selecione, novamente, o botão "+NEW" e procure "Drop files" em baixo. Carregue nessa caixa e carregue o ficheiro no seu computador com o "MEGUA package".
::



5. Selecione FILES e depois "BASH.term" e faça:
::

    $ sage -pip install  --user megua<PRESS TAB key>
    (o nome completo do ficheiro deve aparecer)



6. Execute este comando para iniciar o megua:
::

    $ megua


7. O SIACUA requer o nome do curso, um username e uma password de sistema. Para isso deve ser editar 'conf.py' com:
::

    $ open ~/.megua/conf.py
    (contacte luisd@ua.pt para mais informações).


8. Crie um orimeiro exercício para o SIACUA (esta etapa abre uma janela com o novo exercício)
::

    $ megua new E12X34_AddTwoNumbers_001_siacua.sagews
    (note o final do ficheiro: "_siacua.sagews" )


9. Pode, ainda, criar exercícios para LaTeX (compilados com pdfltex) para usar em papel
::

    $ megua new E12X34_AddTwoNumbers_001_latex.sagews
    (note o final do ficheiro: "_latex.sagews" )



10. Para criar
::

   $ megua catalog
   (mostra todos os exercícios criados para siacua ou latex)

  
11. Mais opções futuras com:
::

    $ megua help




.. nonpayed:

Install on a SMC Free account
-----------------------------

With this type of account the user does not have "internet access" using command-line or scripts but can use manual upload and download of files. Package MEGUA must be downloaded to your computer from `PYPi <https://pypi.python.org/pypi/megua>`_ and then uploaded to project area as the folloing instructions suggest.


1. Download MEGUA package to your computer from `PYPi <https://pypi.python.org/pypi/megua>`_ using the green button. Save the file in your computer.
::

2. Create an account in SMC `<https://cloud.sagemath.com>`_, 
::


- then create a project; 
- other users must create an account 
- and then add them to this project.


3. Create a terminal named BASH.term
::


- Button "+NEW"
- Change name to "BASH"
- Press ">_Terminal" button


4. Select, again, the +NEW button and go to the "Drop files" box below (you can press here or move the file to this box). Upload the MEGUA package (at the moment in your computer).
::


5. In the terminal do:
::

    $ sage -pip install  --user megua<PRESS TAB key>
    (the compplete filename should be shown)


6. Run for initialization:
::

    $ megua


7. Change working options with (portuguese: for siacua system see bellow):
::

    $ open ~/.megua/conf.py


8. Create the first exercise targeting LaTeX (a worksheet will open)
::

    $ megua new E12X34_AddTwoNumbers_001_latex.sagews


9. Create a catalog of all exercises:
::

   $ megua catalog
 
  
   
10. More options with:
::

    $ megua help






.. payed:

Install on a SMC Payed account
------------------------------

With this type of account it is necessary to turn "internet access" in Setting and MEGUA could be downloaded from github directly with recent updates in "master" branch.


1. Create an account in SMC `<https://cloud.sagemath.com>`_, 
::


- then create a project; 
- other users must create an account 
- and then add them to this project.


2. Create a terminal named BASH.term
::


- Button "+NEW"
- Change name to "BASH"
- Press ">_Terminal" button


3. In the terminal do:
::

    $ sage -pip install  --user git+https://github.com/jpedroan/megua


4. Run for initialization:
::

    $ megua

5. Change working options with (portuguese: for siacua system see bellow):
::

    $ open ~/.megua/conf.py

6. Create the first exercise targeting LaTeX (a worksheet will open)
::

    $ megua new E12X34_AddTwoNumbers_001_latex.sagews


7. Create a catalog of all exercises:
::

   $ megua catalog
 
   
8. More options with:
::

    $ megua help


 
Ubuntu/linux desktop
--------------------


If you choose this option then please use what is necessary from "Install on Payed account on SMC" if you have internet access in your linux box.




Development Notes
-----------------


There are two branches in this repository:

- **master**: version to be adopted for SageMathCloud use, command-line, etc. 
- **old_megua**: running in a non public server from november 2010 to 2015.


* etoolbox.sty: sudo apt-get install texlive-latex-extra

* salvus: /projects/sage/sage-6.10/local/lib/python2.7/site-packages/smc_sagews

* from smc_sagews.sage_salvus import salvus #Functions: salvus.file(), salvus.html()

* sage_server.py: contains definitions of "def file()" and "def html()", see useful arguments

* decorators dynamically alter the functionality of a function, method or class without having to directly use subclasses, http://thecodeship.com/patterns/guide-to-python-function-decorators/

* http://doc.sagemath.org/html/en/reference/calculus/sage/symbolic/function_factory.html


**Answered questions by SMC team**

- startup file for sagews 

    - https://groups.google.com/forum/#!topic/sage-cloud/L-9QwvlfnvY
    - https://github.com/sagemathinc/smc/issues/369

- about "salvus"

HTML and Links

  - https://groups.google.com/forum/#!searchin/sage-cloud/salvus/sage-cloud/dg4mhp99cOg/9LiiIdEonlYJ

Images

   - https://groups.google.com/forum/#!searchin/sage-cloud/salvus/sage-cloud/-nChfU76j7Q/D-y8rIPfUngJ


   
Memória (português)
-------------------

Começou em 2010, num almoço no Snack, uma das principais protagonistas do `PMate <http://pmate.ua.pt>`_ e a conversa era sobre resoluções paranetrizadas em LaTeX (na altura ainda não disponíveis no sistema pmate). O SageMath estava na pré-adolescência e pensou-se: porque não juntar os dois temas.

Em 2011 surgiu uma primeira abordagem e uma nova colega veio dar força ao projeto MEGUA. Este projeto, até agora tem sido uma  biblioteca externa que depende do SageMath, linguagem Python e LaTeX para criar exercícios parametrizados para LaTeX. Entretanto, a chegada do SIACUA (siacua.web.ua.pt) fez com que durante um ano a produção se concentrasse apenas para HTML+MathJAX com a ajuda de mais dois colegas tendo o desenvolvimento em LaTeX/PDF ficado mais parado. 

- `Página Institucional do MEGUA <http://cms.ua.pt/megua>`_: people, works, seminars, and related things.
- `Tutorial em portuguê <http://megua.readthedocs.org/pt/latest/>`_: conceitos e prática.

O trabalho foi apresentado em:

- `MEGUA PACKAGE FOR PARAMETERIZED EXERCISES <http://library.iated.org/view/CRUZ2013MEG>`_ 


**END**
