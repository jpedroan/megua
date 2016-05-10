# coding: utf-8

"""
Could be useful:
- .bashrc: export PATH=$HOME/bin:$HOME/.local/bin:$PATH:$HOME/megua/megua

"""


#PYTHON modules
import os



# Why this file:
# 1. megua project could benefit from a command line "megua <some command>"
# 2. megua python/sage project needs local variable setup
# 3. The solution is to put configure variables in $HOME/.megua/mconfig.sh
# 4. How to read this variable into python ?


# ======================
# SYSTEM CONFIGURATION
# ======================

SAGECMD = os.getenv("SAGECMD")

export MEGUA_MODULES_DIR="$HOME/megua/megua"

export MEGUA_TEMPLATE_DIR = '$HOME/megua/megua/template/pt_pt'

#Options: desktop, smc
export MEGUA_BASH_ENVIRONMENT = "desktop"

#Options: commandline, sagews, and in the "future": jupyter, sagenb, ...
export MEGUA_PLATFORM = "commandline"

#siacua key
export SIACUA_WEBKEY = "oblady"



# =================
# PROJECT CONFIGURATION
# =================

export PROJECT_DATABASE = "$HOME/all/calculo2/.calculo2.sqlite"

# Directory where exercises are stored
export MEGUA_EXERCISE_INPUT = "$HOME/all/calculo2"

# Directory where graphics and results are stored
export MEGUA_EXERCISES_OUTPUT = "$HOME/Downloads/calculo2"


# Directory for CATALOGS
export MEGUA_EXERCISES_CATALOG = "$HOME/Downloads/calculo2-catalogo"


export MATHJAX_HEADER = "<script type='text/x-mathjax-config'>
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
"













#MCONFIG_PATH = os.path.join( os.getenv("HOME"), ".megua/mconfig.sh")
###TODO: improve
##MEGUA modules
#import codecs
#from megua.jinjatemplates import templates
#if not os.path.exists(MCONFIG_PATH):
#    os.makedirs(os.path.join( os.getenv("HOME"), ".megua/"))
#    f = codecs.open(MCONFIG_PATH, mode='w', encoding='utf-8')
#    f.write(templates.render("mconfproject.py"))
#    f.close()
#    print "Change the new '%s' configuration file and restart again." % \
#            MCONFIG_PATH
#    exit()



