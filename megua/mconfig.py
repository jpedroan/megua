# coding=utf-8

"""

Could be useful:

- .bashrc:export PATH=$HOME/bin:$HOME/.local/bin:$PATH:$HOME/megua/megua

"""


#PYTHON modules
import os




MCONFIG_PATH = os.path.join( os.getenv("HOME"), ".megua/mconfig.py")


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



execfile(MCONFIG_PATH)

#
##===================
##Sample Config File
##===================
#
#MEGUA_TEMPLATE_DIR = '/home/jpedro/megua/megua/template/pt_pt'
#
#===========#
##===========
##
#projectname = 'calculo2'
#
## =====================
## SIACUA CONFIGURATION
## =====================
#SIACUA_WEBKEY = "oblady"
#
#
## =============
##
## commandline, sagews, jupyter, sagenb, ...
#MEGUA_PLATFORM = "commandline"
##MEGUA_MODULES_DIR = "/home/jpedro/all/megua/megua"
#
#
## ===
## Directory where exercises are stored
## ===
#MEGUA_EXERCISE_INPUT = os.path.join(os.getenv("HOME"),"all/calculo2")
#if not os.path.exists(MEGUA_EXERCISE_INPUT):
#    os.makedirs(MEGUA_EXERCISE_INPUT)
#
#
## ===
## Directory where graphics and results are stored
## ===
#MEGUA_EXERCISES_OUTPUT = os.path.join(os.getenv("HOME"),"Downloads/calculo2")
#if not os.path.exists(MEGUA_EXERCISES_OUTPUT):
#    os.makedirs(MEGUA_EXERCISES_OUTPUT)
#
#
## ===
## Directory for CATALOGS
## ===
#MEGUA_EXERCISES_CATALOG = os.path.join(os.getenv("HOME"),"Downloads/Calculo2Catalogo")
#if not os.path.exists(MEGUA_EXERCISES_CATALOG):
#    os.makedirs(MEGUA_EXERCISES_CATALOG)
#
#
#
#MATHJAX_HEADER = r'''
#<script type="text/x-mathjax-config">
#  MathJax.Hub.Config({
#    extensions: ["tex2jax.js"],
#    jax: ["input/TeX", "output/HTML-CSS"],
#    tex2jax: {
#      inlineMath: [ ['$','$'], ["\\(","\\)"] ],
#      displayMath: [ ['$$','$$'], ["\\[","\\]"] ],
#      processEscapes: true
#    },
#    "HTML-CSS": { availableFonts: ["TeX"] }
#  });
#</script>
#<script src='https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML'>
#</script>
#'''
#
#
#



