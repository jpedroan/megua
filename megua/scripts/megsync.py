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
import codecs

# MEGUA
from megua.megoptions import PROJECT_DATABASE, MEGUA_EXERCISE_INPUT, MEGUA_PLATFORM
from megua.parse_ex import parse_ex
from megua.tounicode import to_unicode
from megua.all import meg
from megua.localstore import ExIter

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


    print "="*23+"\n"
    print "Check files that are not in the database."
    print "="*23+"\n"

    
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

            if not row:
                print "Check",fn,"(cannot save the exercise)."
                continue

            #print row["unique_name"]
            
            if not meg.megbook_store.get_classrow(row["unique_name"]):
                print row["unique_name"],"is not in",PROJECT_DATABASE
                
        else:
            print "\n",fn,"does not have 'save' command (it seems it does not have an exercise).\n"


    print "="*23+"\n"
    print "Check records in the database that are not in the files."
    print "="*23+"\n"

    #Check db for records and verify if they exist as a file
    for row in ExIter(meg.megbook_store):
        if MEGUA_PLATFORM=="SMC":
            fn = os.path.join(MEGUA_EXERCISE_INPUT,row['unique_name']+'.sagews')
        else:
            fn = os.path.join(MEGUA_EXERCISE_INPUT,row['unique_name']+'.sage')
            
        if not os.path.isfile(fn):
            print "Exercise",row['unique_name'],"exists in",PROJECT_DATABASE,"but not in filesystem."
            
            
            


def inputfiles_add():
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
            
            if not row:
                print "Check",fn,"(cannot save the exercise)."
                continue
            
            if not meg.megbook_store.get_classrow(row["unique_name"]):
                #meg.save(uexercise)        
                ex_instance = meg.exerciseinstance(row,ekey=0)
                #After all that, save it on database:                        
                meg.megbook_store.insertchange(row)
                
        else:
            print fn,"does not have 'save' command (it seems it does not have an exercise)."
            

    #Check db for records and verify if they exist as a file
    for row in ExIter(meg.megbook_store):
        if MEGUA_PLATFORM=="SMC":
            pathname = os.path.join(MEGUA_EXERCISE_INPUT,row['unique_name']+'.sagews')
        else:
            pathname = os.path.join(MEGUA_EXERCISE_INPUT,row['unique_name']+'.sage')
            
        if not os.path.isfile(pathname):
            #probably, filename missed _siacua, or _latex
            old_unique_name = row['unique_name']
            unique_name = row['unique_name']+"_siacua"
            try:
                meg.megbook_store.rename(old_unique_name,unique_name,warn=False)
                print "Exercise",row['unique_name'],"in",PROJECT_DATABASE,"is now", unique_name
            except:
                pass

            if MEGUA_PLATFORM=="SMC":
                pathname = os.path.join(MEGUA_EXERCISE_INPUT,unique_name+'.sagews')
            else:
                pathname = os.path.join(MEGUA_EXERCISE_INPUT,unique_name+'.sage')

            with codecs.open(pathname, mode='r', encoding='utf-8') as f:
                source_code = f.read()
                new_source_code = re.sub(old_unique_name,unique_name,source_code,re.U|re.M)
            with codecs.open(pathname, mode='w', encoding='utf-8') as f:
                f.write(new_source_code)
                print "Exercise",unique_name,"contained in file",pathname,"has changed all occurrences of",old_unique_name




