# coding=utf8

r"""
c_megua.py -- "Command" calling several MEGUA tools.


Assume that:

- if there is an home, there is a single database and project.
- megua setup (for the single home and "project" ) is at .megua/mconfig.sh


DEVELOP:

study this:
- http://stackoverflow.com/questions/8085520/generating-pdf-latex-with-python-script


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


# SAGE modules
#from sage.misc.latex import have_pdflatex


#MEGUA modules
from megua.all import *


def usage(argv):
    if len(argv)<=1:
        #####  1.......................26..................................................78
        #####  |.....................--.|...................................................|
        print "Arguments:"
        print "  help <cmd>          -- calls help on command <cmd>"  
        print "  catalog             -- produce a catalog based on exercises database"  
        print "  new <filename>      -- make new exercise file"  
    elif len(argv)==2 and not sys.argv[1] in ['catalog','new']:
        #####  1.......................26..................................................78
        #####  |.....................--.|...................................................|
        print "Arguments:"
        print "  help catalog          -- calls help on command catalog"  
        print "  help new              -- make new exercise file"  
    elif len(argv)==3 and sys.argv[1]=='help' and sys.argv[2]=='catalog':
        #####  1.......................26..................................................78
        #####  |.....................--.|...................................................|
        print "megua catalog         -- produces a pdf file with an instance with all exercises."
    elif len(argv)==2 and sys.argv[1]=='new':
        usage_new()
    elif len(argv)==3 and sys.argv[1]=='help' and sys.argv[2]=='new':
        usage_new()
    else:
        usage([])        
        
    usage_bash_vars()


def usage_new():
    #####  1.......................26..................................................78
    #####  |.....................--.|...................................................|
    print "megua new <filename> "
    print "  <filename> is       --  E12X34_name_001_latex.sagews"
    print "  <filename> is       --  E12X34_name_001_siacua.sagews"
    print "      or"
    print "  <filename> is       --  E12X34_name_001_latex.sage"
    print "  <filename> is       --  E12X34_name_001_siacua.sage"


def usage_bash_vars():
    try:
        print "\nProject description and directories:"
        print "  course name (in siacua system):", environ["COURSE"]
        print "  user name (in siacua system):", environ["USERNAME_SIACUA"]
        print "  project datbase:", environ["PROJECT_DATABASE"]
        print "  exercise source directory:", environ["MEGUA_EXERCISE_INPUT"]
        print "  exercise catalog directory:", environ["MEGUA_EXERCISE_CATALOG"]
    except KeyError as k:
        print "\n\nc_megua.py say: contact administrator because there are missing bash variables."


def valid_filename(filename):
    #check meg.new_exercise: maybe this is not needed.
    return ("_siacua" in filename or "_latex" in filename) and ( filename[-7:] == '.sagews' or filename[-5:] == '.sage')


def main():
    """
    This routine will be called by a script produced by
    
    ::
        sage -python setup.py install 
        
            
    #if __name__=="__main__":
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)
            
    """

    if len(sys.argv)==1 or not sys.argv[1] in ['help','catalog','new','meg2smc']:
        usage(sys.argv)
        return 0

    if sys.argv[1] == 'help':
        usage(sys.argv)
    elif sys.argv[1] == 'catalog':
        meg.catalog()
    elif sys.argv[1] == 'new':
        if len(sys.argv)<3: # or (len(sys.argv)==3 and not valid_filename(sys.argv[2])):
            usage(sys.argv)
            return 0
        if len(sys.argv)>3:
            print "megua new <filename>, only; other arguments were ignored."
        meg.new_exercise(sys.argv[2])
    elif sys.argv[1] == 'meg2smc':
        print "At bash, call 'sage -python meg2smc.py'"
    else:
        print "Command not known."
        usage()
        return 0

    return 0
