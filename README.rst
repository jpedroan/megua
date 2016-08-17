

MEGUA package for SageMath and SageMath Cloud
=============================================

MEGUA is a package for SageMath for creating parametrized exercises in HTML+MathJAX or LaTeX+PDF files and more formats are planned. 

* `Tutorial em português <http://megua.readthedocs.io/pt/latest/>`_ (contacto: pedrocruz@ua.pt)
* `Tutorial in english <http://megua.readthedocs.io/en/latest/>`_ (contact: pedrocruz@ua.pt)

Development state: `alpha version <https://en.wikipedia.org/wiki/Software_release_life_cycle#Alpha>`_


INSTALL and USE in SageMath Cloud (SMC)
---------------------------------------

The target for the following instructions is SIACUA system (siacua.webua.pt) -- portuguese.

1. Create an acount in SMC and create a project; add other users/authors to this project.
::

2. Create a terminal named BASH.term
::


3a. In the terminal do:
::

    $ sage -pip install  --user git+https://github.com/jpedroan/megua

3b. In the terminal do:
::

    $ open ~/.local/bin/megua
    and change first line to #!/usr/local/bin/sage
    and remove __requirement__ line.

4. Run for initialization:
::

    $ megua

5. Change working options with (siacua needs changes in this file):
::

    $ open ~/.megua/conf.py

6. Create the first exercise for siacua (a worksheet will open)
::

    $ megua new E12X34_AddTwoNumbers_001_siacua.sagews


7. Create a catalog of all exercises:
::

   $ megua catalog
 
   
8. More options with:
::

    $ megua help



9. Contat pedrocruz@ua.pt for more details.
::


HISTORY
-------


Started in 2011, MEGUA is an external package for Sagemath for creating parametrized exercises in HTML+MathJAX or LaTeX PDF files. Software docs strings are in english but the following documentation is in [portuguese](https://pt.wikipedia.org/wiki/L%C3%ADngua_portuguesa):

- `MEGUA PACKAGE FOR PARAMETERIZED EXERCISES <http://cms.ua.pt/megua>`_: people, works, seminars, and related things.
- `Tutorial (portuguese) <http://megua.readthedocs.org/pt/latest/>`_: concepts and practice.

Presented at:

- `MEGUA PACKAGE FOR PARAMETERIZED EXERCISES <http://library.iated.org/view/CRUZ2013MEG>`_ 


There are two branches in this repository:

- **master**: version to be adopted for SageMathCloud use, command-line, etc. 
- **old_megua**: running in a non public server from november 2010 to 2015.


DEVELOPMENT NOTES
-----------------

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


**END**
