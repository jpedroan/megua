
.. _userguide:

User Guide
==========

MEGUA acronym stands for 'Mathematics Exercise Generator' and 'UA' stand for University of Aveiro (Portugal). 

It's a package for |sagemath|_ to create and edit a personal 
or group databases of parameterized exercise templates written in LaTeX_ typeset. 
The package is ready for command line use or Sage notebook use. 
    
Currently, MEGUA operations are:

1. Open one or more local databases.
2. Produce, edit and delete exercises from it.
3. Search for one or a group of exercises.
4. Produce a PDF document from a selected list of exercises (and the tex file).

To create an exercise, elementary programming skills are needed. |sagemath|_ uses Python_ language 
with very little preparsing. Currently MEGUA uses LaTeX_ and you have here_ a collection of introductory level tutorials.

One can use the command-line of |sagemath|_ (on a Linux environment) or the Sage notebook front-end, usually in a server.

.. |sagemath| replace:: *Sage math*
.. _sagemath: http://www.sagemath.org
.. _Python: http://www.python.org
.. _LaTeX: http://www.tug.org
.. _here: http://www.tug.org/begin.html

The following block is a full exercise template:

.. code-block:: latex

   %Summary Section; Subsection; Subsubsection
   Here one can write few words, keywords about the exercise.
   For example, the subject, MSC code, and so on.

   %Problem Some Name Here
   What is the primitive of $ap x + bp@()$ ?

   %Answer
   The answer is $prim+C$, for $C in \mathbb{R}$.

.. code-block:: python

   class E28E28_pdirect_001(Exercise):

       def make_random(s):

           s.ap = ZZ.random_element(-4,4)
           s.bp = RR.random_element(-4,4)

       def solve(s):

           x=SR.var('x')
           s.prim = integrate(s.ap * x + s.bp,x)

First part is the exercise LaTeX_ part and the second part is the Python_ part (Sage math preparses_ mathematics notation).


.. _preparses: http://www.sagemath.org/doc/reference/sage/misc/preparser.html


The LaTeX part has 3 sections marked by respective tags:

Tag **%Summary**

    Here one can write few words, keywords about the exercise.
    For example, the subject, MSC code, and so on. Or inline latex $equations$.

    Text in this field can help searching for a specific exercise. 
    This part is usually hidden from a student to whom this exercise is presented.

    In front of tag **%summary** one can add sections as if this exercise is taken from a section of a book.

Tag **%Problem** and tag **%Answer**

    Problem and answer are separated text parts.
    Textual parts may contain parameters to be changed by values on the final text. 
    These parameters are identified by letters or letters and numbers and they will be replaced by some LaTeX_ expression (formula, numbers, etc.). 

    In the above example, `ap` and `bp@()` are parameters (the second has a output filter @()). 

    In front of tag **%problem** one can write an suggestive name for the exercise.

How does this work? 

1. Textual parts contains **parameters** where a value, math expression, etc is to appear; As seen in the example above:

   *  in the expression ``ap x + bp@()`` parameters could be ``ap``, ``x`` and a filtered one ``bp@()``.

2. In the *make_random* function one set a Sage value or expression to the parameter.  As seen in the example:

   * ``s.a = ZZ.random_element()``: a random integer value is given to ``ap``;
   * ``s.b = RR.random_element(-4,4)``: a random real value is given to ``bp``;
   * ``s.prim = integrate(s.ap * x + s.bp,x)``: parameter ``prim`` will get the integration result on variable ``x``.

3. The Sage Math value, formula, or number is converted to its LaTeX representation and replaced on the parameter place.


.. _megvariables: 


Parameters can be **filtered** as the following examples show. Consider these variables::

   name1 = -12.123456``
   name2 = -34.32
   name3 = 1

The following table summaries replacements:

.. http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables

