# coding=utf-8

r"""
Converter from some megua.sqlite to *.sagews files.


AUTHORS:

- Pedro Cruz (2016-03): First version (refactoring old "megua" for SMC).


DISCUSSION:

Each project has is own sqlite database.
Those databases are to be re-used in SMC but a new version of each exercise, 
each file for each exercise, is to be created in SMC.


HOW TO CONVERT:

In the following, consider variations of this names:

- .newfile.sqlite : is the new sqlite file that will go to SMC
- megua_latex.sqlite: is an old format database with latex exercises
- megua_siacua.sqlite: is an old format database with siacua exercises
- megua_latex.sqlite.sage: contains all text from exercises from old database.
- megua_siacua.sqlite.sage: contains all text from exercises from old database.


The, follow the steps:

1. Extract exercises from the latex sqlite database, megua 5.2, to 
individual *.sagews files, individual *.sage files, and 
one large *.sage file containing all exercises. This file will be used to recreate the new database.


::

   sage -python $HOME/megua/megua/c_meg2smc.py latex megua_latex.sqlite .newfile.sqlite 

2. Do the same but for the web sqlite old database format with:

::

   sage -python $HOME/megua/megua/c_meg2smc.py web megua_siacua.sqlite .newfile.sqlite

3. After using the first two forms, it is necessary to run a large file using

::

   sage <megua.sqlite.sage>
   
for the appropriate database name, to recreate the new database with 
all exercises in the new format. Errors will appear so:

- correct <exercise>.sage file and after corretion, delete the 
exercise from megua_xxxx.sqlite.sage.
- keep doing sage ``<megua.sqlite.sage>`` until no more errors.


4. Do this for both latex and siacua web exercises, in order them to be 
saved to the same database .newfile.sqlite.

5. All individual *.sage files are now correct and have been stores to .newfile.sqlite. 
Now, run the follwoing to create individual *.sagews files.

   sage -python $HOME/megua/megua/c_meg2smc.py mix .newfile.sqlite .newfile.sqlite


6. Then, export all *.sagews and .newfile.sqlite to SMC.
       

       
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
import codecs
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
re_class = re.compile(ur'^class[ \t]+(E([a-zA-Z0-9]+)_\w+_\d+\w*)\(\w+\):\s*',re.U)


def meg2smc(instyle,sqlitefilename,newmegbookfilename):
    r"""
    Reads a sqlite file from megua5.2 (latex or web styles) and generated a *.sagews file
    for each exercise and a *.sage file.
    
    Reads a sqlite file from megua for SMC style (mix style) and generated a *.sagews file 
    for each exercise and a *.sage file.

    The following substitutions will be done:

    - for latex exercises: ``class E12X34_name_001(Exercise)`` will be ``class E12X34_name_001_latex(ExLatex)``
    - for web (html for siacua) exercises: ``class E12X34_name_001(Exercise)`` will be ``class E12X34_name_001(ExSiacua)`` (in siacua system, the unique_names can't be changed.)
    - for mix: ExLatex or ExSiacua: the exercise is written to a *.sagews file and a *.sage file.
    
    INPUT:
    
    - ``instyle``: latex or web (megua5.2 styles) or mix (for smc style)
    - ``sqlitefilename``: existent sqlite file
    - ``newmegbookfilename``: this will be part of each new *.sagews file and *.sage

    OUTPUT:
    
    - one `*.sagews` file for each exercise in sqlite file ``sqlitefilename``
    - one `*.sage` file for each exercise in sqlite file ``sqlitefilename``
    - a single `*.sage` file containing all exercises: could be used to build the sqlite.
    
    """    
    
    assert(instyle in ["latex","web","mix"])    
    
    #TODO: now: go to localstore and ignore markuplang
    lstore = LocalStore(sqlitefilename,natlang='pt_pt',markuplang=instyle)

    newsagefile = codecs.open(sqlitefilename+'.sage', 'w', 'utf-8')
    newsagefile.write(u'# -*- coding: utf-8 -*-\n\n')
    newsagefile.write(u'from megua.all import *\n')
    newsagefile.write(u'#meg = MegBook("%s")\n\n' % newmegbookfilename)
    newsagefile.write(u'''print "Open file %s and replace all 'Exercise.' by 'ExLatex.' or 'ExSiacua.';"\n\n''')



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
        elif instyle == "web":    
            #siacua system does not have "_siacua" in their names
            new_unique_name = row['unique_name'] + '_siacua' 
            new_codetext = u'class {0}(ExSiacua):\n'.format(new_unique_name)
            htmlstr = u'<h4>%s (Siacua)</h4>' % new_unique_name
        else: #mix style
            if '_latex' in row['unique_name']:
                new_unique_name = row['unique_name'] 
                new_codetext = u'class {0}(ExLatex):\n'.format(new_unique_name)
                htmlstr = u'<h4>%s (Latex)</h4>' % new_unique_name
            else:
                new_unique_name = row['unique_name'] 
                new_codetext = u'class {0}(ExSiacua):\n'.format(new_unique_name)
                htmlstr = u'<h4>%s (Siacua)</h4>' % new_unique_name

        #add other code lines.            
        for i in lines[1:]:
            new_codetext += i


        #Correct multiplechoice position to problem, only
        if "multiplechoice" in row['answer_text']:
            (problemtext,answertext) = _multiplechoice_parser(row)
        elif 'CDATA' in row['answer_text']:
            (problemtext,answertext) = _CDATA_parser(row)
        else:
            (problemtext,answertext) = (row['problem_text'],row['answer_text'])

        #save this ex to its own file.
        exstr1 = templates.render("megua2smc.sagews",
                    megbookfilename=newmegbookfilename,
                    unique_name=new_unique_name,
                    summary=row["summary_text"],
                    sections=row['sections_text'],
                    problem_name=row['suggestive_name'],
                    problem=problemtext,
                    answer=answertext,
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
        open(new_unique_name+".sagews","w").write(exstr1.encode("utf8"))


        #save this ex to a global file.
        exstr2 = templates.render("megua2smc_sagefile.sage",
                megbookfilename=newmegbookfilename,
                unique_name=new_unique_name,
                summary=row["summary_text"],
                sections=row['sections_text'],
                problem_name=row['suggestive_name'],
                problem=problemtext,
                answer=answertext,
                code=new_codetext,
                )

        open(new_unique_name+".sage","w").write(exstr2.encode("utf8"))
        newsagefile.write(exstr2) 
        
    newsagefile.write(u"print 'All exercises have been successfuly written into %s'" % newmegbookfilename)
    newsagefile.close()




def _multiplechoice_parser(row):
    """When <multiplechoice>...</multiplecoice> is present in answer
    it parses it and puts it in problem. 
    """
    
    #Find and extract text inside <multiplechoice>...</multiplechoice>
    choices_match = re.search(r'(<\s*multiplechoice\s*>.+?<\s*/multiplechoice\s*>)', row['answer_text'], re.DOTALL|re.UNICODE)

    if choices_match is None:
        raise SyntaxError("exsiacua module: problem %s should have <multiplechoice>...</multiplechoice> tags." % row['unique_name'])

    #Text inside tags <multiplechoice> ... </multiplechoice>
    choice_text = choices_match.group(1)

    problem_text = row['problem_text'] + u'\n\n' + choice_text
    answer_text  = row['answer_text'][choices_match.end():].strip("\t\n ")
    
    return (problem_text,answer_text)




def _CDATA_parser(row):
    """When CDATA is present in answer
    it parses it and puts it in problem. 
    """
    options = []

    #http://stackoverflow.com/questions/4616554/what-is-the-regex-expression-for-cdata
    CDATAtag_iter = re.finditer(ur'<!\[CDATA\[((?:[^]]|\](?!\]>))*)\]\]>',row['answer_text'],re.UNICODE)

    for cd in CDATAtag_iter:
        options.append( cd.group(1).strip() )
   
    for l in range(len(options)-1): #exclude Detailed Answer
        options[l] = "".join(["<choice>",options[l],"</choice>\n\n"])
    
    options_text = u'\n<multiplechoice>\n\n' + ''.join(options[0:-1]) + u'\n</multiplechoice>\n'
   
    return (row['problem_text'] + u'\n\n' + options_text,options[-1])


if __name__=='__main__':
    r"""
    arg1 = latex or web
    arg2 = sqlite filename
    arg3 = new sqlite filename
    
    NOTES:
    
    - Before use this command, do sqlitebrowser and change sqlite exercise table (owner_key to unique_name)
    """

    import sys
    assert(sys.argv[1] in ["latex","web", "mix","help"])
    if sys.argv[1]=="help":
        ##### "1.......................26..................................................78
        #####  |.....................--.|...................................................|
        print "Open old sqlite db and change owner_key to unique_name."
        print "See more details in c_meg2smc.py file."
        print "Usage examples:"
        print "[1] sage -python $HOME/megua/megua/c_meg2smc.py latex megua_latex.sqlite .newfile.sqlite" 
        print "[2] sage -python $HOME/megua/megua/c_meg2smc.py web megua_siacua.sqlite .newfile.sqlite"
        print "[3] sage -python $HOME/megua/megua/c_meg2smc.py mix .newfile.sqlite .newfile.sqlite"
        exit()
        
    print "Producing *.sagews files from '%s' for %s...." % (sys.argv[2],sys.argv[1])
    #print 'Number of arguments:', len(sys.argv), 'arguments.'
    #print 'Argument List:', str(sys.argv)
    import os.path
    if not os.path.isfile(sys.argv[2]):
        print "...filename does not exist."
        exit()
    meg2smc(sys.argv[1],sys.argv[2],sys.argv[3])


