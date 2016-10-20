# -*- coding: utf-8 -*-

"""
main.py -- calling several MEGUA tools.

The automatic script creation (using install process using setuptools) will 
create a bash call to main.py:main procedure defined below.

Assume that:

- if there is an home, there is a single database and project.
- megua setup (for the single home and "project" ) is at .megua/mconfig.sh


DEVELOPMENT NOTES:

Study this:

- http://stackoverflow.com/questions/8085520/generating-pdf-latex-with-python-script


Automatic script creation (install process using setuptools):

- https://setuptools.readthedocs.io/en/latest/setuptools.html#automatic-script-creation

How to add a new command:

- add an "if clause" in main()
- add a line in usage()
- add command in line:  if len(sys.argv)==1 or not sys.argv[1] in ['help','catalog','new',....

"""


#*****************************************************************************
#       Copyright (C) 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


# PYTHON modules  
#import re
#import subprocess
import sys
from os import environ,path,mkdir,makedirs,error
import shutil


#MEGUA modules
#See main function for: from megua.all import *
from megua.scripts.megsync import inputfiles_status,inputfiles_add
#The following import is placed where needed below 
#from megua.all import meg


r"""
From 
    .../megua/script/main.py
to 
    .../megua/templates/pt_pt

DETAILS:    

   https://docs.python.org/2/library/os.path.html
    
"""    
MEGUA_TEMPLATE_DIR = path.join( 
    path.dirname(path.dirname(path.abspath(__file__))),
    "template/pt_pt")



def usage(argv):
    if len(argv)<=1:
        #####  1.......................26..................................................78
        #####  |.....................--.|...................................................|
        print "Arguments:"
        print "  help <cmd>          -- calls help on command <cmd>"  
        print "  new <filename>      -- make new exercise file"  
        print "  catalog             -- produce a catalog based on exercises database"  
        print "  status              -- show unsyncronized worksheet exercise files"  
        print "  add                 -- add unsyncronized worksheet exercise files"  
    elif len(argv)==2 and not sys.argv[1] in ['catalog','new','status','add']:
        #####  1.......................26..................................................78
        #####  |.....................--.|...................................................|
        print "Arguments:"
        print "  help catalog          -- calls help on command catalog"  
        print "  help new              -- calls help on command new"  
        print "  help status           -- calls help on command status"  
        print "  add                   -- add unsyncronized worksheet exercise files"  
    elif len(argv)==3 and sys.argv[1]=='help' and sys.argv[2]=='catalog':
        #####  1.......................26..................................................78
        #####  |.....................--.|...................................................|
        print "megua catalog         -- produces a pdf file with an instance with all exercises."
    elif len(argv)>=3 and sys.argv[1]=='help' and sys.argv[2]=='status':
        #####  1.......................26..................................................78
        #####  |.....................--.|...................................................|
        print "megua status          -- show unsyncronized worksheet exercise files"
        print ""
        print "For each filename,"
        print "1. checks if filename is recorded in the database"
        print "2. when a record is in the database, checks if a filename exists."
        print "3. if 'status test' is given, and a filename is recorded in the database, checks if it runs properly."
        #TODO: 3. is not READY! Write more help above,  store help in templates, make 'test' option work
        #TODO: a general help file is easy!
    elif len(argv)==2 and sys.argv[1]=='new':
        usage_new()
    elif len(argv)==3 and sys.argv[1]=='help' and sys.argv[2]=='new':
        usage_new()
    else:
        usage([])        
        
    usage_show_options()


def usage_new():
    #####  1.......................26..................................................78
    #####  |.....................--.|...................................................|
    print "megua new <filename> "
    print "  <filename> is       --  E12X34_name_001_latex.sagews"
    print "  <filename> is       --  E12X34_name_001_siacua.sagews"
    print "      or"
    print "  <filename> is       --  E12X34_name_001_latex.sage"
    print "  <filename> is       --  E12X34_name_001_siacua.sage"


