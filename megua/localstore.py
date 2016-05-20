# coding: utf-8

# vim:fileencoding=utf-8

#The above python directive allows the testing for european accented characters.
#The vim for python coding directive informs vim  of the use of iso-....


# Warning about UNICODE: 
# 1. for unicode string cannot use u'áé' and must use u'\xe1\xe9'
# 2. for str string can use "áé".

r"""
Creating and editing and exercise database file using sqlite3 module from Python standard library.

AUTHORS:

- Pedro Cruz (2011-02-17): initial version
- Pedro Cruz (2011-10): another version
- Pedro Cruz (2016-02): Prepare for SMC

NOTES:

Database sqlite.
Edition with sqlitebrowser


LINKS:

- http://docs.python.org/release/2.6.4/library/sqlite3.html
- About bytecode: file:///home/jpedro/Downloads/python-2.6.4-docs-html/reference/simple_stmts.html#exec

TODO:

- Create a table for meta information: author name, spoken language, markup language
- Add encrypted content with a password.
- problem_id: it will be created or maintained by "insertchange" function.
- DONE. Use unicode on TEXT columns. See python slite3: "Connection.text_factory"

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz 
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

#Python modules
import sqlite3
import os
import re
import shutil



#MEGUA modules
from megua.convertdb import convertdb
from megua.tounicode import to_unicode


__VERSION__ = '0.2.1'

r"""
Version description:

