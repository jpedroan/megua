# coding=utf-8

"""
MegSiacua -- Functions to work with one or a list of ExSiacua exercises.

READ THIS:  MegBook  inherits this class! MegBook is the author front-end.

AUTHORS:

- Pedro Cruz (2016-01): first modifications for use in SMC.


TESTS: check MegBook

"""


#*****************************************************************************
#       Copyright (C) 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  


class MegSiacua:
    r"""
    MegSiacua -- Functions to work with one or a list of ExSiacua exercises.

    See also MegBook that an author uses as a front-end.

    """


    #TODO: rever isto tudo
    def siacua(self,
               ekeys=[],
               course="calculo3",
               usernamesiacua="(no username)",
               level=1,
               slip=0.05,
               guess=0.25,
               discr=0.5,
               concepts = [ (0,  1) ],
               grid2x2=False,
               siacuatest=False,
               sendpost=True,
               verbose=False
              ):
        r"""

        INPUT:

        - ``ekeys``: list of numbers that generate the same problem instance.

        - ``course``: Right now could be "calculo3", "calculo2". Ask siacua administrator for more.

        - ``usernamesiacua``: username used by the author in the siacua system.

        - ``level``: (usually 1) I don't know what does this mean but it's an small integer number.

        - ``slip``: (0,...,1) The probability of knowing how to answer, commit a mistake.

        - ``guess``: (usually 0.25) The probability of guessing the right option.

        - ``discr``: (0,...,1) Parameter `discr` is the probability that a student knows how to select the right answer.

        - ``concepts``: a list like [(110, 0.3),(135, 0.7)] where 0.3+0.7 = 1 and 110 and 135 are codes of concepts.

        - ``grid2x2``: (usually False) Write exercise answering options in a 2x2 grid (useful for graphics).

        - ``siacuatest``: (usually False) If True, send data to a test machine.

        - ``sendpost``: (usually True) If True send information to siacua, otherwise simulates to check problems.

        - ``verbose``: (usually False) print the message received by siacua.

        OUTPUT:

        - this command prints the list of sended exercises for the siacua system.

        NOTE:

        - you can export between 3 and 6 wrong options and 1 right.

        TODO: securitykey: implemenent in a megua-server configuration file.

        LINKS:
            http://docs.python.org/2/library/json.html
            http://stackoverflow.com/questions/7122015/sending-post-request-to-a-webservice-from-python

        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.

        TESTS:

            ~/Dropbox/all/megua/archive$ sage jsontest.sage

        """

        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(self._current_unique_name)
        if not row:
            print "megsiacua module: %s cannot be accessed on database." % self._current_unique_name
            return

        #Create an instance (ekey=0 because it needs one.)
        ex_instance = self.exerciseinstance(row=row, ekey=0)

        #exercise instance will sent instances to siacua
        ex_instance.siacua(ekeys,course,usernamesiacua,level,slip,guess,discr,concepts,grid2x2,siacuatest,sendpost,verbose)

        #done
            

    def siacuapreview(self,ekeys,unique_name=None):
        r"""

        INPUT:

        - ``unique_name``: unique exercise name (name in "class E12X34_something_001(Exercise):").

        - ``ekeys``: list of numbers that generate the same problem instance.

        OUTPUT:

        - this command writes an html file with all instances.

        NOTE:

        - you can export between 3 and 6 wrong options and 1 right.

        EXAMPLE:

            sage: ex.siacuapreview(ekeys=[1,2,5])


        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.

        """

        if not unique_name:
            unique_name = self._current_unique_name

        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(unique_name)
        if not row:
            print "megsiacua module: %s cannot be accessed on database." % unique_name
            return
        #Create an instance (ekey=0 because it needs one.)
        ex_instance = self.exerciseinstance(row=row, ekey=0)

        #exercise instance will sent instances to siacua
        ex_instance.siacuapreview(ekeys)

#end class MegSiacua