def usage_show_options():
    try:
        print "\nProject directories:"
        print "  exercises source directory:", MEGUA_EXERCISE_INPUT
        print "  catalogs directory:", MEGUA_EXERCISE_CATALOGS
    except KeyError as k:
        print "\n\nscripts/main.py say: there are missing variables in '.megua/conf.py'."


def valid_filename(filename):
    #check meg.new_exercise: maybe this is not needed.
    return ("_siacua" in filename or "_latex" in filename) and ( filename[-7:] == '.sagews' or filename[-5:] == '.sage')



def init():
    #TODO: when is this file called ?
    
    #print "==============================="
    #print "script/main.py: MEGUA_TEMPLATE_DIR =", MEGUA_TEMPLATE_DIR
    #print "==============================="

    PATH_CONF_PY = path.join(environ["HOME"],".megua","conf.py")
    
    #Create, if not exit, ~/.megua/conf.py and
    #allow user to change it before use
    if not path.isfile(PATH_CONF_PY):
        
        #1. create .megua
        try:
            mkdir(path.join(environ["HOME"],".megua"))
        except error as e: #error is os.error alias of exceptions.OSError
            print e.message
        
        #2. get template of conf.py (conf_megua.py because there is conf.py for rest)
        source = path.join(MEGUA_TEMPLATE_DIR,"conf_megua.py")
        shutil.copyfile(source,PATH_CONF_PY)
        
        print "NOTE:"
        print "1. Configuration file 'conf.py' created at:", PATH_CONF_PY
        print "2. Edit pathnames in 'conf.py' and other options, if necessary."
        print "3. Call '$ megua help' for help on other routines."
        return 'user-must-run-again'
        

    #File ~/.megua/conf.py exists and now check
    #if directories exist, otherwise, create them.

    #load path variables to this module space
    execfile( PATH_CONF_PY, globals())


    # =========================
    # ENVIRONMENT CONFIGURATION
    # =========================

    #CODE: it's important that the configuration variables below be mentioned 
    #      in templates/<lang>/conf_megua.py

    if not path.isdir(MEGUA_EXERCISE_INPUT):
        makedirs(MEGUA_EXERCISE_INPUT)
    if not path.isdir(MEGUA_EXERCISE_OUTPUT):
        makedirs(MEGUA_EXERCISE_OUTPUT)
    if not path.isdir(MEGUA_EXERCISE_CATALOGS):
        makedirs(MEGUA_EXERCISE_CATALOGS)
    
    # =====================
    # PROJECT CONFIGURATION
    # =====================
    
    #No directory to be created.
    
    return 0




def main():
    """
    This routine will be called by a script produced by
    
    Method 1
    
    ::
        sage -python setup.py install 

    Method 2
    
    ::
        sage -sh
        pip install --user ....
            
    #if __name__=="__main__":
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)
            
    """

    #create options file and create directories
    res = init()
    if res=='user-must-run-again':
        return 0


    if len(sys.argv)==1 or not sys.argv[1] in ['help','catalog','new','status','add']:
        usage(sys.argv)
        return 0

        
     
    
    if sys.argv[1] == 'help':
        usage(sys.argv)
    elif sys.argv[1] == 'catalog':
        from megua.all import meg
        meg.catalog()
    elif sys.argv[1] == 'status':
        inputfiles_status()
    elif sys.argv[1] == 'add':
        inputfiles_add()
    elif sys.argv[1] == 'new':
        if len(sys.argv)<3: # or (len(sys.argv)==3 and not valid_filename(sys.argv[2])):
            usage(sys.argv)
            return 0
        if len(sys.argv)>3:
            print "megua new <filename>, only; other arguments were ignored."
        from megua.all import meg
        meg.new_exercise(sys.argv[2])
    else:
        print "Command not known."
        usage()
        return 0

    return 0



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
"""

def create_for_desktop():
    print "create_for_desktop()"
    
"""

'''
