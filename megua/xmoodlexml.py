r"""
xmoodlexml.py -- export to html using Sphinx system (ReST hypertext compiler).


AUTHORS:

- Pedro Cruz (2011-11): initial version

LINKS::

   http://effbot.org/zone/element-index.htm

NOTES: 

"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#sage
from sage.all import *  


#python package
import os
import shutil
import codecs
import jinja2
from string import join

#megua package
from localstore import ExIter
from csection import SectionClassifier, Section

class MoodleXMLExporter:
    """
    Produce rst code files from the database and an index reading first line of the %summary field.

    LINKS:

    http://sphinx.pocoo.org/config.html#options-for-internationalization

    http://code.activestate.com/recipes/193890-using-rest-restructuredtext-to-create-html-snippet/

    ReST NOTATION (http://sphinx.pocoo.org/rest.html#sections)::

        # with overline, for parts
        * with overline, for chapters
        =, for sections
        -, for subsections
        ^, for subsubsections
        ", for paragraphs

    """

    char_level = { 0: '#', 1: '*', 2: '=', 3:'-', 4:'^' }


    def __init__(self,megbook,where=None,debug=False):
      
        #save megstore reference
        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store


        # --------------------    
        # Create sphinx folder 
        # --------------------
        if where is None:
            self.sphinx_folder = self.megbook_store.local_store_filename + '_sphinx'
        else:
            self.sphinx_folder = where
        if debug:
            print "Index folder: " + self.sphinx_folder

        #If does not exist create
        if not os.path.exists(self.sphinx_folder):
            os.makedirs(self.sphinx_folder)
            os.mkdir(os.path.join(self.sphinx_folder,'build'))
            os.mkdir(os.path.join(self.sphinx_folder,'build/html'))
            os.mkdir(os.path.join(self.sphinx_folder,'build/html/_templates'))
            os.mkdir(os.path.join(self.sphinx_folder,'build/html/_static'))


        from pkg_resources import resource_filename
        #sphinx_theme_dir = os.path.join(resource_filename(__name__,''),'default2')
        sphinx_theme_dir = resource_filename(__name__,'')

        #Build a new conf.py based on template at conf_sphinx.py.
        cpy_str = self.megbook.template("conf_sphinx.py",
            language=lang_set(self.megbook.megbook_store.natural_language),
            local_store_filename = self.megbook.local_store_filename,
            megua_theme_dir = sphinx_theme_dir
        )
        f = open( os.path.join(self.sphinx_folder,'conf.py'), 'w') 
        f.write(cpy_str)
        f.close()
        #end sphinx setup folders


            #self.markup_language = markuplang

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.exercise_template = self.megbook.env.get_template("xsphinx_exercise.rst")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template xsphinx_exercise.rst"
            raise e


        #Create tree structure
        self.sc = SectionClassifier(self.megbook_store)
        
        #Save to files and build html.
        self._save_to_files()

        #Build HTML from rst files.

        #argv = ['/usr/bin/sphinx-build', '-q', '-a', '-b', 'html', '-d', 
        #    os.path.join(self.sphinx_folder,'build/doctrees'), #don't put a leader / like  /build/doctrees
        #    self.sphinx_folder, 
        #    os.path.join(self.sphinx_folder,'build/html')]

        argv = [os.path.join(SAGE_ROOT,'local/bin/sphinx-build'), '-q', '-a', '-b', 'html', '-d', 
            os.path.join(self.sphinx_folder,'build/doctrees'), #don't put a leader / like  /build/doctrees
            self.sphinx_folder, 
            os.path.join(self.sphinx_folder,'build/html')]

        if debug:
            print str(argv)
            print sphinx.main(argv)
        else:
            sphinx.main(argv)

        self.htmlfile = os.path.join(self.sphinx_folder,'build/html/index.html')


    def _save_to_files(self):
        
        #Create index.rst from xsphinx_index.rst template.
        for sec_number,sec_name in enumerate(sorted(self.sc.contents)):

            #Get Section with sec_name (see class Section from csection.py)
            section = self.sc.contents[sec_name]

            #Open file
            self.ofile = codecs.open( os.path.join( self.sphinx_folder, "sec%02d.rst" % (sec_number+1) ),encoding='utf-8', mode='w+')

            #Write 
            self.sec_print(section)

            #close
            self.ofile.close()

        #Create index.rst
        index_contents = join( ["   sec%02d" % (sec_number+1) for sec_number in range(len(self.sc.contents))], "\n" )
        s = self.megbook.template("xsphinx_index.rst", contents=index_contents, local_store_filename = self.megbook.local_store_filename )
        ofile = codecs.open(os.path.join(self.sphinx_folder,"index.rst"),encoding='utf-8', mode='w+')
        ofile.write(s)
        ofile.close()


    def sec_print(self, section):

        if section.level<=3:
            self.ofile.write( section.sec_name + "\n")
            self.ofile.write( self.char_level[section.level] * len(section.sec_name) + "\n\n")
        else:
            self.ofile.write( "**" + section.sec_name + "**\n")

        for e in section.exercises:

            #Write exercise ownkey always at level 4.
            self.ofile.write(e+"\n"+self.char_level[4]*len(e) +"\n\n")

            row = self.megbook_store.get_classrow(e) #e is exer name (same as unique_name)
            etxt = self.exercise_template.render(
                    summary=str_indent(row['summary_text']),
                    problem=str_indent(row['problem_text']),
                    answer=str_indent(row['answer_text']),
                    sage_python=str_indent(row['class_text'])
            )

            self.ofile.write(etxt)
            self.ofile.write("\n\n")

        for subsection in section.subsections.itervalues():
            self.sec_print(subsection)



def str_indent(s):
    return "   " + s.replace("\n","\n   ")

def lang_set(s):
    if s == 'pt_pt':
        return 'pt_br'
    else:
        return s

