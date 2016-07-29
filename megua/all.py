#*****************************************************************************
#       Copyright (C) 2011, 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#Common libaries
from megua.ur import ur
from megua.mathcommon import *

#Book of Exercises
from megua.megbook import MegBook

#Exercise Types
from megua.exbase import ExerciseBase
from megua.exsiacua import ExSiacua
from megua.exlatex import ExLatex

#Open the project database 
#(see configuration in $HOME/.megua/conf.py or at megua/megua/sage bash)
meg = MegBook()

