# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 04:54:54 2016

@author: jpedro
"""

r"""
xlatex.py -- export to pdflatex.

AUTHORS:

- Pedro Cruz (2014-10): initial version

TODO:
- break long lines to fit 80 chars in verbatim environment
- trim to much blank lines (only one for each)

NOTES:
- first version based on xsphinx.py module of megua

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  


#python package
import os
import shutil
import codecs
import jinja2
from string import join
import re
import textwrap
import unicodedata

#megua package
from localstore import ExIter
from csection import SectionClassifier, Section


    def amc(self,sheet_structure):
        r"""
        Generates a tex file ready to use in AMC for multiple choice 
        questions with:

        * "No one of the previous answers is correct",
        * groups or no groups of questions.

        INPUT:
        
        - `structure`: see below.

        Structure:
            Simple: no division in groups ("sections") in the final examination sheet.
            [ 
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
            ]

            Grouped: division in groups ("sections") in the final examination sheet.
            [ 
              [group_id,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
              ],
              [group_id,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
              ],
            ]


        """

        if type(sheet_structure[0]) == list:
            self.amc_grouped(sheet_structure)        
        else:
            self.amc_single(sheet_structure)
            
    def amc_grouped(self,problem_list):
        print "Not yet implemented: use only meg.amc( [exercise,ekey, exercise, ekey,... pairs] )"


    def amc_single(self,problem_list):
        r"""
        Generates a tex file ready to use in AMC for multiple choice 
        questions.
        See amc() first.

        Added options:
        * "No one of the previous answers is correct",

        INPUT:
        
        - `problem_list`: see below.

        Structure example:
            Simple: no division in groups ("sections") in the final examination sheet.
            [ 
                "E12X34_Calc_001", 10,  #specific problem key
                "E12X34_Calc_001", 20,  #specific problem key (repeat the template)
                "E12X34_Deriv_001"      #select a random key for this problem
            ]

        """

        #Build paired list (ex,ekey) adding a random ekey when
        #no key is given.
        i = 0
        n = len(problem_list)
        paired_list = []
        #print random.__module__
        rn = randint(0,10**5) #if user did not supplied an ekey.
        while i < (n-1):
            if type(problem_list[i])==str and type(problem_list[i+1])==str: #two problems
                paired_list.append( (problem_list[i], rn) ) 
                i += 1 #advance to position i+1
            elif type(problem_list[i])==str and type(problem_list[i+1])!=str: #!= probably a number
                paired_list.append( (problem_list[i], problem_list[i+1]) )
                i += 2 #advance to position i+2, consuming the ekey
        if i < n: #add last problem 
            paired_list.append( (problem_list[i], rn) )



        #amc template without groups for each question
        allproblems_text = ''
        for (problem_name,ekey) in paired_list:

            #generate problem and answer text (choices are in the answer part)

            #Get summary, problem and answer and class_text
            row = self.megbook_store.get_classrow(problem_name)
            if not row:
                print "amc_single: %s cannot be accessed on database" % problem_name
                continue
            #Create and print the instance
            ex_instance = exerciseinstance(row, int(ekey) )

            summary =  ex_instance.summary()
            problem = ex_instance.problem()
            answer = ex_instance.answer()
            problem_name =  ex_instance.name
    
            #Adapt for appropriate URL for images
            if ex_instance.image_list != []:
                problem = self._adjust_images_url(problem)
                answer = self._adjust_images_url(answer)
                #see siacua functions: self.send_images()


            #TODO: this lines are a copy of code in "siacua()".
            if ex_instance.has_multiplechoicetag:
                if ex_instance.image_list != []:
                    answer_list = [self._adjust_images_url(choicetxt) for choicetxt in ex_instance.collect_options_and_answer()]
                else:
                    answer_list = ex_instance.collect_options_and_answer()
            else:
                answer_list = ex_instance.answer_extract_options()


            #TODO: os CDATA tem que ser recuperados neste ficheiro e os <choice> ja estao no campo ex.all_choices.

            #generate amc problemtext

            problem_string = self.template("amc_element.tex",
                    problem_name=problem_name,
                    problem_text=html2latex(problem),
                    correcttext=html2latex(answer_list[0]),
                    wrongtext1=html2latex(answer_list[1]),
                    wrongtext2=html2latex(answer_list[2]),
                    wrongtext3=html2latex(answer_list[3]),
                    summtxt=latexcommentthis(summary),
                    detailedanswer=latexcommentthis(html2latex(answer_list[4])) 
                      #expected at position 4 the full answer.
            )

            #Convert the link below to \includegraphics{images/E12A34_cilindricas_0001-fig4-10.png}
            #<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/E12A34_cilindricas_0001-fig4-10.png'></img>
            problem_string = re.subn(
                """<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/(.*?)'></img>""",
                r'\n\includegraphics{images/\1}\n', 
                problem_string, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]

            #add this to allproblems_text
            allproblems_text += problem_string


        #Make a latex file to be compiled using amc program (or pdflatex).
        latextext_string = self.template("amc_latexfile.tex",
            ungroupedamcquestions=allproblems_text
        )

        f = open('amc_test.tex','w')
        f.write(latextext_string.encode('utf8'))  #latin1  <-- another option
        f.close()

        f = open('amcpt.sty','w')
        f.write(self.template("amcpt.sty"))
        f.close()

        f = open('amc_instructions.html','w')
        f.write(self.template("amc_instructions.html").encode('utf8'))
        f.close()

        os.system("zip -r images images > /dev/null 2>&1")

        os.system("pdflatex -interact=nonstopmode {0} > /dev/null 2>&1".format("amc_test.tex"))
        os.system("rm amc_test.amc amc_test.log amc_test.aux > /dev/null 2>&1") 
        #os.system("rm -r images > /dev/null 2>&1")
    

    def getexercise(self,exname,ekey):
        """Put the contents of an exercise in megbook variables."""

        #Create exercise instance
        row = self.megbook_store.get_classrow(exname)
        if not row:
            print "Exercise %s not found." % exname
            return

        ex_instance = exerciseinstance(row, ekey=ekey)

        self.c_problem = ex_instance.problem()
        self.c_answer = ex_instance.answer()
        self.c_allchoices = ex_instance.all_choices

    def getproblem(self):
        return self.c_problem

    def getanswer(self):
        return self.c_answer

    def getoption(self,pos):
        return self.c_allchoices[pos]


    def _adjust_images_url(self, input_text):
        #This is a clone of the MegBookWeb function.
        #Check that for changes.
        """the url in problem() and answer() is <img src='images/filename.png'>
        Here we replace images/ by the public dropbox folder"""

        target = r"https://dl.dropboxusercontent.com/u/10518224/megua_images"
        img_pattern = re.compile(r"src='images/", re.DOTALL|re.UNICODE)

        (new_text,number) = img_pattern.subn(r"src='%s/" % target, input_text) #, count=1)
        #print "===> Replacement for %d url images." % number
        return new_text