- 0.2.1: added 'suggestive name' to %problem tag and a new column.
"""


def megregexp(regex,text):

    #if type(text)!=unicode:
    #    text = text.encode('utf-8')

    #if type(regex)!=unicode:
    #    regex = regex.encode('utf-8')

    #Manual debug only:
    #print "Type of megregexp arguments: -------"
    #print "regex argument: ", type(regex)
    #print "text argument: ", type(text)

    # Testing:
    # Get numeric value of second character
    #import unicodedata
    #print "UNICODE DATA FOR REGEX:----------------"
    #for i, c in enumerate(regex):
    #    print i, '%04x' % ord(c), unicodedata.category(c),
    #    print unicodedata.name(c)
    #print "UNICODE DATA FOR TEXT:----------------"
    #for i, c in enumerate(text):
    #    print i, '%04x' % ord(c), unicodedata.category(c),
    #    print unicodedata.name(c)

    if re.search(regex,text,re.MULTILINE|re.DOTALL|re.IGNORECASE|re.U):
        return 1
    else:
        return 0


class LocalStore:

    r"""
    LocalStore class implements the database of a MegBook over sqlite3.

    .. test with: OLD sage -python -m doctest localstore.py
    
    
    .. sage -t localstore.py

    EXAMPLES::

    sage: from megua.localstore import LocalStore
    sage: filename = r"/tmp/localstore.sqlite"
    sage: import os
    sage: if os.access(filename,os.F_OK):        #Remove previous test if exists:
    ....:     os.remove(filename)
    sage: lstore = LocalStore(filename,natlang='pt_pt',markuplang='latex')
    sage: LocalStore._debug = True
    sage: row = {'unique_name': u'keyone', 'sections_text': u'Section; SubSection; Subsubsection', 'suggestive_name': u'Some Name1',
    ....: 'summary_text': u'summary1 \xe1\xe9', 'problem_text': u'problem1', 'answer_text': u'answer1', 'class_text': u'class Ex1'}
    sage: r = lstore.insertchange(row) 
    Exercise 'keyone' inserted in database.
    sage: slist = lstore.search("áé") #str 
    sage: lstore.print_row(slist[0]) #print the only record
    Record 001: keyone
    <BLANKLINE>
    problem1
    <BLANKLINE>
    sage: row = {'unique_name': u'keytwo', 'sections_text': u'Section; SubSection; Subsubsection', 'suggestive_name': u'Some Name2',
    ....: 'summary_text': u'summary2 \xe9\xf3', 'problem_text': u'problem2', 'answer_text': u'answer2', 'class_text': u'class Ex2'}
    sage: r = lstore.insertchange(row)
    Exercise 'keytwo' inserted in database.
    sage: slist = lstore.search(u"\xe9\xf3") #unicode
    sage: lstore.print_row(slist[0])
    Record 002: keytwo
    <BLANKLINE>
    problem2
    <BLANKLINE>
    sage: row = {'unique_name': u'keyone', 'sections_text': u'Section; SubSection; Subsubsection', 'suggestive_name': u'Some Name1',\
    ....: 'summary_text': u'summary1 modified', 'problem_text': u'problem1 modified', 'answer_text': u'answer1 modified', \
    ....: 'class_text': u'class Ex1 modified'}
    sage: r = lstore.insertchange(row)
    Exercise 'keyone' changed in database.
    sage: slist = lstore.search(u"\xe1\xe9") #unicode
    sage: print slist
    []

    """

    #Class variable to be available to ``megregexp`` function.
    _debug = False

    def __init__(self,filename=None,natlang='pt_pt',markuplang='latex'):
        """
        Create a local storage for exercises.
        """

        self.natural_language = natlang
        self.markup_language = markuplang

        # =================
        # 1. Get a filename 
        # =================
        self.local_store_filename = get_dbfilename(filename)


        # =============================
        # 2. Create or convert and use.
        # =============================
    
        version = self._database_version()
        if LocalStore._debug:
            print "Version in file: ", version, " -- Localstore code version: ", __VERSION__

        if version == None:

            self._createdb(self.local_store_filename)

            #Open database to use
            self._open_to_use()

        elif version != __VERSION__:

            #Move current database to a new filename "old_dbfilename"
            old_dbfilename = self.local_store_filename + '.' + version
            shutil.move( self.local_store_filename, old_dbfilename)

            #Create a new one.
            self._createdb( self.local_store_filename )

            #Open database to use (and receive exercises from old database)
            self._open_to_use()
            
            convertdb(old_dbfilename, self, version)

        else:

            #Open database to use
            self._open_to_use()


        if LocalStore._debug:
            print "Database opened in: ", self.local_store_filename

 

    def _open_to_use(self):
        """
        Open to use.
        """
        if LocalStore._debug:
            print "Open MegBook %s to use." % self.local_store_filename
        self.conn = sqlite3.connect(self.local_store_filename)
        self.conn.create_function("regexp",2,megregexp)
        self.conn.row_factory = sqlite3.Row
        # self.conn.text_factory = str
        
        if LocalStore._debug:
            sqlite3.enable_callback_tracebacks(True)
        else:
            sqlite3.enable_callback_tracebacks(True)#while in testing TODO
        if LocalStore._debug:
            print "....  ready."


    def _database_version(self):
        """
        Check if a database exists.
        """
        conn = sqlite3.connect(self.local_store_filename)
        conn.row_factory = sqlite3.Row

        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='exercises'")

        if c.fetchone()!=None: #if empty database
            """
            Version algorithm:
            
            Version 0.1:
            - don't have metameg
            - TEXT fields are not unicode

            Version 0.2
            - with metameg (includes version field)
            - TEXT fields are unicode

            """
            #Check metameg
            #TODO: improve this meta tag
            c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metameg'")
            row = c.fetchone()            
            if row == None:
                version = '0.1'
            else:
                c2 = conn.cursor()
                c2.execute("SELECT version,natural_language,markup_language from metameg")
                row = c2.fetchone()
                version = row['version']
                #assert(self.natural_language == row['natural_language']) #TODO: check this
                #assert(self.markup_language == row['markup_language'])
                c2.close()

        else:
            version = None

        c.close()
        conn.close()

        return version


    def _createdb(self,filename):
        """
        Create a new empty database.
        """

        conn = sqlite3.connect(filename)
        conn.row_factory = sqlite3.Row
        # conn.text_factory = str
        
        # Create database for current version.
        c = conn.cursor()

        c.execute('''CREATE TABLE exercises ( 
            problem_id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
            unique_name TEXT UNIQUE, 
            sections_text TEXT,
            suggestive_name TEXT,
            summary_text TEXT, 
            problem_text TEXT, 
            answer_text TEXT, 
            class_text TEXT
            )'''
        )

        c.execute('''CREATE TABLE metameg (
            natural_language TEXT, 
            markup_language TEXT, 
            version TEXT )'''
        )

        c.execute("""INSERT INTO metameg (natural_language, markup_language, version) VALUES (?,?,?)""", 
            (self.natural_language, self.markup_language, __VERSION__) 
        )

        #bytecode will not be used: see livro/pyinspect.py

        conn.commit()
        c.close()
        conn.close()


    #def insertchange(self,unique_name,sections,summary,problem,answer,class_text):
    def insertchange(self,row):
        """
        Insert or change an entry in database with key ``unique_name``.

        INPUT:

        - ``row`` -- data dictionary with entries:

            * ``unique_name`` --  Exercise template name (and also python class name) and unique record identifier (string).
            * ``sections_text`` -- Section; subsection; etc or empty string (unicode).
            * ``suggestive_name`` -- Suggestive name for this problem.
            * ``summary_text`` -- Summary of the exercise (unicode).
            * ``problem_text`` -- Problem text description (unicode).
            * ``answer_text`` -- Answer text description (unicode).
            * ``classtext`` -- python class code in textual form ready for Python ``eval``.

        OUTPUT:

        -   Funtion returns a ``row`` object (see sqlite3 documentation).
        

        NOTES: it is implicit in each instance the columns.

        TODO: if exercise is not changed it need not be compiled again. Maybe 
        this function could return "new", "changed", "not changed" for helping
        decision in pdf file.

        """

        unique_name = row['unique_name']

        #Check if unique_name already on database
        c = self.conn.cursor()
        c.execute("SELECT unique_name FROM exercises WHERE unique_name=?",(unique_name,))
        do_insert = (c.fetchone()==None)
        c.close()
        if do_insert:
            self.insert(row)
        else:
            self.change(row)

        #return the changed row
        c = self.conn.cursor()
        c.execute("SELECT * FROM exercises WHERE unique_name=?",(unique_name,))
        row = c.fetchone()
        c.close()
        return row

    def insert(self,row):

        #INSERT INTO Persons (P_Id, LastName, FirstName) VALUES (5, 'Tjessem', 'Jakob')
        #http://www.w3schools.com/sql/sql_insert.asp


        c = self.conn.cursor()
        c.execute("""INSERT INTO exercises \
            (unique_name, \
            sections_text, \
            suggestive_name, \
            summary_text, \
            problem_text, \
            answer_text, \
            class_text) VALUES \
            (?,?,?,?,?,?,?)""",  #ADD OR REMOVE ? for each new/removal columns
            (   row['unique_name'], 
                row['sections_text'],
                row['suggestive_name'],
                row['summary_text'],
                row['problem_text'],
                row['answer_text'],
                row['class_text']
            )
        )
        self.conn.commit()
        c.close()
        if LocalStore._debug:
            print "Exercise '" + row['unique_name'] + "' inserted in database."




    def change(self,row):
        """

        """

        #INSERT INTO Persons (P_Id, LastName, FirstName) VALUES (5, 'Tjessem', 'Jakob')
        #http://www.w3schools.com/sql/sql_insert.asp

        c = self.conn.cursor()
        r = c.execute("""UPDATE exercises \
            SET \
                sections_text=?, \
                suggestive_name=?, \
                summary_text=?, \
                problem_text=?, \
                answer_text=?, \
                class_text = ? \
             WHERE \
                unique_name=? """,
            (   row['sections_text'],
                row['suggestive_name'],
                row['summary_text'],
                row['problem_text'],
                row['answer_text'],
                row['class_text'],
                row['unique_name']
            )
        )
        self.conn.commit()
        c.close()
        if LocalStore._debug:
            print "Exercise '" + row['unique_name'] + "' changed in database."

    #See def search(...) below. 
    #
    #def row_contains(self,regexp):
    #    """Helper method for search method
    #    #TODO: check if keywords can be a list and what sintaxe.
    #    http://www.go4expert.com/forums/showthread.php?t=2337
    #    """
    #    l = [re.search( regexp ,row[ this ],re.I|re.L|re.M|re.S) for this in \
    #        ['summary_text', 'problem_text', 'answer_text', 'sage_classtext']]
    #    return sum(l)



    def get_classrow(self, unique_name):
        unique_name = to_unicode(unique_name)
        c = self.conn.cursor()
        c.execute("SELECT * FROM exercises WHERE unique_name=?", (unique_name,))
        row = c.fetchone()
        c.close()
        return row


    def remove_exercise(self, unique_name):
        unique_name = to_unicode(unique_name)
        c = self.conn.cursor()
        c.execute("DELETE FROM exercises WHERE unique_name=?", (unique_name,))
        self.conn.commit()
        c.close()

    def search(self,regex):
        r"""
        Present headers from problems containing keywords from regex anywhere.

        http://docs.python.org/release/2.6.4/library/sqlite3.html
        """
        #Connect
        #conn = sqlite3.connect(self.local_store_filename)

        if type(regex)==str:
            regex = unicode(regex,'utf-8')

        #Debug unicode problems
        #print "localstore.search(regex) ---------------"
        #import unicodedata
        #for i, c in enumerate(regex):
        #    print i, '%04x' % ord(c), unicodedata.category(c),
        #    print unicodedata.name(c)



        #if LocalStore._debug:
        #    print "regex=",regex," with type ",type(regex)

        c = self.conn.cursor()

        c.execute("""SELECT * FROM exercises  \
            WHERE \
                    sections_text REGEXP ? OR \
                    suggestive_name REGEXP ? OR \
                    summary_text REGEXP ? OR \
                    problem_text REGEXP ? OR \
                    answer_text REGEXP ? OR \
                    class_text REGEXP ? \
            ORDER BY unique_name \
            """, (regex, regex, regex, regex, regex, regex,)
        )

        #Build a list with all records
        #TODO: can be an enourmous list.
        row_list = c.fetchall()

        c.close()

        return row_list


    def print_all(self):
        """
        Helper function to print each exercise.
        """

        print "----------------------"
        print "List of all exercises:"
        print "----------------------"
        for row in ExIter(self):
            self.print_row(row)


    def print_row(self,row):
        sname = 'Record %03d: %s' % (row['problem_id'],row['unique_name'])
        print sname + '\n\n' + row['problem_text'] + '\n'




