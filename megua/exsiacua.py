# -*- coding: utf-8 -*-

"""
Created on Sun Jan 24 04:52:15 2016

@author: jpedro
"""

r"""
MegBook -- build your own database of exercises in several markup languages.

AUTHORS:

- Pedro Cruz (2012-06): initial version (based on megbook.py)
- Pedro Cruz (2016-01): first modifications for use in SMC.

"""

# Abstract function
# raise NotImplementedError( "Should have implemented this" )


#*****************************************************************************
#       Copyright (C) 2012 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  


    def exercise_compiletest(self,row,dest='.',silent=False):
        r"""
        pdflatex compilation test to check for error. 
        A new exercise is not entering the database if it has latex errors.
        """

        #create an instance
        ex_instance = exerciseinstance(row)

        #Use jinja2 template to generate LaTeX.
        latex_string = self.template("print_instance_latex.tex",
            sname=ex_instance.name,
            summtxt=ex_instance.summary(),
            probtxt=ex_instance.problem(),
            answtxt=ex_instance.answer(),
            ekey = ex_instance.ekey,
        )

        if not silent:
            print "Compiling '%s' with pdflatex." % row['owner_key']

        #TODO: put this in other place
        latex_error_pattern = re.compile(r"!.*?l\.\d+(.*?)$",re.DOTALL|re.M)

        try:
            pcompile(latex_string,dest,row['owner_key'])
        except subprocess.CalledProcessError as err:
            #Try to show the message to user
            #print "Error:",err
            #print "returncode:",err.returncode
            #print "output:",err.output
            print "================"
            match = latex_error_pattern.search(err.output) #create an iterator
            if match:
                print match.group(0)
            else:
                print "There was a problem with an latex file."
            print "You can download %s.tex and use your windows LaTeX editor to help find the error." % ex_instance.name 
            print "================"
            return False

        return True
            



    def print_instance(self, ex_instance):
        """
        After producing an exercise template or requesting a new instance of some exercise
        this routine will print it on notebook notebook or command line mode. It also should
        give a file were the user can find text markup (latex or html, etc).
        """

        #Use jinja2 template to generate LaTeX.
        latex_string = self.template(
            "print_instance_latex.tex",
            sname=ex_instance.name,
            summtxt=ex_instance.summary(),
            probtxt=ex_instance.problem(),
            answtxt=ex_instance.answer(),
            ekey=ex_instance.ekey)

        #Produce PDF file from LaTeX.
        pcompile(latex_string,'.',sname, hideoutput=True)

