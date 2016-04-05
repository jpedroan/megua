#*****************************************************************************
#       Copyright (C) 2011, 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#tirar? from megua.mconfig import *



#Common libaries
from megua.ur import ur
from megua.mathcommon import *

#Book of Exercises
from megua.megbook import MegBook

#Exercise Types
from megua.exbase import ExerciseBase
from megua.exsiacua import ExSiacua
from megua.exlatex import ExLatex

from os import environ
meg = MegBook(environ["PROJECT_DATABASE"])



#
#export MATHJAX_HEADER = "<script type='text/x-mathjax-config'> 
#  MathJax.Hub.Config({ 
#    extensions: ['tex2jax.js'], 
#    jax: ['input/TeX', 'output/HTML-CSS'], 
#    tex2jax: { 
#      inlineMath: [ ['$','$'], ['\\(','\\)'] ], 
#      displayMath: [ ['$$','$$'], ['\\[','\\]'] ], 
#      processEscapes: true 
#    }, 
#    'HTML-CSS': { availableFonts: ['TeX'] } 
#  }); 
#</script> 
#<script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'> 
#</script> 
#"
#
