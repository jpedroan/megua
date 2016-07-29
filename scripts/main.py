# -*- coding: utf-8 -*-
# megua_main.py
"""
Created on Sat Jun  4 11:26:18 2016

@author: jpedro
"""


def main():
    
    print "here am i"
    
    
'''

# MEGUA specific
from os import environ
import jinja2

print "HOME=",environ["HOME"]  # and if is root?

#Create:
#.megua/
#.megua/mconfig.sh  (ir buscar ao template)


######################
# Is this setup running inside SMC?
######################
INSIDE_SMC = False
try:
    from smc_sagews.sage_salvus import salvus
except ImportError as e:
    INSIDE_SMC = e.message == "No module named smc_sagews.sage_salvus"

if INSIDE_SMC:
    create_for_smc()
else:
    create_for_desktop()

# Create Directories

#Save .megua/mconfig.sh

def create_for_smc():
    return "create_for_smc():"
"""
    # ======================
    # SYSTEM CONFIGURATION
    # ======================
    export SAGECMD="$HOME/SageMath/sage"
    export MEGUA_MODULES_DIR="$HOME/megua/megua"
    export MEGUA_TEMPLATE_DIR="$HOME/megua/megua/template/pt_pt"
    #Options: DESKTOP, SMC
    export MEGUA_BASH_ENVIRONMENT="DESKTOP"
    #Options: DESKTOP, SMC (waiting mode: jupyter, sagenb)
    export MEGUA_PLATFORM="DESKTOP"
    #siacua key
    export SIACUA_WEBKEY="oblady"
    #Options: on, off
    export MEGUA_BASH_CALL='off'
    # =================
    # PROJECT CONFIGURATION
    # =================
    export PROJECT_DATABASE="$HOME/all/calculo2/.calculo2.sqlite"
    # Directory where exercises are stored
    export MEGUA_EXERCISE_INPUT="$HOME/all/calculo2"
    # Directory where graphics and results are stored
    export MEGUA_EXERCISE_OUTPUT="$HOME/Downloads/calculo2"
    # Directory for CATALOGS
    export MEGUA_EXERCISE_CATALOG="$HOME/Downloads/calculo2-catalogo"
"""

def create_for_desktop():
    print "create_for_desktop()"
    
"""
# ======================
# SYSTEM CONFIGURATION
# ======================
    export SAGECMD="$HOME/SageMath/sage"
    export MEGUA_MODULES_DIR="$HOME/megua/megua"
    export MEGUA_TEMPLATE_DIR="$HOME/megua/megua/template/pt_pt"
    #Options: DESKTOP, SMC
    export MEGUA_BASH_ENVIRONMENT="DESKTOP"
    #Options: DESKTOP, SMC (waiting mode: jupyter, sagenb)
    export MEGUA_PLATFORM="DESKTOP"
    #siacua key
    export SIACUA_WEBKEY="oblady"
    #Options: on, off
    export MEGUA_BASH_CALL='off'
    # =================
    # PROJECT CONFIGURATION
    # =================
    export PROJECT_DATABASE="$HOME/all/calculo2/.calculo2.sqlite"
    # Directory where exercises are stored
    export MEGUA_EXERCISE_INPUT="$HOME/all/calculo2"
    # Directory where graphics and results are stored
    export MEGUA_EXERCISE_OUTPUT="$HOME/Downloads/calculo2"
    # Directory for CATALOGS
    export MEGUA_EXERCISE_CATALOG="$HOME/Downloads/calculo2-catalogo"

'''