+-----------------------------+--------------------+----------------------------------------+
| parameter                   | after substitution | comment                                |
+=============================+====================+========================================+
| name1                       |  -12.123456        | straight replacement.                  |
+-----------------------------+--------------------+----------------------------------------+
| name1\@()                   |  (-12.123456)      | put (...) around number if negative.   |
+-----------------------------+--------------------+----------------------------------------+
| name1\@f{2.3g}              | -12.1              | use printf_ notation (C users).        | 
+-----------------------------+--------------------+----------------------------------------+
| name2\@s{sin}               | 0.42857465435      | call 1 argument function on parameter. |
+-----------------------------+--------------------+----------------------------------------+
| name3\@c{"text0", "text1"}  | text1              | choose one string of the list.         |
+-----------------------------+--------------------+----------------------------------------+

.. _printf: http://docs.python.org/library/stdtypes.html#string-formatting


Team work
---------

Sage notebook provides a natural and graphical way for team work were users are able to share worksheets. 
We recomend using a worksheet for each exercise template for better organization. 

Using it via Linux command line has the means well known to programmers: each text file 
could be an exercise template, everything organized in folders and a versioning program 
could be use to share work and keep records of changes. Note for current version: to use this package on 
a server the administrator should install it locally (currently, a single user cannot install it).


Use from Sage notebook
----------------------

First define the database and the ``megua`` object::

   from megua.all import *
   meg = MegBook(r'/home/user/a_meg_base.sqlite')

Then, in a new cell, the command::

   meg.save(...)

is used to save exercises in ``meg`` database. Saving an exercise template on the database is only allowed if:

1. The textual part, in LaTex, makes no compilation compilation errors.
2. It has no python syntactical error.
3. Parameters are replaced by several random values in order to possible detect mistakes in function algorithm.

If some one of the above errors appear then user is warned.

A possible of work flow is:

1. Create each different exercise in its own worksheet. In the same worksheet execute a command to save the exercise to the database.
2. After all verifications on the exercise one can store a copy on the local disk (as sws file) and archive it on the notebook. 
3. Recall the exercise by searching the database (using exercise name or by words).

If the objective is to build only a few exercises then using the same worksheet is a good solution. 

**Creating and editing a template**

In a new cell of an opened worksheet do, as in the example:

.. code-block:: python

   #START of the cell  ------------------
   
   meg.save( r'''

   %Summary Section name; Subsection name; Subsubsection name

   Here one can write few words, keywords about the exercise.
   For example, the subject, MSC code, and so on.

   %Problem Suggestive name

   What is the primitive of $ap x + bp@()$ ?

   %Answer

   The answer is $prim+C$, for $C in \mathbb{R}$.

   class E28E28_pdirect_001(Exercise):

       def make_random(s):

           s.ap = ZZ.random_element(-4,4)
           s.bp = RR.random_element(-4,4)

       def solve(s):

           x=SR.var('x')
           s.prim = integrate(s.ap * x + s.bp,x)

    ''')

    #END of the cell ------------------


Previously we address the content of the template of the exercise.

Now we describe how to declare it in the Sage notebook.

