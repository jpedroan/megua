r"""
xair.py -- export to latex format to be used on Adobe Air.

AUTHORS:

- Pedro Cruz (2012-01): initial version

LINKS::

"""


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
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
from ex import exerciseinstance, to_unicode
from platex import pcompile

#pdfminer
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdftypes import PDFStream, PDFObjRef, resolve1, stream_value



class AirExporter:
    """
    Produce a latex code file from the database and an index reading first line of the %summary field.

    LINKS:

    """

    def __init__(self,megbook,repetitions=2,exerset=None,debug=False,dest='.'):

        #save megstore reference
        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store

        #Exercise set or None for all
        self.exercise_set = exerset

        #Number of random repetitions of each exercise
        self.repetitions = repetitions

        
        self.template_row = self.megbook.env.get_template("air_row.tex")

        self._build_sectionstext()

        self.fulltext = self.megbook.template("air_main.tex",allsections=self.allsections_text)
        #removed: see MegBook.make_air()
        #pcompile(self.fulltext, dest, "air_out",hideoutput=is_notebook())


    def _build_sectionstext(self):

        #Create tree structure        
        self.sc = SectionClassifier(self.megbook_store,max_level=2,exerset=self.exercise_set)

        self.lines = []

        #Root sections
        for section in self.sc.contents.itervalues():

            #Store exercices of subsections.
            self._get_subsections(section)

        #Join all lines with \n
        self.allsections_text = join(self.lines,"\n")


    def _get_subsections(self,section):

        #Write (sub*)section header
        if section.level == 0:
            txt = r'\clearpage\section{%s}' % section.sec_name
        elif section.level == 1:
            txt = r'\subsection{%s}' % section.sec_name
        elif section.level == 2:
            txt = r'\subsubsection{%s}' % section.sec_name
        elif section.level==3:
            txt = r'\subsubsubsection{%s}' % section.sec_name
        else:
            txt = r'\textbf{%s}' % section.sec_name
        self.lines.append(txt)

        #Store exercises of this section 
        self._add_exercises(section)

        #Go on for subsections
        for subsection in section.subsections.itervalues():
            self._get_subsections(subsection)


    def _add_exercises(self,section):
        """
        Add LaTeX representation.
        """
        for e in section.exercises:
            for rep in range(self.repetitions):                
                self.lines.append( self._get_exercise_text(e,rep,section.level) )

            
    def _get_exercise_text(self,unique_name,ekey,elevel):

        if elevel<1: #exercise is not a leaf of the tree. TODO: improve
            print "Air: Exercise %s needs section and subsection on %%summary tag." % unique_namestring
            utxt = u"\n\n{\\small Exercise \\verb'%s' needs section and subsection on \\%%summary tag.}\n\n" % unique_namestring
            return utxt

        row = self.megbook_store.get_classrow(unique_name)
        if not row:
            utxt = "MegUA: '%s' cannot be accessed on database '%s'" % (unique_name,self.megbook_store.local_store_filename)
            print utxt
            return utxt

        # http://docs.python.org/tutorial/errors.html
        try:
            ex_instance = exerciseinstance(row, ekey=ekey, edict=None)
            utxt = self.template_row.render(
                ename   =  row['suggestive_name'], 
                problem =  to_unicode( ex_instance.problem() ), 
                answer  =  to_unicode( ex_instance.answer() ),
                elabel  =  "%s-%d" % ( remove_underscore(unique_name), ekey),
                elevel = elevel+2,
                ekey=ekey,
                exname=unique_namestring
            )
        except:
            utxt = u"Exercise %s could not be created (ekey=%d).\n" % (unique_name,ekey)

        return utxt


class BookmarkList:
    r"""
    pdfminer to get bookmarks and pages to xml
    """

    def __init__(self,pdf_fn):

        self.pdf_fn = pdf_fn
        self.bm_list = []

        fp = open(pdf_fn, 'rb')
        parser = PDFParser(fp)
        doc = PDFDocument()
        parser.set_document(doc)
        doc.set_parser(parser)
        #doc.initialize(password)

        pages = dict( (page.pageid, pageno) for (pageno,page) in enumerate(doc.get_pages()) )

        def resolve_dest(dest):
            if isinstance(dest, str):
                dest = resolve1(doc.get_dest(dest))
            elif isinstance(dest, PSLiteral):
                dest = resolve1(doc.get_dest(dest.name))
            if isinstance(dest, dict):
                dest = dest['D']
            return dest


        # Get the outlines of the document.
        outlines = doc.get_outlines()
        for (level,title,dest,a,se) in outlines:
            #print "(level,title,dest,a,se)",(level,title,dest,a,se)
            #print a.resolve()
            pageno = None
            if dest:
                #dest = resolve_dest(dest)
                pageno = pages[dest[0].objid]
            elif a:
                action = a.resolve()
                if isinstance(action, dict):
                    subtype = action.get('S')
                    if subtype and repr(subtype) == '/GoTo' and action.get('D'):
                        dest = resolve_dest(action['D'])
                        #print dest
                        pageno = pages[dest[0].objid]

            #if pageno is not None:
            #    print "Page = ", pageno
            #else:
            #    print "no page"

            self.bm_list.append( (level,title,pageno)  )

        #close filename
        fp.close()


        #Create string with contents
        filename = os.path.splitext(pdf_fn)[0]  # get rid of extension
        fxml = open(filename + '.xml','w')
        fxml.write('<?xml version="1.0" encoding="Windows-1252" ?>\n')
        fxml.write('<Bookmarks>\n')
        for (i,b) in enumerate(self.bm_list):
            fxml.write('\
\t<Bookmark>\n\
\t\t<Item>{0}</Item>\n\
\t\t<Level>{1}</Level>\n\
\t\t<Name>{2}</Name>\n\
\t\t<Page>{3}</Page>\n\
\t</Bookmark>\n'.format(i+1,b[0],b[1].encode('utf-8'),b[2]))
        fxml.write('</Bookmarks>\n')
        fxml.close()




# -------------------------------

def remove_underscore(txt):
    r"""
    
    EXAMPLES::
        
        sage: remove_underscore("ABC_caso_123")
        'ABCcaso123'
        sage: remove_underscore("ABC_caso")
        'ABCcaso'
        sage: remove_underscore("ABC")
        'ABC'
    """
        
    s_pos = 0
    pos = txt.find("_")
    out_t = ''
    while pos>-1:
        out_t += txt[s_pos:pos] + '-'
        s_pos = pos+1
        pos = txt.find("_",s_pos)
    out_t += txt[s_pos:]
    return out_t




