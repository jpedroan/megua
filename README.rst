

MEGUA package
=============

**Alpha version**

Started in 2011, MEGUA is an external package for Sagemath for creating parametrized exercises in HTML+MathJAX or LaTeX PDF files. Software docs strings are in english but the following documentation is in [portuguese](https://pt.wikipedia.org/wiki/L%C3%ADngua_portuguesa):

- `MEGUA PACKAGE FOR PARAMETERIZED EXERCISES <http://cms.ua.pt/megua>`_: people, works, seminars, and related things.
- `Tutorial (portuguese) <http://megua.readthedocs.org/pt/latest/>`_: concepts and practice.



HISTORY
-------

Presented at:

- `MEGUA PACKAGE FOR PARAMETERIZED EXERCISES <http://library.iated.org/view/CRUZ2013MEG>`_ 


There are two branches in this repository:

- **master**: version to be adopted for SageMathCloud use, command-line, etc. 
- **old_megua**: running in a non public server from november 2010 to 2015 (well 5 years...!!).

DEVELOP
-------

* etoolbox.sty: sudo apt-get install texlive-latex-extra

* salvus: /projects/sage/sage-6.10/local/lib/python2.7/site-packages/smc_sagews

* from smc_sagews.sage_salvus import salvus #Functions: salvus.file(), salvus.html()

* sage_server.py: contains definitions of "def file()" and "def html()", see useful arguments

* decorators dynamically alter the functionality of a function, method or class without having to directly use subclasses, http://thecodeship.com/patterns/guide-to-python-function-decorators/

* http://doc.sagemath.org/html/en/reference/calculus/sage/symbolic/function_factory.html


Answered questions
------------------

- startup file for sagews 

https://groups.google.com/forum/#!topic/sage-cloud/L-9QwvlfnvY

que se converteu num ticket:

https://github.com/sagemathinc/smc/issues/369


## Sobre o salvus

HTML e Links

https://groups.google.com/forum/#!searchin/sage-cloud/salvus/sage-cloud/dg4mhp99cOg/9LiiIdEonlYJ

Imagens

https://groups.google.com/forum/#!searchin/sage-cloud/salvus/sage-cloud/-nChfU76j7Q/D-y8rIPfUngJ




**FIM**

