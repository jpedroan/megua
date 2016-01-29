r"""
xsphinx.py -- export to html using Sphinx system (ReST hypertext compiler).


AUTHORS:

- Pedro Cruz (2011-11): initial version

LINKS::

   http://sphinx.pocoo.org/config.html#confval-html_theme_options

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  


#python package
import sphinx 
import os
import shutil
import codecs
import jinja2
from string import join

#megua package
from localstore import ExIter
from csection import SectionClassifier, Section

class SphinxExporter:
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
        argv = ['/usr/bin/sphinx-build', '-a', '-b', 'html', '-d', 
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
        for sec_number,sec_name in enumerate(self.sc.contents):

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
            self.ofile.write(e+"\n"+self.char_level[section.level+1]*len(e) +"\n\n")

            row = self.megbook_store.get_classrow(e) #e is exer name (same as owner_keystring)
            etxt = self.exercise_template.render(
                    summary=str_indent(row['summary_text']),
                    problem=str_indent(row['problem_text']),
                    answer=str_indent(row['answer_text']),
                    sage_python=str_indent( row['class_text'] ),
                    sections_text = row["sections_text"],
                    suggestive_name= row["suggestive_name"]
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




    def make_index(self,where='.',debug=False):
        """
        Produce rst code files from the database and an index reading first line of the %summary field.

        Command line use: 
            The ``where`` input argument, when specified,  will contain all details of Sphinx compilation.

        LINKS:

        http://code.activestate.com/recipes/193890-using-rest-restructuredtext-to-create-html-snippet/

        """

        html_index = SphinxExporter(self,where,debug)
        print "Index is at: "+ html_index.htmlfile

        if is_notebook():
            if where == '.': 
                #To open a browser
                pos = html_index.htmlfile.find(".")
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            elif 'data' in where:
                #To open a browser
                pos = html_index.htmlfile.find("/home")
                pos2 = html_index.htmlfile.find("/home",pos+1)
                if pos2>=0:
                    pos = pos2
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            else:
                #print "Index is at: "+ html_index.htmlfile
                print "See index at Megua button at top."
        else:
            print "firefox -no-remote ", html_index.htmlfile


    #def make_air(self,repetitions=2,dest='.',exerset=None):
    #    air = AirExporter(self,repetitions,exerset)
    #    if pcompile(air.fulltext, dest, "air_out",hideoutput=is_notebook(),runs=2):
    #        BookmarkList(os.path.join(dest,'air_out.pdf'))
    #    #print bm.bm_list #TODO: export to xml



    def make_index(self,where='.',debug=False):
        """
        Produce rst code files from the database and an index reading first line of the %summary field.

        Command line use: 
            The ``where`` input argument, when specified,  will contain all details of Sphinx compilation.

        LINKS:

        http://code.activestate.com/recipes/193890-using-rest-restructuredtext-to-create-html-snippet/

        """

        html_index = SphinxExporter(self,where,debug)
        print "Index is at: "+ html_index.htmlfile

        if is_notebook():
            if where == '.': 
                #To open a browser
                pos = html_index.htmlfile.find(".")
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            elif 'data' in where:
                #To open a browser
                pos = html_index.htmlfile.find("/home")
                pos2 = html_index.htmlfile.find("/home",pos+1)
                if pos2>=0:
                    pos = pos2
                html(r'<a href="%s" target=_blank>Press to open database index.</a>' % html_index.htmlfile[pos:])
            else:
                #print "Index is at: "+ html_index.htmlfile
                print "See index at Megua button at top."
        else:
            print "firefox -no-remote ", html_index.htmlfile



    def gallery(self,owner_keystring, ekey=None, edict=None):
        r"""Prints an exercise instance of a given type and output RST file for gallery.

        INPUT:

         - ``owner_keystring`` -- the class name.
         - ``ekey`` -- the parameteres will be generated for this random seed.
         - ``edict`` --  after random generation of parameters some of them could be replaced by the ones in this dict.

        OUTPUT:
            An instance of class named ``owner_keystring`` and output RST file for gallery.

        """
        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(owner_keystring)
        if not row:
            print "%s cannot be accessed on database" % owner_keystring
            return None
        #Create and print the instance
        ex_instance = exerciseinstance(row, ekey, edict)
        #generate one instance
        self.print_instance(ex_instance)
        #generate rst file

        summtxt =  ex_instance.summary()
        probtxt =  ex_instance.problem()
        answtxt =  ex_instance.answer()
        sname   =  ex_instance.name

        #Use jinja2 template to generate LaTeX.
        if 'CDATA' in answtxt:
            answtxt_woCDATA = re.subn(
                '<!\[CDATA\[(.*?)\]\]>', r'\1', 
                answtxt, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]
        else:
            answtxt_woCDATA = re.subn(
                '<choice>(.*?)</choice>', r'<b>Escolha:</b><br>\1<hr>', 
                answtxt, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]



        html_string = self.template("print_instance_html.html",
                sname=sname,
                summtxt=summtxt,
                probtxt=probtxt,
                answtxt=answtxt_woCDATA,
                ekey=ex_instance.ekey)

        #Produce files for pdf and png graphics if any tikz code embed on exercise
        #Ver ex.py: now latex images are produced in ex.problem() and ex.answer()
        #html_string = self.publish_tikz(sname,html_string)


        #file with html to export (extension txt prevents html display).

        #To be viewed on browser
        #f = open(sname+'.html','w')
        #f.write(html_string.encode('latin1'))
        #f.close()
        f = codecs.open(sname+'.html', mode='w', encoding='utf-8')
        f.write(html_string)
        f.close()

        rst_string = self.template("rst_instance.rst",
                sname=sname,
                summtxt=summtxt,
                probtxt=probtxt,
                answtxt=answtxt_woCDATA,
                ekey=ex_instance.ekey)

        #Produce files for pdf and png graphics if any tikz code embed on exercise
        #Ver ex.py: now latex images are produced in ex.problem() and ex.answer()
        #html_string = self.publish_tikz(sname,html_string)

        #file with html to export (extension txt prevents html display).

        #To be viewed on browser
        #f = open(sname+'.html','w')
        #f.write(html_string.encode('latin1'))
        #f.close()
        f = codecs.open(sname+'.rst', mode='w', encoding='utf-8')
        f.write(rst_string)
        f.close()


