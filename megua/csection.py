# coding=utf8

r"""
csection.py -- Create a tree of contents, organized by sections and inside 
sections the exercises unique_name.


AUTHOR:

- Pedro Cruz (2012-01): initial version
- Pedro Cruz (2016-03): improvment for smc


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

    EXAMPLES:


    Test with:
    
::

    sage -t csection.py


    Create or edit a database:

::

       sage: from megua.megbook import MegBook
       sage: meg = MegBook(r'_input/csection.sqlite')


    Save a new or changed exercise

::

       sage: txt=r'''
       ....: %Summary Primitives; Imediate primitives; Trigonometric 
       ....:   
       ....:  Here, is a summary. 
       ....:   
       ....: %Problem Some Name
       ....: What is the primitive of $a x + b@()$ ?
       ....: 
       ....: %Answer
       ....: The answer is $prim+C$, for $C in \mathbb{R}$.
       ....: 
       ....: class E28E28_pimtrig_001(ExerciseBase):
       ....:     pass
       ....: '''
       sage: meg.save(txt)
       -------------------------------
       Instance of: E28E28_pimtrig_001
       -------------------------------
       ==> Summary:
       Here, is a summary.
       ==> Problem instance
       What is the primitive of $a x + b$ ?
       ==> Answer instance
       The answer is $prim+C$, for $C in \mathbb{R}$.

       sage: txt=r'''
       ....: %Summary Primitives; Imediate primitives; Trigonometric 
       ....:   
       ....:  Here, is a summary. 
       ....:   
       ....: %Problem Some Name2
       ....: What is the primitive of $a x + b@()$ ?
       ....: 
       ....: %Answer
       ....: The answer is $prim+C$, for $C in \mathbb{R}$.
       ....: 
       ....: class E28E28_pimtrig_002(ExerciseBase):
       ....:     pass
       ....: '''
       sage: meg.save(txt)
       -------------------------------
       Instance of: E28E28_pimtrig_002
       -------------------------------
       ==> Summary:
       Here, is a summary.
       ==> Problem instance
       What is the primitive of $a x + b$ ?
       ==> Answer instance
       The answer is $prim+C$, for $C in \mathbb{R}$.

       sage: txt=r'''
       ....: %Summary Primitives; Imediate primitives; Polynomial 
       ....:   
       ....:  Here, is a summary. 
       ....:   
       ....: %Problem Some Problem 1
       ....: What is the primitive of $a x + b@()$ ?
       ....: 
       ....: %Answer
       ....: The answer is $prim+C$, for $C in \mathbb{R}$.
       ....: 
       ....: class E28E28_pdirect_001(ExerciseBase):
       ....:     pass
       ....: '''

       sage: meg.save(txt)
       -------------------------------
       Instance of: E28E28_pdirect_001
       -------------------------------
       ==> Summary:
       Here, is a summary.
       ==> Problem instance
       What is the primitive of $a x + b$ ?
       ==> Answer instance
       The answer is $prim+C$, for $C in \mathbb{R}$.
       sage: txt=r'''
       ....: %Summary  
       ....:   
       ....:  Here, is a summary. 
       ....:   
       ....: %Problem 
       ....: What is the primitive of $a x + b@()$ ?
       ....: 
       ....: %Answer
       ....: The answer is $prim+C$, for $C in \mathbb{R}$.
       ....: 
       ....: class E28E28_pdirect_003(ExerciseBase):
       ....:     pass
       ....: '''
       sage: meg.save(txt)
       Each exercise can belong to a section/subsection/subsubsection. 
       Write sections using ';' in the '%summary' line. For ex., '%summary Section; Subsection; Subsubsection'.
       <BLANKLINE>
       Each problem can have a suggestive name. 
       Write in the '%problem' line a name, for ex., '%problem The Fish Problem'.
       <BLANKLINE>
       Check exercise E28E28_pdirect_003 for the above warnings.
       -------------------------------
       Instance of: E28E28_pdirect_003
       -------------------------------
       ==> Summary:
       Here, is a summary.
       ==> Problem instance
       What is the primitive of $a x + b$ ?
       ==> Answer instance
       The answer is $prim+C$, for $C in \mathbb{R}$.

    Travel down the tree sections:

::

       sage: s = SectionClassifier(meg.megbook_store)
       sage: s.textprint()
       Primitives
        Imediate primitives
         Polynomial
         > E28E28_pdirect_001
         Trigonometric
         > E28E28_pimtrig_001
         > E28E28_pimtrig_002
       E28E28_pdirect
       > E28E28_pdirect_003


    Testing a recursive iterator:

::

       sage: meg = MegBook("_input/paula.sqlite") 
       sage: s = SectionClassifier(meg.megbook_store)
       sage: for section in s.section_iterator():
       ....:     print section
       

"""

#*****************************************************************************
#       Copyright (C) 2011,2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#PYHTON modules
import collections
  
#MEGUA modules
from megua.localstore import ExIter



class SectionClassifier:
    """

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

    

    def section_iterator(self):
        r"""
        OUTPUT:
        
        - an iterator yielding (secname, sorted exercises)
        """
        # A stack-based alternative to the traverse_tree method above.
        od_top = collections.OrderedDict(sorted(self.contents.items()))
        stack = []
        for secname,section in od_top.iteritems():
            stack.append(section)
        while stack:
            section_top = stack.pop(0) #remove left element
            yield section_top
            od_sub = collections.OrderedDict(sorted(section_top.subsections.items()))
            desc = []
            for secname,section in od_sub.iteritems():
                desc.append(section)
            stack[:0] = desc #add elemnts from desc list at left (":0")
    

class Section:
    r"""

    Section = (sec_name, level, [list of exercises names], dict( subsections ) )

    """
    def __init__(self,sec_name,level=0):
        self.sec_name = sec_name
        self.level = level
        #Exercises of this section (self).
        self.exercises = []
        #This section (self) can have subsections.
        self.subsections = dict()

    def __str__(self):
        return self.level*" " + self.sec_name.encode("utf8") + " has " + str(len(self.exercises))

    def __repr__(self):
        return self.level*" " + self.sec_name.encode("utf8") + " has " + str(len(self.exercises))
  
    def add(self,exname,sections):
        r"""
        Recursive function to add an exercise to """

        if sections == []:
            self.exercises.append(exname)
            self.exercises.sort()
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


