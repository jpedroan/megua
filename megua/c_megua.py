# coding=utf8

r"""
c_megua.py -- "Command" calling several MEGUA tools.


Assume that:

- if there is an home, there is a single database and project.
- megua setup (for the single home and "project" ) is at .megua/mconfig.py

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


def usage():
    #####  1.......................26..................................................78
    #####  |.....................--.|...................................................|
    print "Arguments:"
    print "  help <cmd>          -- calls help on command <cmd>"  
    print "  catalog             -- produce a catalog based on exercises database"  
    print "  dup                 -- duplicate name, inc. counter, make new exercise file"  
    print "  new                 -- make new exercise file"  
    print "  meg2smc             -- convert megua5.2 database to megua for smc"  





if __name__=="__main__":
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)

    if len(sys.argv)==1 or not sys.argv[1] in ['help','catalog','dup','new','meg2smc']:
        usage()
        exit()

    if sys.argv[1] == 'help':
        usage()
    elif sys.argv[1] == 'catalog':
        meg.catalog()
    elif sys.argv[1] == 'dup':
        raise NotImplementedError
    elif sys.argv[1] == 'new':
        raise NotImplementedError
    elif sys.argv[1] == 'meg2smc':
        print "At bash, call 'sage -python meg2smc.py'"
    else:
        print "Command not known."
        usage()



