# coding=utf-8

r"""
ex_amc.py -- an exercise in LaTeX for use in AMC.



AUTHORS:

- Pedro Cruz (2016-03): first modifications for use in SMC.
- Pedro Cruz (2016-08): firts version of exercises for AMC?

EXAMPLES:

::
  
    sage -t ex_amc.py

Creation a LaTeX exercise:

::
        
       sage: from megua.all import *
       sage: meg = MegBook(r'_input/megbook.sqlite') 
       sage: meg.save(r'''
       ....: %Summary Análise Exploratória de Dados; Medidas; Média
       ....:   #TODO: mudar para PT:
       ....: Here one can write few words, keywords about the exercise.
       ....: For example, the subject, MSC code, and so on.
       ....:   
       ....: %Problem Média da Concentração Sérica
       ....: 
       ....: Considere o seguinte conjunto de dados de nível concentração sérica (em g / ml) de Gentamicina no sangue  recolhido a partir de uma amostra casual de $ssize$ ovelhas:
       ....: \begin{center}
       ....: \begin{tabular}{|l|r|}
       ....:   \hline
       ....: concentração sérica (g/ml)	& sample \\
       ....:   \hline
       ....: \end{tabular}
       ....: \end{center}
       ....: A média é, aproximadamente,
       ....:   \begin{choices}
       ....:   \correctchoice{res1}
       ....:   \wrongchoice{res2}
       ....:   \wrongchoice{res3}
       ....:   \wrongchoice{res4}
       ....: \end{choices}
       ....:  
       ....: %Answer
       ....:  
       ....:  A média calcula-se somando e dividindo pelo número de elementos.
       ....: 
       ....: class E28E28_aed_medidas_001(ExAMC):
       ....:  
       ....:     def make_random(s,edict=None):
       ....:         # sample size
       ....:         s.ssize = ZZ.random_element(5,15)
       ....:         sample1 = [ZZ.random_element(15,40) for _ in xrange(s.ssize)]
       ....:         s.sample = r'\  '.join([str(num) for num in sample1])
       ....:         s.res1 = round( sum(sample1)/s.ssize, 2) #correct
       ....:         s.res2 = round( 2*sum(sample1)/s.ssize, 2) #wrong
       ....:         s.res3 = round( 0.5*sum(sample1)/s.ssize, 2) #wrong
       ....:         s.res4 = round( 10+sum(sample1)/s.ssize, 2) #wrong
       ....: ''')
       ex_amc.py module say: evince  _output/E28E28_aed_medidas_001/E28E28_aed_medidas_001.pdf

"""


#*****************************************************************************
#       Copyright (C) 2011,2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#PYTHON modules
import os
import subprocess
import shutil
import sys

#MEGUA modules
from megua.platex import pcompile
from megua.exbase import ExerciseBase
from megua.jinjatemplates import templates
from megua.megoptions import MEGUA_PLATFORM,MEGUA_TEMPLATE_DIR


class ExAMC(ExerciseBase):
   
   #TODO: review all "amc" in templates/pt_pt
   
    def print_instance(self):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        #Use jinja2 template to generate LaTeX.
        latex_string = templates.render("examc_print_instance.tex",
            unique_name=self.unique_name(),
            ekey = self.ekey,
            summtxt=self.summary(),
            probtxt=self.problem(),
            answtxt=self.answer(),
         )

        #copy amc.sty to the working dir:
        shutil.copy(os.path.join(MEGUA_TEMPLATE_DIR,"amcpt.sty"), self.wd_fullpath)
        
        pcompile(latex_string,self.wd_fullpath,self.unique_name())

        EXERCISE_TEX_PATHNAME = os.path.join(self.wd_fullpath, self.unique_name()+'.tex')
        EXERCISE_PDF_PATHNAME = os.path.join(self.wd_fullpath, self.unique_name()+'.pdf')

        if MEGUA_PLATFORM=='SMC':
            sys.path.append('/cocalc/lib/python2.7/site-packages')
            from smc_sagews.sage_salvus import salvus
            salvus.file(EXERCISE_PDF_PATHNAME,show=True,raw=True); 
            print ("\n")
            salvus.file(EXERCISE_TEX_PATHNAME,show=True,raw=True); 
            print ("\n")
            salvus.open_tab(EXERCISE_PDF_PATHNAME)
        elif MEGUA_PLATFORM=='DESKTOP':
            print ("ex_amc.py module say: evince ",EXERCISE_PDF_PATHNAME)
            subprocess.Popen(["evince",EXERCISE_PDF_PATHNAME])
        else:
            print ("ex_amc module say: MEGUA_PLATFORM must be properly configured at $HOME/.megua/conf.py")



