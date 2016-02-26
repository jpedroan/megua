# coding=utf-8

r"""
Group together random generators for Sage, Python, Numpy and R (RPy2 module). 

AUTHORS:

- Pedro Cruz (2011-05-06): initial version.
- Pedro Cruz (2011-08-23): documentation test strings.
- Pedro Cruz (2016-01): review doc tests.


EXAMPLES:

Test examples using::
    
    sage -t ut.py

Using Sage random numbers::

    sage: from megua.ur import ur
    sage: ur.start_at(10)
    10
    sage: print ZZ.random_element(-10,11) 
    -4
    sage: print ZZ.random_element(-10,11) 
    1
    sage: ur.start_at(10) #test if start_at guarantees the same sequence
    10
    sage: print ZZ.random_element(-10,11)
    -4
    sage: print ZZ.random_element(-10,11)
    1

Using python random numbers::

    sage: from megua.ur import *
    sage: #python module 'random' is imported above.
    sage: ur.start_at(10) 
    10
    sage: print random.randint(-10,10)
    1
    sage: print random.randint(-10,10)
    -1
    sage: ur.start_at(10) #after import random
    10
    sage: print random.randint(-10,10)
    1
    sage: print random.randint(-10,10)
    -1


Using numpy random numbers::

    sage: from megua.ur import ur
    sage: #python module 'numpy.random' as 'nprandom' is imported above.
    sage: ur.start_at(10)
    10
    sage: print nprandom.randint(-10,10)
    -1
    sage: print nprandom.randint(-10,10)
    -6
    sage: ur.start_at(10)
    10
    sage: print nprandom.randint(-10,10)
    -1
    sage: print nprandom.randint(-10,10)
    -6



Using RPy2 random numbers::

    sage: from megua.ur import ur
    sage: ur.start_at(10)
    10
    sage: ur.rpy2_rnorm(0,1)
    0.018746170941826425
    sage: ur.rpy2_rnorm(0,1)
    -0.18425254206906366
    sage: ur.start_at(10)
    10
    sage: ur.rpy2_rnorm(0,1)
    0.018746170941826425
    sage: ur.rpy2_rnorm(0,1)
    -0.18425254206906366


Using ur (this module) random functions::

    Integers::

    sage: from megua.ur import ur
    sage: ur.start_at(10)
    10
    sage: ur.iunif(-10,10)
    -4
    sage: ur.iunif(-10,10)
    1
    sage: ur.start_at(10)
    10
    sage: ur.iunif(-10,10)
    -4
    sage: ur.iunif(-10,10)
    1

    Random set::

    sage: from megua.ur import ur
    sage: ur.start_at(10)
    10
    sage: ur.random_element() 
    sqrt(2)
    sage: ur.random_element([1,2,3,4,5,6]) 
    4


IMPLEMENTATION NOTES:

* Test with ``sage -t ur.py`` or ``sage -t -verbose ur.py``.
* All tests passed with Sage 4.7.
* See ``sage.misc.randstate`` (all details about Sage random number generator).

LINKS and FILES:

1. Sage module prandom: sage/local/lib/python2.6/site-packages/sage/misc/prandom.py
2. Numpy random numbers: http://docs.scipy.org/doc/numpy/reference/routines.random.html
3. RPy2: http://rpy.sourceforge.net/rpy2/doc-2.0/html/robjects.html#r-objects


**NEXT FUNCTIONS SHOULD NOT APPEAR IN THIS PAGE. PLEASE GO DOWN FOR THIS MODULE DOCUMENTATION.**

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  

#================
# PYTHON modules
#================

#Random numbers from numpy
#http://docs.scipy.org/doc/numpy/reference/routines.random.html
import numpy.random as nprandom


#Random numbers from R using RPy2
# 1. Always do casts to python rpy2 commands.
# 2. To do: study how does rpy2 works.
import rpy2.robjects as robjects

#to restart random
import time 


#====================
# SAGEMATH modules
#====================
#Random numbers from Sage
from sage.all import *



#Random numbers with python
#TODO: sagemath prandom.py redefined random and here 
#      we define it again as python module.
import random 





"""Rounding numbers

