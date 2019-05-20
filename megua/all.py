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
from megua.ex_amc import ExAMC

# SYSTEM CONFIGURATION
#MEGUA_BASH_ENVIRONMENT=environ["MEGUA_BASH_ENVIRONMENT"]
from os import environ
MEGUA_PLATFORM=environ["MEGUA_PLATFORM"]

if MEGUA_PLATFORM == "WINDOWS":
    import mwindows
    ExLatex.print_instancte = mwindows.windows_exlatex_print_instance
    ExSiacua.print_instancte = mwindows.windows_exsiacua_print_instance
    ExAMC.print_instancte = mwindows.windows_examc_print_instance

elif MEGUA_PLATFORM == "SMC":
    import msmc
    ExLatex.print_instancte = msmc.smc_exlatex_print_instance
    ExSiacua.print_instancte = msmc.smc_exsiacua_print_instance
    ExAMC.print_instancte = msmc.smc_examc_print_instance

elif MEGUA_PLATFORM == "DESKTOP":
    import mdesktop
    ExLatex.print_instancte = mdesktop.desktop_exlatex_print_instance
    ExSiacua.print_instancte = mdesktop.desktop_exsiacua_print_instance
    ExAMC.print_instancte = mdesktop.desktop_examc_print_instance

#Open the project database 
#(see configuration in $HOME/.megua/conf.py or at megua/megua/sage bash)
meg = MegBook()