1. Notice the ``r'''`` in the top of the cell. This defines a string containing with both TeX and Python parts. 
The raw string starts with ``r'''`` and ends with ``'''`` and contains the LaTeX in the beginning and the Python_ coding for the exercise.
2. The exercise must have a name. The recommended pattern for names is::  
 
   E<MSC code>_name_number

where codes are taken from MSC_ classification, ``name`` some suggestive name and a numeration scheme like 001, 002, etc, as 
more exercises could share same name. All connected by an underscore ``_``.


.. _MSC: http://www.ams.org/mathscinet/msc/msc2010.html

**Notes:**

To produce new exercise from the template there is the command::

   meg.new("E28E28_pdirect_001",ekey=2)

where ``"E28E28_pdirect_001"`` is the exercise name and ``ekey=2`` is a number to generate a set of values for parameters.



Use from Text files
-------------------


Developing a new exercise:

1. Edit a new file, named for example, "E28E28_pdirect_001.sage" and use this syntax:

.. code-block:: python    

   from megua.all import *
   meg = MegBook(r'/home/user/a_meg_base.sqlite')
   meg.save( r'''

      exercise TeX and Sage/Python definition (see above E28E28_pdirect_001)

   ''')

2. At shell prompt do:

   sage E28E28_pdirect_001.sage


3. Check E28E28_pdirect_001.tex and E28E28_pdirect_001.pdf files for an example.

 


Creating booklets
-----------------

The title word "books" could be a little ostentatious! Maybe booklets, book of exercises, exercise sheets, and so on.

One can join several exercises (template or instances) on a PDF. We need two templates: the 'row' template for each exercise --
what are the columns we want to appear in PDF, and the 'book' template -- what packages, LaTeX style, sections and exercise we want to
show.

In what follows, note that ``"""`` mark the beginning and end of the string in Python_. In the first example:


.. code-block:: python    

   #Full information from an exercise template

   all_details = """\\textbf{Name:}~\\verb+{{ exname }}+ \
   \n\n \\textbf{Summary} \n\n {{ summary }} \
   \n\n \\textbf{Problem template} \n\n {{ problemtemplate }} \
   \n\n \\textbf{Answer template} \n\n {{ answertemplate }} \
   \n\n \\begin{verbatim}\n{{ codetxt }}\n\\end{verbatim} \
   \n\n \\textbf{Problem Example } \n\n {{ problem }} \
   \n\n \\textbf{Answer Example } \n\n {{ answer }} \
   \n\n"""

we see the keyword names of every information that is stored about an exercise:

``exname``
   The given name to the exercise. Example ``E62L20_stochastic_001``.

``summary``
   The textual summary

``problemtemplate``
   The original problem text (template) without substitutions.

``answertemplate``
   The original answer text (template) without substitutions.

``problem``
   One sample of problem text with variables replace by proper values according to *make_random* function.

``answer``
   The related answer text with variables replace by proper values according to *solve* function.


Then we must define what the book look like using another template:

.. code-block:: latex

   #
   # Exemplo de ficheiro latex a ser usado como molde.
   #

   book_template = r"""
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

Now we create the book using the string ``all_details`` that indicates what we want to show from each exercise and the string template 
``book_template``:


.. code-block:: python

   # Producing a book
   meg.template_fromstring(book_template,rowtemplate=all_details)


Another configurations
^^^^^^^^^^^^^^^^^^^^^^

Short configuration:

.. code-block:: python

   #Configuração curta: mostra apenas problem e answer

   modelo_curto = """\
   \n\n \\textbf{Problem Example } \n\n {{ problem }} \
   \n\n \\textbf{Answer Example } \n\n {{ answer }} \
   \n\n"""


With LaTeX package "exercise":


.. code-block:: python

   # 
   # Using \usepackage{exercise}
   #

   model_exercicelist= """\
   \n\n \\Exercise \n {{ problem }} \
   \n\n \\Answer \n {{ answer }} \
   \n\n"""
   #proper for exercises at start and answers at the end.

   #
   # main latex file
   #

   file_exercicelist = r"""
   \documentclass{article}

   \usepackage[utf8]{inputenc}

   \usepackage{amsfonts}

   % ================
   % Exercise Package
   % ================
   \usepackage[lastexercise,answerdelayed]{exercise}
   \renewcommand{\AnswerListHeader}{\textbf{Resposta do ex.~\ExerciseHeaderNB\ ---\ }}
   \renewcommand{\theExercise}{\arabic{section}.\arabic{Exercise}} %texto da numeracao de cada exercicio
   \renewcounter{Exercise}[section] %permite re-iniciar Exercise=1 a cada chapter.

   \begin{document}

   %Isto é um teste.

   \section{Problemas}

   \begin{ExerciseList}

   {{ put_here("E26A36_PImediatas_001") }}

   {{ put_here("E26A36_PElementosSimples_001") }}

   {{ put_here("E26A36_PRacionais_001") }}

   \end{ExerciseList}


   \section{Soluções}

   \shipoutAnswer


   \end{document}
   """

   #
   #comando que gera o pdf e tex usando os moldes acima.
   #

   meg.template_fromstring(ficha_exercicelist,rowtemplate=modelo_exercicelist)



