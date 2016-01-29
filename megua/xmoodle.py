r"""
xmoodle.py -- export to moodle xml format.


AUTHORS:

- Pedro Cruz (2012-10): initial version

LINKS::

   http://docs.moodle.org/23/en/Embedded_Answers_%28Cloze%29_question_type
   http://docs.moodle.org/20/en/Import_questions


NOTES: 
   from sphinx import cmdline
   cmdline??

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
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
from ex import exerciseinstance


class MoodleExporter:
    """
    Produce a xml file from the database with categories sections in the %summary field.

    LINKS about Moodle::

        http://docs.moodle.org/23/en/Embedded_Answers_%28Cloze%29_question_type
        http://docs.moodle.org/20/en/Import_questions
        
    LINKS about XML::
    
        http://www.w3schools.com/xml/xml_cdata.asp

    """


    def __init__(self,megbook,where=None,debug=False):
      
        #save megstore reference
        self.megbook = megbook
        self.megbook_store = self.megbook.megbook_store

        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.exercise_template = self.megbook.env.get_template("moodle-cloze.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_cloze.xml"
            raise e

        # -----------------
        # Open output file
        # -----------------
        #TODO: use this base name:self.megbook_store.local_store_filename
        self.xmlfilename = "quiz.xml"
        self.xmlfile = codecs.open(self.xmlfilename, encoding='utf-8', mode='w')
        self.xmlfile.write('<?xml version="1.0" encoding="utf-8"?>\n<quiz>\n')


        #Save to files and build html.
        self._save_to_xmlfile()


        # -----------------
        # Close output file
        # -----------------
        self.xmlfile.write("\n</quiz>")
        self.xmlfile.close()

        #TODO: provide a link to notebook user:
        #self.htmlfile = os.path.join(self.sphinx_folder,'build/html/index.html')


    def _save_to_xmlfile(self):

        all_ex = []
        for row in ExIter(self.megbook_store):

            for ekey in range(2): #TODO: allow user change.

                ex_instance = exerciseinstance(row, ekey)
            
                probtxt =  ex_instance.problem()
                answtxt =  ex_instance.answer()

                xml_string = self.exercise_template.render(
                    sections= self._get_sections(row['sections_text']),
                    exercisename=row['owner_key'],
                    ekey=ex_instance.ekey,    
                    problemname=row['suggestive_name'],
                    problemtext=probtxt,
                    answertext=answtxt)


                self.xmlfile.write(xml_string)


    def _get_sections(self,sectionstxt):
        """
        LINKS::
    
            http://stackoverflow.com/questions/2054746/how-to-search-and-replace-utf-8-special-characters-in-python?rq=1
        """   
        s = "megua/"+sectionstxt.replace("; ","/") #case "; " by "/"
        return s.replace(";","/") #possible case without space: ";" by "/"


    #def _parse(self, ex_instance):
    #    """
    #    Get Moodle Type Question of the %problem and generate proper xml.
    #    """
    #    probtxt  =  ex_instance.problem()
    #    if string.find(probtxt, r"%multiplechoice" )!=-1:
    #
    #    else:
    #        #Assume "cloze" question type



def lang_set(s):
    if s == 'pt_pt':
        return 'pt_br'
    else:
        return s


VER ISTO
        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.cloze_template = self.env.get_template("moodle-cloze.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_cloze.xml"
            raise e



        # -------------------------------
        # Set the Exercise print template
        # -------------------------------
        try:
            self.mchoice_template = self.env.get_template("moodle-mchoice.xml")
        except jinja2.exceptions.TemplateNotFound as e:
            print "MegUA -- missing template moodle_mchoice.xml"
            raise e


    def moodle(self, exname, questiontype="mchoice", many=10,  ekey=0, where='.'):
        """
        Save an exercse to moodle xml file format.

	INPUT:

	- exname: string with exercise identification name.
	- questiontype: "mchoice" or "cloze"
	- many: how many samples (starting ekey generated key).
	- ekeys: random values generation key.
        - where: local folder to store data.

        EXAMPLES:

        Full use of parameters::

            sage: meg.moodle("E12A34_Aplic_DerivadasE1_002", "mchoice", many=10, ekey=100)

        Less parameters::

            sage: meg.moodle("E12A34_Aplic_DerivadasE1_002", many=10 )

        """

        #If does not exist create
        if not os.path.exists(where):
            os.makedirs(where)


        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        questions_xml = unicode('')

        for e_number in range(many):

            #Create exercise instance
            ex_instance = exerciseinstance(row, ekey= ekey + e_number)

            if questiontype=='mchoice':
                questions_xml += self.mchoice_template.render(
                    sections= m_get_sections(row['sections_text']),
		    exercisename = exname,
		    ekey = e_number,
                    problemname=row['suggestive_name'],
                    answertext = ex_instance.answer(),
                    problemtext = ex_instance.problem()
                )
            else:
                questions_xml += self.cloze_template.render(
                    sections= m_get_sections(row['sections_text']),
		    exercisename = exname,
		    ekey = e_number,
                    problemname=row['suggestive_name'],
                    answertext = ex_instance.answer(),
                    problemtext = ex_instance.problem()
                )


        # -----------------
        # output file
        # -----------------
        xmlfilename = "quiz-%s.xml" % exname
        xmlfile = codecs.open(xmlfilename, encoding='utf-8', mode='w')
        xmlfile.write('<?xml version="1.0" encoding="utf-8"?>\n<quiz>\n')
        xmlfile.write(questions_xml)
        xmlfile.write("\n</quiz>")
        xmlfile.close()