Solution 1
#import __builtin__; 
#def fround(x,digits=0):
#    #return __builtin__.round(x._sage_(),digits)
#    return round(x._sage_(),digits)

Solution 2
To do: Use RealField from Sage.

"""

class UnifiedRandom(SageObject):

    """Check every function in the module for how to use details.
    """

    #See squnif for details about this list. 
    _qlist = [Integer(1)/Integer(9), Integer(1)/Integer(8), Integer(1)/Integer(7),\
Integer(1)/Integer(6), Integer(1)/Integer(5), Integer(2)/Integer(9),\
Integer(1)/Integer(4), Integer(2)/Integer(7), Integer(1)/Integer(3),\
Integer(3)/Integer(8), Integer(2)/Integer(5), Integer(3)/Integer(7),\
Integer(4)/Integer(9), Integer(1)/Integer(2), Integer(5)/Integer(9),\
Integer(4)/Integer(7), Integer(3)/Integer(5), Integer(5)/Integer(8),\
Integer(2)/Integer(3), Integer(5)/Integer(7), Integer(3)/Integer(4),\
Integer(7)/Integer(9), Integer(4)/Integer(5), Integer(5)/Integer(6),\
Integer(6)/Integer(7), Integer(7)/Integer(8), Integer(8)/Integer(9)]

    _qlen = len(_qlist)


    def _init_(self,seed_value=None):
        self.seed(seed_value)

    def __repr__(self):
        return "UnifiedRandom(%d)" % self.seed_value


    def start_at(self,seed_value=None):
        """ Set or get seeds from all random number libraries to the "same" value.

        INPUT:

        - ``seed_value`` -- an Integer or None

        OUTPUT:

        - return self.seed_number 

        Seed commands:

        1. for sage: set_random_seed, seed.
        2. for R: set.seed
        3. for python: TODO ????

        TODO: 

        1. check what happens with simultaneous notebooks 
        and worksheets and also in a shared "sage" instance.

        2. Change random_seed set.

        """

        #Keep in memory, use int to convert from sage to python int
        if seed_value==None:
            self.seed_value = int(time.time()) #NOTE: change this.
        else:
            self.seed_value = int(seed_value)

        #set SAGE seed
        set_random_seed(self.seed_value)
        
        #set PYTHON RANDOM module seed
        random.seed(self.seed_value)
        
        #set R from rpy2
        self._rpy2_setseed(self.seed_value) 
        
        #Set PYTHON NUMPY MODULE seed
        nprandom.seed(int(self.seed_value))

        return self.seed_value

    def random_element(self,somelist=[exp(1),pi,sqrt(2)]):
        """
        Returns an element from the ``somelist`` parameter.

        INPUT:

        - ``somelist`` -- a list, for example ``[exp(1),pi,sqrt(2)]``.

        OUTPUT:

        A random element from the input list.
        """

        l = len(somelist)
        i = ZZ.random_element(l)
        return somelist[i]


    def iunif(self,a,b):
        """
        Integer random number from a uniform distribution (iunif).
        Seed is from Sage random module.

        INPUT:

        - ``a`` -- minimum integer

        - ``b`` -- maximum integer

        OUTPUT:

            Integer

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.start_at(10)
            10
            sage: ur.iunif(-10,10)
            -4
            sage: ur.iunif(-10,10)
            1

        Notes: iunif function returns ZZ.random_element(a,b+1)
        """

        return ZZ.random_element(a,b+1) #An integer in [a,b]
 

    def iunif_nonset(self,a,b,nonset):
        """
        Integer random number from a uniform distribution excluding numbers on "nonset".
        Seed is from Sage random module.

        INPUT:

        - ``a`` -- minimum integer

        - ``b`` -- maximum integer

        OUTPUT:

            Integer

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.start_at(10)
            10
            sage: ur.iunif_nonset(-10,10,[-1,0,1]) #exclude [-1,0,1]
            -4
            sage: ur.iunif_nonset(-10,10,[-1,0,1]) #exclude [-1,0,1]
            4

        To do: improve this algorithm.
        """
        nonset = set(nonset) #remove duplicates
        n = b-a+1 #number of integers from a to b
        m = len(nonset) #number of excluded cases
        rd_yes = ZZ.random_element(n-m) #Get a random number from 0 to (n-m-1)
        #Choose the rd 'y'
        #  -3 -2 -1 0 1 2 3 (i iterator)
        #   y  n y  y n y y (yes iterator)
        i=a-1
        yes=-1
        while yes<rd_yes:
            i += 1        
            if i not in nonset:
                yes += 1
        return i

    def different_integers(self,num=1,a=0,b=10):
        """
        Generate ``num`` different integers between ``a`` and ``b`` from a uniform distribution.

        NOTE:

        Seed is from Sage random module.

        INPUT:

        - ``num`` -- number of integers to generate
        - ``a`` -- minimum integer
        - ``b`` -- maximum integer

        OUTPUT:

        - Integer list.


        ALGORITHM:

        Ideas for future algorithms:
        * http://stackoverflow.com/questions/3722430 by Sheldon L. Cooper.
        * http://eyalsch.wordpress.com/2010/04/01/random-sample/ (Eyal Schneider)

        And also, from python:
        * http://docs.python.org/2/library/bisect.html
        * http://www.sagemath.org/doc/reference/structure/sage/sets/set.html

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.start_at(10)
            10
            sage: ur.different_integers(5,-10,10)
            [1, -1, -4, -3, -10]
            sage: ur.different_integers(5,-10,10)
            [1, -5, -4, -10, 7]

        """

        if (b-a+1) < num:
            print "Cannot choose %d different elements from [%d,%d]" % (num,a,b)
            assert(0)

        attempts = 0
        chosen = set()
        for i in range(num):
            found = False
            while not found and attempts<1000:
                r = ZZ.random_element(a, (b+1))
                found = not r in chosen
                attempts += 1
            if found:
                chosen.add(r)
            else:
                #tiemout!
                return [i for i in xrange(a,a+num)]

        return list(chosen)




    def runif(self,a,b,prec=None):
        """
        Real random number from a uniform distribution.
        Seed is from Sage random module.

        INPUT:

        - ``a`` -- minimum integer

        - ``b`` -- maximum integer

        - ``prec`` -- number of decimal digits (default all).

        OUTPUT: 

        An ``RealDoubleField`` (or ``RDF``) number.

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.start_at(10)
            10
            sage: ur.runif(-10,10,2)
            7.44
            sage: ur.runif(-10,10) 
            -0.639847508477489

        NOTE:
            Previous result from the above tests where: 
            -8.74 and -7.17316398804125. But from which version of sage?

        """
        res = RR.random_element(a,b)
        if prec:
            res = round(res,prec)
        return res


    def rnorm(self,mean,stdev,prec=None):
        """
        Real random number from a normal distribution.
        Seed is from Sage random module.

        INPUT:

        - ``mean`` -- mean value of the Normal distribution.

        - ``stdev`` -- standard deviation of the Normal distribution.

        - ``prec`` -- number of decimal digits (default all).

        OUTPUT:

        An ``RealDoubleField`` (or ``RDF``) number.

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.start_at(10)
            10
            sage: ur.rnorm(0,1,2) 
            1.33
            sage: ur.rnorm(0,1) 
            -0.11351682931886863

        Another possible implemention::

            #rpy version 
            rnum = rnorm(1,RDF(mean),RDF(sigma))._sage_()
            #rpy2 version
            rnum = rpy2_rnorm(1,float(mean),float(sigma))[0]

        """
        #sage version
        rnum = normalvariate(mean,stdev) #rnum is a float
        if prec:
            rnum = round(rnum, prec)
        return rnum


    def rbernoulli(self):
        """
        Generate 0 or 1 randonly.
        Seed is from Sage random module.

        INPUT: no need.

        OUTPUT:

            0 or 1.

        EXAMPLES::

            sage: from megua.ur import ur
            sage: ur.start_at(10)
            10
            sage: ur.rbernoulli() 
            1
            sage: ur.rbernoulli() 
            1

        """
        return int(getrandbits(1))
    

    def squnif(self):
        """
        Random select pure rationals (no integers) that are suitable for easy hand calculations over a predefined list:

        1. `squnif`` means 'selected from Q using uniform distribution'.
        2. Extracts negative or positive rationals in the form `a/b` where::

            b in 1,2,3,4,5,6,7,8,9
            a in 1,2,...,b

        3. No integer numbers.
        4. No duplicates (`2/4` is not produced, only `1/2`).
        5. See implementation notes below for more details.

        Seed is from Sage random module.

        INPUT: nothing

        OUTPUT:

        A rational number from -8/9 to 8/9 usign single digits on numerator and denominator (integeres excluded).

        EXAMPLES::
 
            sage: from megua.ur import ur
            sage: ur.start_at(10)
            10
            sage: ur.squnif() 
            -1/4
            sage: ur.squnif() 
            -4/9
 
        IMPLEMENTATION NOTES:

        1. Check class variable UnifiedRandom._qlist.
        2. This module is a pure python module so 1/3 results in 0. One must use
 Integer(1)/Integer(3)::
        3. Testing::
            sage: from sage.all import *
            sage: qq = [ Integer(a+1)/Integer(b+1) for b in range(9) for a in range(b)]
            sage: ql = list(set(qq))
            sage: ql.sort()
            sage: print ql
            [1/9, 1/8, 1/7, 1/6, 1/5, 2/9, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 4/9, 1/2, 5/9, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 7/9, 4/5, 5/6, 6/7, 7/8, 8/9]
            sage: len(ql)
            27
            sage: from megua.ur import ur
            sage: print ur._qlist
            [1/9, 1/8, 1/7, 1/6, 1/5, 2/9, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 4/9, 1/2, 5/9, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 7/9, 4/5, 5/6, 6/7, 7/8, 8/9]
            sage: print ur._qlen
            27

        """
        qr = ZZ.random_element(UnifiedRandom._qlen)
        if self.rbernoulli() == 0:
            return - UnifiedRandom._qlist[qr]
        else:
            return + UnifiedRandom._qlist[qr]


    """
    RPy2 wrappers
     
    Postpone::

        def rpy2_multinomial(self,....)
        rpy2_multinomial = robjects.r['rmultinom']

        def rpy2_runif(self,...)
        rpy2_runif = robjects.r["runif"]

    """ 

    def _rpy2_setseed(self,seed):
        """
        Set seed for RPy2 module.
        See start_at on this module.
        """
        setseed = robjects.r['set.seed']
        setseed(int(seed))


    def rpy2_rnorm(self,mean,stdev,prec=None):
        """
        Random number from Normal distribution. 

        NOTES:

        - Based on RPy2 module (seed is from RPy2).

        INPUT:

        - ``mean`` -- mean value of the Normal distribution.

        - ``stdev`` -- standard deviation of the Normal distribution.

        - ``prec`` -- number of decimal digits (default all).

        OUTPUT:

            A random number from Normal distribution with given parameters.

        EXAMPLES::
 
            sage: from megua.ur import ur
            sage: ur.start_at(10)
            10
            sage: ur.rpy2_rnorm(0,1,2) #two decimals 
            0.02
            sage: ur.rpy2_rnorm(0,1) 
            -0.18425254206906366
 
        """
        rnorm = robjects.r['rnorm']
        res = rnorm(1,float(mean),float(stdev))[0]
        if prec:
            res = round(res,prec)
        return res
    



#==========
# Instance
#==========
"""
The global instance ``ur=UnifiedRandom()``::

   sage: from megua.ur import ur
   sage: ur 
   UnifiedRandom(10)
"""
ur = UnifiedRandom()



