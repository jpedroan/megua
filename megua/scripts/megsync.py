# -*- coding: utf-8 -*-

"""
megsync.py -- tools to syncronize "worksheet files" and the projet database.

At command line, "megua status" will show files that are not in the database.
More commands here to be created: add, remove.

Assume that:

- if there is an home, there is a single database and project.
- megua setup (for the single home and "project" ) is at .megua/mconfig.sh


DEVELOPMENT NOTES:


"""


#*****************************************************************************
#       Copyright (C) 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


# PYTHON modules  
import re
import os.path
import glob

# MEGUA
from megua.megoptions import PROJECT_DATABASE, MEGUA_EXERCISE_INPUT, MEGUA_PLATFORM
from megua.parse_ex import parse_ex
from megua.tounicode import to_unicode
from megua.all import meg

def inputfiles_status():
    """
    Opens folder MEGUA_EXERCISE_INPUT and compares its files to
    contents in database PROJECT_DATABASE, checking if:
    - filename, without extension, is the name in save(...) part
    - the exercise exists in db
    - fields have changed
    and warns the user of this events
    
    Types of files: *.sage and *.sagews
    Check if MEGUA_PLATFORM="SMC" or "DESKTOP" (see templates/pt_pt/conf_megua.py)
    
    """
    
    if MEGUA_PLATFORM=="SMC":
        search_pattern = os.path.join(MEGUA_EXERCISE_INPUT,"*.sagews")
    else:
        search_pattern = os.path.join(MEGUA_EXERCISE_INPUT,"*.sage")


    #to search exercise code
    re_save = re.compile(ur'save\(r\'\'\'(.+?)\'\'\'\)',re.IGNORECASE|re.U|re.M|re.S)
        
    for fn in glob.glob(search_pattern):

        with open(fn,"r") as f:
            exstr = f.read()
            
        #Parse contents
        mobj = re_save.search(exstr)

        if mobj:
            #print mobj.groups()
            uexercise = mobj.group(1)

            #print uexercise
            row =  parse_ex(to_unicode(uexercise))
            
            if not meg.megbook_store.get_classrow(row["unique_name"]):
                print row["unique_name"],"is not in",PROJECT_DATABASE
                
        else:
            print fn,"does not have 'save' command (it seems it does not have an exercise)."
            


