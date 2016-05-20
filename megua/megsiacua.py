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
    def siacua(self,unique_name=None,ekeys=[],sendpost=False,course="calculo3",usernamesiacua="",grid2x2=0,siacuatest=False):
        r"""

        INPUT:

        - ``unique_name``: unique exercise name (name in "class E12X34_something_001(Exercise):").

        - ``ekeys``: list of numbers that generate the same problem instance.

        - ``sendpost``: if True send information to siacua.

        - ``course``: Right now could be "calculo3", "calculo2". Ask siacua administrator for more.

        - ``usernamesiacua``: username used by the author in the siacua system.

        - ``grid2x2``: write user options in multiplechoice in a 2x2 grid (useful for graphics) values in {0,1}.

        OUTPUT:

        - this command prints the list of sended exercises for the siacua system.

        NOTE:

        - you can export between 3 and 6 wrong options and 1 right.

        EXAMPLE:

            sage: meg.siacua(exname="E97K50_Laplace_001_siacua",ekeys=[1,2,5],sendpost=False,course="calculo2",usernamesiacua="jeremias")


        LINKS:
            http://docs.python.org/2/library/json.html
            http://stackoverflow.com/questions/7122015/sending-post-request-to-a-webservice-from-python

        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.


        """

        if not unique_name:
            unique_name = self._unique_name

        #Get summary, problem and answer and class_text
        row = self.megbook_store.get_classrow(unique_name)
        if not row:
            print "megsiacua module: %s cannot be accessed on database." % unique_name
            return
        
        #Create an instance (ekey=0 because it needs one.)
        ex_instance = self.exerciseinstance(row=row, ekey=0)

        #exercise instance will sent instances to siacua
        ex_instance.siacua(ekeys,sendpost,course,usernamesiacua,grid2x2,siacuatest)

        #done

    
    def siacuapreview(self,unique_name=None,ekeys=[]):
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
            unique_name = self._unique_name

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
        
        
