# coding=utf-8

r"""
Converter from some megua.sqlite to *.sagews files.

RUN WITH:

::

    sage -python meg2smc.py 1 2 3 4

AUTHORS:

- Pedro Cruz (2016-03): First version (refactoring old "megua" for SMC).


DISCUSSION:

Each project has is own sqlite database.
Those databases are to be re-used in SMC but a new version of each exercise, 
each file for each exercise, is to be created in SMC.


EXAMPLES:

The examples

::

   sage -python meg2smc.py latex megua_latex.sqlite  
   sage -python meg2smc.py siacua megua_siacua.sqlite 

will create several *.sagews files in the same directory.

       
DEVELOPMENT:

---------
​Hi, I​ ​don't know why you would want to do that, but in any case: 
a good start might be to look at the sws2sagews converter.
https://github.com/sagemath/cloud/blob/master/scripts/sws2sagews.py
In particular, at the top are the definitions for the delimiters, and 
around line 148 each cell is assembled. 
(e.g. in your case "modes" is an empty string, etc.)
​-- harald
---------

What has been done:

1. created rsa_key to sftp files to SMC
2. use the link above to construct *.sagews files for latex

What has to be done:

1. 


"""


#*****************************************************************************
#       Copyright (C) 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************



#PATH
#import sys
#from os.path import dirname
#sys.path.append(dirname(__file__))

#PYTHON modules
import re
import json
from uuid import uuid4

def uuid():
    return unicode(uuid4())


#MEGUA modules
from megua.localstore import LocalStore,ExIter
from megua.jinjatemplates import templates


#SMC codes
MARKERS = {'cell':u"\uFE20", 'output':u"\uFE21"}


#class identifier
re_class = re.compile(ur'^class[ \t]+(E([a-zA-Z0-9]+)_\w+_\d+)\(\w+\):\s*',re.U)


def meg2smc(instyle,sqlitefilename,newmegbookfilename):
    
    assert(instyle in ["latex","web"])    
    
    #TODO: now: go to localstore and ignore markuplang
    lstore = LocalStore(sqlitefilename,natlang='pt_pt',markuplang=instyle)

    for row in ExIter(lstore):

        #Change in exercise class name
        lines = row["class_text"].splitlines(True) #including \n
        mobj = re_class.match(lines[0])
        if not mobj:
            print "===== Did not recognize class ====="
            print lines
            exit()
        if instyle == "latex":
            new_unique_name = row['unique_name'] + '_latex'
            new_codetext = u'class {0}(ExLatex):\n'.format(new_unique_name)
            htmlstr = u'<h4>%s</h4>' % new_unique_name
        else:
            #siacua system does not have "_siacua" in their names
            new_unique_name = row['unique_name'] #keep for compatibility
            new_codetext = u'class {0}(ExSiacua):\n'.format(new_unique_name)
            htmlstr = u'<h4>%s (Siacua)</h4>' % new_unique_name


        #print new_codetext
        #continue


        for i in lines[1:]:
            new_codetext += i



        exstr = templates.render("megua2smc.sagews",
                    megbookfilename=newmegbookfilename,
                    unique_name=new_unique_name,
                    summary=row["summary_text"],
                    sections=row['sections_text'],
                    problem_name=row['suggestive_name'],
                    problem=row['problem_text'],
                    answer=row['answer_text'],
                    code=new_codetext,
                    uuid1=uuid(),
                    uuid2=uuid(),
                    uuid3=uuid(),
                    uuid4=uuid(),
                    marker_cell=MARKERS["cell"],
                    marker_output=MARKERS["output"],
                    html=htmlstr,
                    json_html=json.dumps({'html':htmlstr})
        )
        
        open(new_unique_name+".sagews","w").write(exstr.encode("utf8"))


if __name__=='__main__':
    r"""
    arg1 = latex or web
    arg2 = sqlite filename
    arg3 = new sqlite filename
    
    NOTES:
    
    - Before use this command, do sqlitebrowser and change sqlite exercise table (owner_key to unique_name)
    """

    import sys
    assert(sys.argv[1] in ["latex","web"])
    print "Producing *.sagews files from '%s' for %s" % (sys.argv[2],sys.argv[1])
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)
    import os.path
    if not os.path.isfile(sys.argv[2]):
        print "...filename does not exist."
        exit()
    meg2smc(sys.argv[1],sys.argv[2],sys.argv[3])


