# -*- coding: utf-8 -*-

r"""
megoptions -- options like directories.


AUTHORS:

- Pedro Cruz (2016-06): first modifications for use in SMC.

This file keeps environment variables from the following sources:

* bash environment variables: it is useful to start megua with local variables, 
for example, for a certain database or to test code using "sage" bash
script inside megua/megua.


* in a python script located in:

       PATH_CONF_PY = path.join(environ["HOME"],".megua","conf.py")
       
if it does not exist, it will be created as a copy from conf.py in templates 
directory and then could be changed by user/installer. This is de default mode.


HOW TO START MEGUA:

* inside SMC: from sagews worksheet (see tutorial)
* inside SMC: from bash using script "megua <args>" (see tutorial)
* in a desktop, in any working directory, from bash  using script "megua <args>" (see tutorial)
* in a desktop, to test megua code, inside megua/megua source directory, using "sage -t <module.py>" (see tutorial)


"""


#*****************************************************************************
#       Copyright (C) 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


from os import environ,path,mkdir,error
import shutil



# ======================
# SYSTEM CONFIGURATION
# ======================

#Not needed:
#environ["SAGECMD"] = path.join(environ["SAGE_ROOT"],"sage")
#environ["MEGUA_MODULES_DIR"] = "$HOME/megua/megua"

#Now, only for pt_pt template
#TODO: change this
MEGUA_TEMPLATE_DIR = path.join( 
    path.dirname(path.abspath(__file__)),
    "template/pt_pt")



MEGUA_READ_ENV = False
try:
    MEGUA_READ_ENV = environ["MEGUA_READ_ENV"]=="True" #Must be "True"
except KeyError:
    pass

#print "MEGUA_READ_ENV=",MEGUA_READ_ENV

if MEGUA_READ_ENV:

    # SYSTEM CONFIGURATION
    #MEGUA_BASH_ENVIRONMENT=environ["MEGUA_BASH_ENVIRONMENT"]
    MEGUA_PLATFORM=environ["MEGUA_PLATFORM"]
    #MEGUA_CALLED_FROM_BASH=environ["MEGUA_CALLED_FROM_BASH"]=="True"
    MATHJAX_HEADER=environ["MATHJAX_HEADER"]
    # PROJECT CONFIGURATION
    MEGUA_EXERCISE_INPUT=environ["MEGUA_EXERCISE_INPUT"]
    PROJECT_DATABASE_NAME=environ["PROJECT_DATABASE_NAME"]
    PROJECT_DATABASE_FULLPATH=environ["PROJECT_DATABASE_FULLPATH"]
    MEGUA_EXERCISE_CATALOGS=environ["MEGUA_EXERCISE_CATALOGS"]

    #optinal: siacua project
    try:
        SIACUA_WEBKEY=environ["SIACUA_WEBKEY"]
        SIACUA_COURSENAME=environ["SICUA_COURSENAME"]
        SIACUA_USERNAME=environ["SIACUA_USERNAME"]
    except KeyError:
        pass 

else: #MEGUA setup is in $HOME/.megua/conf.py

    PATH_CONF_PY = path.join(environ["HOME"],".megua","conf.py")

    if not path.isfile(PATH_CONF_PY):

        #1. create .megua
        try:
            mkdir(path.join(environ["HOME"],".megua"))
        except error as e: #error is os.error alias of exceptions.OSError
            print e.message

        #2. get template of conf.py (conf_megua.py because there is conf.py for rest)
        source = path.join(MEGUA_TEMPLATE_DIR,"conf_megua.py")
        shutil.copyfile(source,PATH_CONF_PY)

    #load path variables to this module space
    execfile( PATH_CONF_PY )


#print "MEGUA_PLATFORM=",MEGUA_PLATFORM

#===================
# Check directories
#===================

# Try to create them:
if not os.path.exists(MEGUA_EXERCISE_INPUT):
    os.makedirs(MEGUA_EXERCISE_INPUT)
if not os.path.exists(MEGUA_EXERCISE_CATALOGS):
    os.makedirs(MEGUA_EXERCISE_CATALOGS)
if not os.path.exists(MEGUA_WORKDIR_FULLPATH):
    os.makedirs(MEGUA_WORKDIR_FULLPATH)
    shutil.copy(os.path.join(MEGUA_TEMPLATE_DIR,"megua_dog.png"), MEGUA_WORKDIR_FULLPATH)



STOP_MEGUA = False

if not path.isdir(MEGUA_EXERCISE_INPUT):
    print "Directory MEGUA_EXERCISE_INPUT='{0}' does not exist. Create it or change configuration.".format(MEGUA_EXERCISE_INPUT)
    STOP_MEGUA = True

#TODO: the string for project database is ok but there is no databae YET
# How to handle it? 
#assert(path.isfile(PROJECT_DATABASE))

if not path.isdir(MEGUA_EXERCISE_CATALOGS):
    print "Directory MEGUA_EXERCISE_CATALOGS='{0}' does not exist. Create it or change configuration.".format(MEGUA_EXERCISE_CATALOGS)
    STOP_MEGUA = True

if not 'SIACUA_WEBKEY' in locals() or not 'SIACUA_COURSENAME' in locals() or not 'SIACUA_USERNAME' in locals():
    print "To configure for SIACUA please edit ~/.megua/conf.py."
    
if STOP_MEGUA:
    print "Check configurable options in ~/.megua/conf.py"
    exit(-1)

