
## Example of a sage bash command

The use of this schema are:

- describe what variables are used by megua package
- a command to test with
 
   ./sage -t <module.py>
 

#!/usr/bin/env bash

# Why this file:
# 1. megua project could benefit from a command line "megua <some command>"
# 2. megua python/sage project needs local variable setup
# 3. A solution is to put configure variables in $HOME/.megua/mconfig.sh


# ======================
# SYSTEM CONFIGURATION
# ======================


export SAGECMD="$HOME/Downloads/sagemath/sage-6.9/sage"

export MEGUA_MODULES_DIR="$HOME/megua/megua"

export MEGUA_TEMPLATE_DIR="$HOME/megua/megua/template/pt_pt"

#Options: desktop, smc
export MEGUA_BASH_ENVIRONMENT="DESKTOP_BASH"

#Options: DESKTOP, SMC (waiting mode: jupyter, sagenb)
export MEGUA_PLATFORM="DESKTOP"

#siacua key
export SIACUA_WEBKEY="oblady"

export COURSE='curso_teste'

export USERNAME_SIACUA='userhere'


# =================
# PROJECT CONFIGURATION
# =================

export PROJECT_DATABASE="_input/.calculo.sqlite"

# Directory where exercises are stored
export MEGUA_EXERCISE_INPUT="_input"

# Directory where graphics and results are stored
export MEGUA_EXERCISE_OUTPUT="_output"

# Directory for CATALOGS
export MEGUA_EXERCISE_CATALOG="_output"


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

