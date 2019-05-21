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
from megua.megoptions import MEGUA_PLATFORM

if MEGUA_PLATFORM == "WINDOWS":
    import megua.mwindows as mwindows
    ExLatex.conf_print_instance = mwindows.conf_exlatex_print_instance
    ExSiacua.conf_print_instance = mwindows.conf_exsiacua_print_instance
    ExSiacua.conf__siacua_send = mwindows.conf__siacua_send
    ExSiacua.conf_siacuapreview = mwindows.conf_siacuapreview
    ExAMC.conf_print_instance = mwindows.conf_examc_print_instance
    MegBook.conf_catalog = mwindows.conf_catalog
    MegBook.conf_fast_exam_siacua = mwindows.conf_fast_exam_siacua
    MegBook.conf_latex_document = mwindows.conf_latex_document
    MegBook.conf_new_exercise = mwindows.conf_new_exercise
    MegBook.conf_replicate_exercise = mwindows.conf_replicate_exercise
    MegBook.set_current_exercise = mwindows.set_current_exercise
    MegBook.conf_set_current_exercise = mwindows.conf_set_current_exercise

elif MEGUA_PLATFORM == "SMC":
    import megua.msmc as msmc
    ExLatex.conf_print_instance = msmc.conf_exlatex_print_instance
    ExSiacua.conf_print_instance = msmc.conf_exsiacua_print_instance
    ExSiacua.conf__siacua_send = msmc.conf__siacua_send
    ExSiacua.conf_siacuapreview = msmc.conf_siacuapreview
    ExAMC.conf_print_instance = msmc.conf_examc_print_instance
    MegBook.conf_catalog = msmc.conf_catalog
    MegBook.conf_fast_exam_siacua = msmc.conf_fast_exam_siacua
    MegBook.conf_latex_document = msmc.conf_latex_document
    MegBook.conf_new_exercise = msmc.conf_new_exercise
    MegBook.conf_replicate_exercise = msmc.conf_replicate_exercise
    MegBook.conf_set_current_exercise = msmc.conf_set_current_exercise

elif MEGUA_PLATFORM == "DESKTOP":
    import megua.mdesktop as mdesktop
    ExLatex.conf_print_instance = mdesktop.conf_exlatex_print_instance
    ExSiacua.conf_print_instance = mdesktop.conf_exsiacua_print_instance
    ExSiacua.conf__siacua_send = mdesktop.conf__siacua_send
    ExSiacua.conf_siacuapreview = mdesktop.conf_siacuapreview
    ExAMC.conf_print_instance = mdesktop.conf_examc_print_instance
    MegBook.conf_catalog = mdesktop.conf_catalog
    MegBook.conf_fast_exam_siacua = mdesktop.conf_fast_exam_siacua
    MegBook.conf_latex_document = mdesktop.conf_latex_document
    MegBook.conf_new_exercise = mdesktop.conf_new_exercise
    MegBook.conf_replicate_exercise = mdesktop.conf_replicate_exercise
    MegBook.conf_set_current_exercise = mdesktop.conf_set_current_exercise

#Open the project database 
#(see configuration in $HOME/.megua/conf.py or at megua/megua/sage bash)
meg = MegBook()
    