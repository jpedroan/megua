r"""
Classify by sections.

AUTHOR:

- Pedro Cruz (2012-01): initial version

"""

#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

from localstore import ExIter

class SectionClassifier:
    """
    An exercise could contain um its %summary tag line a description of section
    in form::

       %sumary section descriptive text; subsection descriptive text; etc

    The class transform contents of some MegUA database into a tree of sections specifying exercises as leaves.
    Then, this tree can be flushed out to some file or output system.

    STRUTURE SAMPLE::

        contents -> { 'Section1': Section('Section1',0), 'Section2': Section('Section2',0) }
        For each Section object see below in this file.
        A brief description is:
            * a SectionClassifier is the "book" made with keys (chapter names) that are keys of a dictionary.
            * SectionClassifier is a dictionary: keys are the chapter names and the values are Section objects.
            * a Section object is defined by 
                * a name (the key of the SectionClassifiers appears again in sec_name)
                * level (0 if it is top level sections: chapters, and so on)
                *  a list of exercises beloging to the section and
                * a dictionary of subsections (again Section objects)
            * Section = (sec_name, level, [list of exercises names], dict( subsections ) )

    EXAMPLES::

    .. test with: sage -python -m doctest csection.py 

    Create or edit a database::

       >>> from all import *
       >>> meg = MegBook(r'./.testoutput/csection.sqlite')
       MegBook opened. Execute `MegBook?` for examples of usage.
       Templates for 'pt_pt' language.


    Save a new or changed exercise::

       >>> txt=r'''
       ... %Summary Primitives; Imediate primitives; Trigonometric 
       ...   
       ... %Problem Some Name
       ... What is the primitive of $a x + b@()$ ?
       ... 
       ... %Answer
       ... The answer is $prim+C$, for $C in \mathbb{R}$.
       ... 
       ... class E28E28_pimtrig_001(Exercise):
       ...     pass
       ... '''
       >>> meg.save(txt,dest='.testoutput')
       Testing python/sage class 'E28E28_pimtrig_001' with 100 different keys.
           No problems found in this test.
          Compiling 'E28E28_pimtrig_001' with pdflatex.
          No errors found during pdflatex compilation. Check E28E28_pimtrig_001.log for details.
       Exercise name E28E28_pimtrig_001 inserted or changed.

       >>> txt=r'''
       ... %Summary Primitives; Imediate primitives; Trigonometric 
       ...   
       ... %Problem Some Name2
       ... What is the primitive of $a x + b@()$ ?
       ... 
       ... %Answer
       ... The answer is $prim+C$, for $C in \mathbb{R}$.
       ... 
       ... class E28E28_pimtrig_002(Exercise):
       ...     pass
       ... '''
       >>> meg.save(txt,dest='.testoutput')
       Testing python/sage class 'E28E28_pimtrig_002' with 100 different keys.
           No problems found in this test.
          Compiling 'E28E28_pimtrig_002' with pdflatex.
          No errors found during pdflatex compilation. Check E28E28_pimtrig_002.log for details.
       Exercise name E28E28_pimtrig_002 inserted or changed.

       >>> txt=r'''
       ... %Summary Primitives; Imediate primitives; Polynomial 
       ...   
       ... %Problem Some Problem 1
       ... What is the primitive of $a x + b@()$ ?
       ... 
       ... %Answer
       ... The answer is $prim+C$, for $C in \mathbb{R}$.
       ... 
       ... class E28E28_pdirect_001(Exercise):
       ...     pass
       ... '''

       >>> meg.save(txt,dest='.testoutput')
       Testing python/sage class 'E28E28_pdirect_001' with 100 different keys.
           No problems found in this test.
          Compiling 'E28E28_pdirect_001' with pdflatex.
          No errors found during pdflatex compilation. Check E28E28_pdirect_001.log for details.
       Exercise name E28E28_pdirect_001 inserted or changed.
       >>> txt=r'''
       ... %Summary  
       ...   
       ... No summary problem.
       ...
       ... %Problem 
       ... What is the primitive of $a x + b@()$ ?
       ... 
       ... %Answer
       ... The answer is $prim+C$, for $C in \mathbb{R}$.
       ... 
       ... class E28E28_pdirect_003(Exercise):
       ...     pass
       ... '''
       >>> meg.save(txt,dest='.testoutput')
       Each exercise can belong to a section/subsection/subsubsection. 
       Write sections using ';' in the '%summary' line. For ex., '%summary Section; Subsection; Subsubsection'.
       <BLANKLINE>
       Each problem can have a suggestive name. 
       Write in the '\%problem' line a name, for ex., '\%problem The Fish Problem'.
       <BLANKLINE>
       Testing python/sage class 'E28E28_pdirect_003' with 100 different keys.
           No problems found in this test.
          Compiling 'E28E28_pdirect_003' with pdflatex.
          No errors found during pdflatex compilation. Check E28E28_pdirect_003.log for details.
       Exercise name E28E28_pdirect_003 inserted or changed.

       >>> s = SectionClassifier(meg.megbook_store)
       >>> s.textprint()
       Primitives
        Imediate primitives
         Polynomial
         > E28E28_pdirect_001
         Trigonometric
         > E28E28_pimtrig_001
         > E28E28_pimtrig_002
       E28E28_pdirect
       > E28E28_pdirect_003

    """

    def __init__(self,megbook_store,max_level=4,debug=False,exerset=None):
        #save megstore reference
        self.megbook_store = megbook_store
        self.max_level = max_level
        #Exercise set or none for all
        self.exercise_set = exerset
        #dictionary of sections
        self.contents = dict()
        self.classify()


    def classify(self):
        """
        Classify by sections.
        """        

        for row in ExIter(self.megbook_store):
            if self.exercise_set and not row['unique_name'] in self.exercise_set:
                continue
            #get a list in form ["section", "subsection", "subsubsection", ...]
            sec_list = str_to_list(row['sections_text'])
            if sec_list == [] or sec_list == [u'']:
               sec_list = [ first_part(row['unique_name']) ]
            #sec_list contain at least one element.
            if not sec_list[0] in self.contents:
                self.contents[sec_list[0]] = Section(sec_list[0])
            #sec_list contains less than `max_level` levels
            subsec_list = sec_list[1:self.max_level]
            self.contents[sec_list[0]].add(row['unique_name'],subsec_list)


    def textprint(self):
        """
        Textual print of all the contents.
        """
        for c in self.contents:
            self.contents[c].textprint()

    


