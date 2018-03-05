.. main:

MEGUA package for SageMath
==========================



MEGUA is a package for SageMath for creating parametrized exercises in HTML+MathJAX or LaTeX+PDF files. It also works in `<https://CoCalc.com>`_

This tutorials are being revised but now they give a good idea of the topics of this project:

* `Tutorial em português <http://megua.readthedocs.io/pt/latest/>`_
* `Tutorial in english <http://megua.readthedocs.io/en/latest/>`_
* Contact: pedrocruz@ua.pt

Development state: `alpha version <https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha>`_



CoCalc is here `<https://CoCalc.com>`_

.. contents:: Contents and Installation procedures
    :depth: 2




.. payed:

Install on a CoCalc Payed account
---------------------------------

With this type of account it is necessary to turn "internet access" in cocalc project Settings. Then, megua package can be downloaded from github directly with recent updates in "master" branch.


1. Create an account in SMC `<https://CoCalc.com>`_,
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

    $ sage -pip install  --user git+https://github.com/jpedroan/meguacocalc


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



Install on Ubuntu/linux desktop
-------------------------------

This instructions have been revised for Sage 8.1 and Ubuntu 16.04.

1. Download and install `SageMath <http://www.sagemath.org/>`_
::


2. In a terminal do:
::

    $ pip2 install --user git+https://github.com/jpedroan/meguacocalc 
    $ ./sage -sh
    $ cd cd $SAGE_ROOT/
    $ pip2 install requests
    $ cd local/lib/python2.7/site-packages
    $ ln -s /home/<user>/.local/lib/python2.7/site-packages/megua
    $ ln -s /home/<user>/.local/lib/python2.7/site-packages/megua-0.2.dev50+g1c43d5a-py2.7.egg-info
    (Adapt the last filename, please.)
    Exit sage shell CRTL-D


2a. Enter:
::

    $ cd /home/<user>/.local/bin
    $ edit megua
    Change the first line to something like:
    #!/usr/bin/env /<path-to-sage>/sage


3. Run for initialization:
::

    $ megua

4. Change working options with (portuguese: for siacua system see topic above):
::

    $ gedit ~/.megua/conf.py
    Change to:
    --> MEGUA_PLATFORM="DESKTOP"
    --> the last three variables with some strings

5. Create the first exercise targeting a LaTeX exercise
::

    $ megua new E12X34_AddTwoNumbers_001_latex.sage


6. Create a catalog of all exercises:
::

   $ megua catalog


7. More options with:
::

    $ megua help






Memória (português)
-------------------

Começou em 2010, num almoço com uma das principais protagonistas do `PMate <http://pmate.ua.pt>`_. A conversa surgiu sobre  "resoluções" parametrizadas em LaTeX (na altura ainda não disponíveis no sistema pmate).
O SageMath estava na arranque e pensou-se: porque não juntar as duas abordagens?

Em 2011 surgiu uma primeira versão e logo uma nova colega veio dar força ao projeto MEGUA. Este projeto, até agora tem sido uma  biblioteca externa que depende do SageMath, linguagem Python e LaTeX para criar exercícios parametrizados para LaTeX. Entretanto, a chegada do SIACUA (siacua.web.ua.pt) fez com que durante um ano a produção se concentrasse apenas para HTML+MathJAX com a ajuda de mais dois colegas tendo o desenvolvimento em LaTeX/PDF ficado mais parado.

- `Página Institucional do MEGUA <http://cms.ua.pt/megua>`_: people, works, seminars, and related things.
- `Tutorial em portuguê <http://megua.readthedocs.org/pt/latest/>`_: conceitos e prática.

O trabalho foi apresentado em:

- `MEGUA PACKAGE FOR PARAMETERIZED EXERCISES <http://library.iated.org/view/CRUZ2013MEG>`_


**END**
