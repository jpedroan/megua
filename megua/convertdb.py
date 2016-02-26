
r"""
Convert an str based Meg exercise database to unicode based database.
This is a script to use in command-line.

AUTHORS:

- Pedro Cruz (2011-08-17): initial version


EXAMPLES:

   This shows help.
   $ sage -python convertdb -h

   Conversion from str to unicode
   $ sage -python convertdb.py -u database.sqlite 


"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz 
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************



#PYTHON library
from optparse import OptionParser
import sqlite3


#MEGUA library
#from megua.exbase import exerciseinstance
from megua.tounicode import to_unicode


def convertdb(dbname,new_store,from_v):
    #TODO: do this as a cycle: convert from 0.1, then from 0.2, etc one at a time.
    if from_v == "0.1":
        convertdb_from01(dbname,new_store) #produce 0.2
    elif from_v == "0.2":
        convertdb_from02(dbname,new_store) #produce 0.2.1.
    else:
        raise NotImplementedError("MegUA version control.")


def convertdb_from01(old_dbname, new_store):

    #Open str database
    conn = sqlite3.connect(old_dbname)
    if conn is not None:
        print "Converting Meg v0.1 archive at " + old_dbname
        conn.row_factory = sqlite3.Row
        #conn.text_factory = str
    else:
        print "Can't open " + old_dbname

    c = conn.cursor()
    c.execute(r"""SELECT * FROM exercises ORDER BY owner_key""")

    for row in c:
        owner_key = row["owner_key"]
        x = row["summary_text"]
        #summary = unicode(row["summary_text"],'utf8')
        #problem = unicode(row["problem_text"],'utf8')
        #answer = unicode(row["answer_text"],'utf8')
        #class_text = unicode(row["class_text"],'utf8')
        summary = row["summary_text"]
        problem = row["problem_text"]
        answer = row["answer_text"]
        class_text = row["class_text"]
        class_text = class_text.replace("Exercise.make_random","#Exercise.make_random")
        class_text = class_text.replace(",seed)",")")
        class_text = class_text.replace("Exercise.solve","#Exercise.solve")
   
        new_store.insert(owner_key,'',summary,problem,answer,class_text)
        print "  Summary text is of type %s and now is %s." % (str(type(x)), str(type(summary)))

    c.close()
    conn.close()
 



def convertdb_from02(old_dbname, new_store):

    #Open str database
    conn = sqlite3.connect(old_dbname)
    if conn is not None:
        print "Converting Meg v0.2 archive at " + old_dbname
        print "Adding column for problem name."
        conn.row_factory = sqlite3.Row
        #conn.text_factory = str
    else:
        print "Can't open " + old_dbname

    c = conn.cursor()
    c.execute(r"""SELECT * FROM exercises ORDER BY owner_key""")

    for row in c:

        #Add new information
        problem_pos = row['problem_text'].find("%problem")
        blank_pos = row['problem_text'][problem_pos:].find(" ")
        newline_pos = row['problem_text'][problem_pos:].find("\n")
        if blank_pos > -1:
            newname = row['problem_text'][blank_pos:newline_pos].strip()
        else:
            newname = ''

        if newname == '':
            print u"  Edit exercise {0} because it has no problem name.".format(row['owner_key'])
            newname = remove_underscore2( row['owner_key'] )
        else:
            print u"  Exercise %s as problem name: %s." % (row['owner_key'],row['problem_name'])

        #Store it
        rowdict = dict(row)
        rowdict['suggestive_name'] = newname #add new column
        new_store.insert(rowdict)

    c.close()
    conn.close()
 


def remove_underscore2(txt):
    r"""
    
    EXAMPLES::
        
        sage: remove_underscore2("ABC_caso_123")
        'ABC caso 123'
        sage: remove_underscore2("ABC_caso")
        'ABC caso'
        sage: remove_underscore2("ABC")
        'ABC'
    """
        
    s_pos = 0
    pos = txt.find("_")
    out_t = ''
    while pos>-1:
        out_t += txt[s_pos:pos] + ' '
        s_pos = pos+1
        pos = txt.find("_",s_pos)
    out_t += txt[s_pos:]
    return out_t


if __name__=='__main__':

    #Get argument (filename of database)

    usage = "usage: %prog [options] databasefilename"
    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--unicode", dest="to_unicode", default=False, action="store_true",
                  help="convert str to unicode fields")
    (options, args) = parser.parse_args()
    #print options,args
    
    if options.to_unicode:
        str_unicode_dbconvert(args[0])


