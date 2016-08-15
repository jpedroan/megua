#!/usr/bin/env bash

#Example of a bash call to megua
#with configuration of variables.

source $HOME/.megua/mconfig.sh

# NOTE:
#
# The following variable must be set here and not in "mconfig.sh"
# because it should be turned off below, and this,
# because megua code must know it was called 
# from "megua bash commandline".
#
# BASH completion --- to read:
# http://stackoverflow.com/questions/5570795/how-does-bash-tab-completion-work
# See: /etc/bash_completion.d; 

export MEGUA_BASH_CALL='on'

$SAGECMD -python $MEGUA_MODULES_DIR/c_megua.py "$@"

export MEGUA_BASH_CALL='off'

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
####################     
# This is here only recall how to use MathJax 
# in a bash command that calls megua:
####################

read -d '' MATHJAX_HEADER <<"EOF"
<script type='text/x-mathjax-config'> 
  MathJax.Hub.Config({ 
    extensions: ['tex2jax.js'], 
    jax: ['input/TeX', 'output/HTML-CSS'], 
    tex2jax: { 
      inlineMath: [ ['$','$'], ['\\(','\\)'] ], 
      displayMath: [ ['$$','$$'], ['\\[','\\]'] ], 
      processEscapes: true 
    }, 
    'HTML-CSS': { availableFonts: ['TeX'] } 
  }); 
</script> 
<script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'> 
</script> 
EOF

export MATHJAX_HEADER

$SAGECMD "$@"
"""