TODO

    def amc(self,sheet_structure):
        r"""
        Generates a tex file ready to use in AMC for multiple choice 
        questions with:

        * "No one of the previous answers is correct",
        * groups or no groups of questions.

        INPUT:
        
        - `structure`: see below.

        Structure:
            Simple: no division in groups ("sections") in the final examination sheet.
            [ 
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
            ]

            Grouped: division in groups ("sections") in the final examination sheet.
            [ 
              [group_id,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
              ],
              [group_id,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
                exercise_name, optinal ekey,
              ],
            ]


        """

        if type(sheet_structure[0]) == list:
            self.amc_grouped(sheet_structure)        
        else:
            self.amc_single(sheet_structure)
            
    def amc_grouped(self,problem_list):
        print "Not yet implemented: use only meg.amc( [exercise,ekey, exercise, ekey,... pairs] )"


    def amc_single(self,problem_list):
        r"""
        Generates a tex file ready to use in AMC for multiple choice 
        questions.
        See amc() first.

        Added options:
        * "No one of the previous answers is correct",

        INPUT:
        
        - `problem_list`: see below.

        Structure example:
            Simple: no division in groups ("sections") in the final examination sheet.
            [ 
                "E12X34_Calc_001", 10,  #specific problem key
                "E12X34_Calc_001", 20,  #specific problem key (repeat the template)
                "E12X34_Deriv_001"      #select a random key for this problem
            ]

        """

        #Build paired list (ex,ekey) adding a random ekey when
        #no key is given.
        i = 0
        n = len(problem_list)
        paired_list = []
        #print random.__module__
        rn = randomlib.randint(0,10**5) #if user did not supplied an ekey.
        while i < (n-1):
            if type(problem_list[i])==str and type(problem_list[i+1])==str: #two problems
                paired_list.append( (problem_list[i], rn) ) 
                i += 1 #advance to position i+1
            elif type(problem_list[i])==str and type(problem_list[i+1])!=str: #!= probably a number
                paired_list.append( (problem_list[i], problem_list[i+1]) )
                i += 2 #advance to position i+2, consuming the ekey
        if i < n: #add last problem 
            paired_list.append( (problem_list[i], rn) )



        #amc template without groups for each question
        allproblems_text = ''
        for (problem_name,ekey) in paired_list:

            #generate problem and answer text (choices are in the answer part)

            #Get summary, problem and answer and class_text
            row = self.megbook_store.get_classrow(problem_name)
            if not row:
                print "amc_single: %s cannot be accessed on database" % problem_name
                continue
            #Create and print the instance
            ex_instance = exerciseinstance(row, int(ekey) )

            summary =  ex_instance.summary() 
            problem = ex_instance.problem()
            answer = ex_instance.answer()
            problem_name =  ex_instance.name
    
            #Adapt for appropriate URL for images
            if ex_instance.image_list != []:
                problem = self._adjust_images_url(problem)
                answer = self._adjust_images_url(answer)
                #see siacua functions: self.send_images()


            #TODO: this lines are a copy of code in "siacua()".
            if ex_instance.has_multiplechoicetag:
                if ex_instance.image_list != []:
                    answer_list = [self._adjust_images_url(choicetxt) for choicetxt in self._siacua_answer_frominstance(ex_instance)]
                else:
                    answer_list = ex_instance.collect_options_and_answer()
            else:
                answer_list = ex_instance.answer_extract_options()


            #TODO: os CDATA tem que ser recuperados neste ficheiro e os <choice> ja estao no campo ex.all_choices.

            #generate amc problemtext

            problem_string = self.template("amc_element.tex",
                    problem_name=problem_name,
                    problem_text=html2latex(problem),
                    correcttext=html2latex(answer_list[0]),
                    wrongtext1=html2latex(answer_list[1]),
                    wrongtext2=html2latex(answer_list[2]),
                    wrongtext3=html2latex(answer_list[3]),
                    summtxt=self._latexcommentthis(summary),
                    detailedanswer=latexcommentthis(html2latex(answer_list[4])) 
                      #expected at position 4 the full answer.
            )

            #Convert the link below to \includegraphics{images/E12A34_cilindricas_0001-fig4-10.png}
            #<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/E12A34_cilindricas_0001-fig4-10.png'></img>
            problem_string = re.subn(
                """<img src='https://dl.dropboxusercontent.com/u/10518224/megua_images/(.*?)'></img>""",
                r'\n\includegraphics{images/\1}\n', 
                problem_string, 
                count=0,
                flags=re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]

            #add this to allproblems_text
            allproblems_text += problem_string


        #Make a latex file to be compiled using amc program (or pdflatex).
        latextext_string = self.template("amc_latexfile.tex",
            ungroupedamcquestions=allproblems_text
        )

        f = open('amc_test.tex','w')
        f.write(latextext_string.encode('utf8'))  #latin1  <-- another option
        f.close()

        f = open('amcpt.sty','w')
        f.write(self.template("amcpt.sty"))
        f.close()

        f = open('amc_instructions.html','w')
        f.write(self.template("amc_instructions.html").encode('utf8'))
        f.close()

        os.system("zip -r images images > /dev/null 2>&1")

        os.system("pdflatex -interact=nonstopmode {0} > /dev/null 2>&1".format("amc_test.tex"))
        os.system("rm amc_test.amc amc_test.log amc_test.aux > /dev/null 2>&1") 
        #os.system("rm -r images > /dev/null 2>&1")


