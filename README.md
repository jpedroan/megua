

MEGUA package
=============

**Alpha version**

Presented at:
<a href="http://library.iated.org/view/CRUZ2013MEG" title="MEGUA PACKAGE FOR PARAMETERIZED EXERCISES">MEGUA PACKAGE FOR PARAMETERIZED EXERCISES</a>


Started in 2011, MEGUA is an external package for Sagemath for creating parametrized exercises in HTML+MathJAX or LaTeX PDF files. Software docs strings are in english but the following documentation is in [portuguese](https://pt.wikipedia.org/wiki/L%C3%ADngua_portuguesa):

- <a href="http://cms.ua.pt/megua" title="MEGUA PACKAGE FOR PARAMETERIZED EXERCISES">Management</a>: people, works, seminars, and related things.
- <a href="http://megua.readthedocs.org/pt/latest/" title="TUTORIAL DO MEGUA">MEGUA Tutorial</a>: concepts and practice.

There are two branches in this repository:

- **old_megua**: running in a non public server from november 2010 to 2015 (well 5 years...!!).
- **master**: version to be adopted for SageMathCloud use, command-line, etc. 

DEVELOP
-------

* aalib: download, gunzip, untar
* aalib: sage -python setup.py install 
* etoolbox.sty: sudo apt-get install texlive-latex-extra
* salvus: /projects/sage/sage-6.10/local/lib/python2.7/site-packages/smc_sagews
* from smc_sagews.sage_salvus import salvus #Functions: salvus.file(), salvus.html()
* sage_server.py: contains definitions of "def file()" and "def html()", see useful arguments
* decorators dynamically alter the functionality of a function, method or class without having to directly use subclasses, http://thecodeship.com/patterns/guide-to-python-function-decorators/
* ascii art http://doc.sagemath.org/html/en/reference/misc/sage/typeset/character_art.html



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



## Packages

**Instalar packages**

**user-installed packages in sage worksheets vs. sage command line**

https://groups.google.com/forum/#!searchin/sage-cloud/package/sage-cloud/ps_6eV1ljjE/uHQEiMzIfwMJ

**Own Module**

https://github.com/sagemathinc/smc/wiki/FAQ#own-module

**Método preferido**

Seguir o comando aqui:

- https://docs.python.org/2/install/#alternate-installation-the-user-scheme

Depois apagar o modulo instalado e fazer:

- $ cd /projects/69b82f4f-dc00-498d-817e-f3575041e14e/.local/lib/python2.7/site-packages
- $ ln -s /project-folder/megua/megua

e o pacote ficará disponível tanto para command line como para worksheet.



**FIM**

