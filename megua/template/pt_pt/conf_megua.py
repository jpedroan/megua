# coding=utf-8

"""
conf_megua.py: setup for megua package

This file was copied from
   <packages>/megua/megua/templates/pt_pt/conf_megua.py
to 
   $HOME/.megua/conf.py

"""


import os

# =========================
# ENVIRONMENT CONFIGURATION
# =========================


#Where bash is running
#Options: 
# "DESKTOP_BASH" - if running in a desktop it use "evince ..."
# "SMC_BASH" - if bash is running in smc it can use "open ..."
MEGUA_BASH_ENVIRONMENT="SMC_BASH"


#Where exercises are being build
#Options: 
# "DESKTOP" - means exercises are created using a text editor
# "SMC" - means exercises are created in SAGEWS files
# TODO: waiting other editors: jupyter, (old) sagenb
MEGUA_PLATFORM="SMC"


#For a proper output its important 
#to know where the call was originated
MEGUA_CALLED_FROM_BASH=False



#When exercises are built to use in HTML
MATHJAX_HEADER=r"""
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
"""



# =====================
# PROJECT CONFIGURATION
# =====================

# Directory where exercises are stored 
# Contents of the directory need backups
MEGUA_EXERCISE_INPUT=os.path.join(os.environ["HOME"],"ENUNCIADOS")

# Filename of the database where exercises are stored
# The database file needs backups
PROJECT_DATABASENAME=".MEGUA_DATABASE.sqlite"
PROJECT_DATABASE=os.path.join(MEGUA_EXERCISE_INPUT,PROJECT_DATABASENAME) #full path to database

# Directory for CATALOGS 
# Is not important to make backups but could be useful
MEGUA_EXERCISE_CATALOGS=os.path.join(os.environ["HOME"],"CATALOGOS")

# Directory where graphics and instances of exercies are stored
# This outputs need not a backup but could be consulted in the file system
MEGUA_EXERCISE_OUTPUT=os.path.join(os.environ["HOME"],".megua",".output")



"""
####################
# Use only when "siacua" system http://siacua.web.ua.pt/ is used.     
####################

SIACUA_WEBKEY=
SIACUA_COURSENAME=
SIACUA_USERNAME=
"""



# End.