def get_dbfilename(filename=None):
    """
    Get an os accessible filename if no filename is given or test if the given filename is accessible.

    INPUT:
    - ``filename`` -- filename or None
    
    OUTPUT:
        a filename
    """
    if filename:
        #TODO: check if os accessible and valid filename here.
        # if bad filename:
        #    raise IOError("MegBook needs a database filename to be specified.")
        return filename
    else:    
        #Create or open an exercise store
        fhome = os.getenv("HOME")
        s = os.path.join(fhome,"meguadb.sqlite")
        return s



class ExIter:
    """
    ExIter is an iterator over the exercises in the LocalStore.

    LINK:
    - http://stackoverflow.com/questions/19151/build-a-basic-python-iterator
    """

    def __init__(self, localstore, regex=None):
        """

        """
        self.localstore = localstore

        #regex to unicode or None
        if regex!=None and type(regex)==str:
            self.regex = unicode(regex,'utf-8')
        else:
            self.regex = regex

        self.cur = self._get_cursor()


    def _get_cursor(self):

        if self.regex is None:
            c = self.localstore.conn.cursor()
            c.execute("""SELECT * FROM exercises""")
        else:
            regex = self._unicode(regex)
            c = self.localstore.conn.cursor()

            c.execute("""SELECT * FROM exercises  \
                WHERE \
                    sections_text REGEXP ? OR \
                    suggestive_name REGEXP ? OR \
                    summary_text REGEXP ? OR \
                    problem_text REGEXP ? OR \
                    answer_text REGEXP ? OR \
                    class_text REGEXP ? \
                ORDER BY unique_name \
                """, (regex, regex, regex, regex, regex,) )
        return c


    def __iter__(self):
        return self


    def next(self):
        row = self.cur.fetchone()
        if row == None:
            raise StopIteration
        else:
            return row