class Section:
    r"""

    Section = (sec_name, level, [list of exercises names], dict( subsections ) )

    """
    def __init__(self,sec_name,level=0):
        self.sec_name = sec_name
        self.level = level
        self.exercises = []
        self.subsections = dict()

  
    def add(self,exname,sections):

        if sections == []:
            self.exercises.append(exname)
            return
        
        if not sections[0] in self.subsections:
            self.subsections[sections[0]] = Section(sections[0],self.level+1)

        self.subsections[sections[0]].add(exname,sections[1:])

    def textprint(self):
        """
        Textual print of the contents of this section and, recursivly, of the subsections.
        """
        sp = " "*self.level
        print sp + self.sec_name
        for e in self.exercises:
            print sp+r"> "+e
        for sub in self.subsections:
            self.subsections[sub].textprint()

        

def str_to_list(s):
    """
    Convert::
  
       'section description; subsection description; subsubsection description'

    into::

       [ 'section description', 'subsection description', 'subsubsection description']

    """
    sl = s.split(';')
    for i in range(len(sl)):
        sl[i] = sl[i].strip()
    return sl


def first_part(s):
    """
    Usually exercise are named like `E12X34_name_001` and this routine extracts `E12X34` or `top` if no underscore is present.
    """
    p = s.find("_")
    p = s.find("_",p+1)
    if p!=-1:
        s = s[:p]
    if s=='':
        s = 'top'
    return s


