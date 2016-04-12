# coding=utf-8

r"""
Generic Mathematical routines for MEGUA.

AUTHORS:

- Pedro Cruz (2010-06): initial version
- Pedro Cruz (2013-11): added logb (and this module is now imported in ex.py)
- Pedro Cruz (2016-01): changed for new formal functions sagemath standard.

"""


#*****************************************************************************
#       Copyright (C) 2011 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


r"""
Must import everything from sage.all::

    from sage.all import *

Avoiding this is impossible. For example::

      from sage.rings.real_double import RDF

does not work.



.. test with: sage -t mathcommon.py


"""

#PYTHON modules
from string import join
import jinja2
import os

#SAGEMATH modules
#from sage.all import var,RealField,SR,function,e
from sage.all import *

#MEGUA modules
from megua.ur import ur
from tounicode import to_unicode



"""
the following code is about templating.

TODO: incorporate other templating code into one module.

"""

#Templating (with Jinja2)
natlang = 'pt_pt'
if os.environ.has_key('MEGUA_TEMPLATE_PATH'):
    TEMPLATE_PATH = os.environ['MEGUA_TEMPLATE_PATH']
else:
    from pkg_resources import resource_filename
    TEMPLATE_PATH = os.path.join(resource_filename(__name__,''),'template',natlang)

#print "Templates in mathcommon.py:  '%s' language at %s" % (natlang,TEMPLATE_PATH)
env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH))



#Sometimes needed.
x,y=var('x,y')


#For 4 digit numbers.
R15=RealField(15)

#For more digit numbers
R20 = RealField(20)

##############
#TikZmod -- Routines to convert sage plots into latex TikZ markup.
##############



def getpoints_str(pointlist):
    return join( [ str( ( R20(p[0]), R20(p[1]) ) ) for p in pointlist ], ' ' )


def tikz_axis(vmin,vmax,axis='x', points=None, ticksize=2, originlabels=True):
    r"""
    Draw the vertical or horizontal 2d axis.

    INPUT:

    - ``vmin``: first point of the axis.

    - ``vmax``: last point of the axis (where the arrow ends).

    - ``axis``: 'x' or 'y'.

    - ``points``: if None, points are guessed. Otherwise they are used to place marks.

    - ``originlabels'': (dafault True) If false (0,0) won't have labels.


    Specials thanks to Paula Oliveira for the first version.

    Other resource: http://matplotlib.org/users/pgf.html#pgf-tutorial

    """
    
    if points is None:
        #integer tick marks only (for now)
        first_int = floor(vmin)
        last_int  = ceil(vmax)
        #last_int - first_int + 1 gives all integers,
        #but the last point is the arrow vertice: no label and no tick mark so "+1" is not added.
        points = [ i+first_int for i in range(last_int - first_int) ] 
        if not originlabels and 0 in points:
            pos = points.index(0)
            del points[pos]
    else:
        first_int = min(points)
        last_int  = max(points) + 1 #added +1 for the reason above.

    if axis=='x':
        #integer tick marks
        tmarks = r'\foreach \x in %s' % Set(points)
        tmarks += r'\draw[color=black] (\x,-%d pt) node[below] {\scriptsize $\x$} -- (\x,%d pt) ;' % (ticksize,ticksize)
        #main line and arrow at end
        tmain = r'\draw[->,color=black] (%f,0) -- (%f,0);' % (first_int,last_int)
    else:
        #integer tick marks
        tmarks = r'\foreach \y in %s' % Set(points)
        tmarks += r'\draw[color=black] (-%d pt,\y) node[left] {\scriptsize $\y$} -- (%d pt,\y);' % (ticksize,ticksize)
        #main line and arrow at end
        tmain = r'\draw[->,color=black] (0,%f) -- (0,%f);' % (first_int,last_int)

    return tmain + tmarks
    

# =====================
# Google charts
# =====================


def svg_pie_chart(valueslist, chartid="chart1", title="Chart", width=400, height=300):
    """
    Plot an SVG chart pie.

    Note: uses google charts.

    INPUT:

    - ``valueslist`` -- list of pairs
    - ``chartname`` -- like a username 'Pizza Pie'
    - ``title`` -- like ''How Much Pizza I Ate Last Night'
    - ``width`` -- default 400
    - ``height`` -- default 300

    OUTPUT:
        A HTML string with code (google chart html code) to plot a chart.
    """

    filename="svg_pie_chart.html"
    try:
        tmpl = env.get_template(filename)
    except jinja2.exceptions.TemplateNotFound:
        return "MegUA -- missing template %s"%filename
    r = tmpl.render(valueslist=valueslist,
                    chartid=chartid,
                    title=title,
                    width=width,
                    height=height)

    print "TYPE=",type(r)

    return r




def svg_pie_chart(valueslist, chartid="chart1", title="Chart", width=400, height=300):
    """
    Plot an SVG chart pie.

    Note: uses google charts.

    INPUT:

    - ``valueslist`` -- list of pairs
    - ``chartname`` -- like a username 'Pizza Pie'
    - ``title`` -- like ''How Much Pizza I Ate Last Night'
    - ``width`` -- default 400
    - ``height`` -- default 300

    OUTPUT:
        A HTML string with code (google chart html code) to plot a chart.
    """

    filename="svg_pie_chart.html"
    try:
        tmpl = env.get_template(filename)
    except jinja2.exceptions.TemplateNotFound:
        return "MegUA -- missing template %s"%filename
    r = tmpl.render(valueslist=valueslist,
                    chartid=chartid,
                    title=title,
                    width=width,
                    height=height)

    return r




#=======================
# log for "high school"
#=======================

def FORMALLOG_latex(fun,x,base=None):
    if base==e or base is None:
        return r'\ln\left(%s\right)' % latex(x)
    elif base==10:
        return r'\log\left(%s\right)' % latex(x)
    else:
        return r'\log_{%s}\left(%s\right)' % (latex(base),latex(x))

x,b=SR.var('x,b')
FORMALLOG = function('logb',nargs=2, print_latex_func=FORMALLOG_latex)
#Two arguments: x and base.


def logb(x,base=e,factorize=False):
    r"""
    This is a procedure that decides to compute or to print a logarithm in any base.
    
    (logb is an alternative to ``log`` from Sage.)
    
    After calling `logb()` several objects could be returned including the `FORMALLOG` formal log function.

    This version keeps the base because ``log(105,base=10)`` is transformed by Sage (and many others CAS) 
    into ``log(105)/log(10)`` and sometimes this is not what we want to see as a result. 

    LaTeX representations are:

    * ``\log_{base} (x)`` if base is not ``e``.
    * ``\log (x)`` if the base is exponential.

    INPUT:

    - ``x`` - the argument of log.

    - ``base`` - the base of logarithm.

    - ``factorize`` - decompose in a simple expression if argument if decomposable in prime factors.

    OUTPUT:

    - an expression based on ``logb``, Sage ``log`` or any other expression.

    Basic cases::

        sage: logb(e) #assume base=e
        1
        sage: logb(10,base=10)
        1
        sage: logb(1) #assume base=e
        0
        sage: logb(1,base=10) #assume base=e
        0
        sage: logb(e,base=10)
        logb(e, 10)
        sage: logb(10,base=e)
        logb(10, e)
        sage: logb(sqrt(105))
        logb(sqrt(105), e) 
        sage: logb(5,base=e)
        logb(5, e)
        sage: logb(e^2,base=e)
        2
        sage: logb(0,base=10)
        -Infinity

    With and without factorization::

        sage: logb(3^5,base=10)  #no factorization
        logb(243, 10)
        sage: logb(3^5,base=10,factorize=True)  
        5*logb(3, 10)
        sage: logb(3^5*2^3,base=10) #no factorization
        logb(1944, 10)
        sage: logb(3^5*2^3,base=10,factorize=True)  
        5*logb(3, 10) + 3*logb(2, 10)

    Latex printing of logb::

        sage: latex( logb(e) )
        1
        sage: latex( logb(1,base=10) )
        0
        sage: latex( logb(e,base=10) )
        \log\left(e\right)
        sage: latex( logb(sqrt(105)) )
        \ln\left(\sqrt{105}\right)
        sage: latex( logb(3^5,base=10) )
        \log\left(243\right)
        sage: latex( logb(3^5,base=10,factorize=True)  )
        5 \, \log\left(3\right)
        sage: latex( logb(3^5*2^3,base=10,factorize=True) )
        5 \, \log\left(3\right) + 3 \, \log\left(2\right)
        sage: latex( logb(3^5*2^3,base=3,factorize=True) )
        5 \, \log_{3}\left(3\right) + 3 \, \log_{3}\left(2\right)

    """
    #e is exp(1) in sage
    r = log(x,base=base)
    if r in ZZ or r in QQ or r==-Infinity: #Note: r in RR results in true if r=log(2/3,e)    #OLD: SR(r).denominator()==1:
        return r
    else:
        if factorize:
            F = factor(x)
        if factorize and type(F) == sage.structure.factorization_integer.IntegerFactorization:
            l = [ factor_exponent * FORMALLOG(factor_base,base) for (factor_base,factor_exponent) in F ]
            return add(l) 
        else:
            return FORMALLOG(x,base)


#=======================
# pow for "high school"
#=======================

def _POW_latex(fun,basev,expv):
    if basev==0 and expv!=0:
        return r'0'
    elif basev==1:
        return r'1'
    else:
        return r'%s^{%s}' % (latex(basev),latex(expv))    

bv,ev=SR.var('bv,ev')
#FORMALPOW = function('powb', bv, ev, print_latex_func=_POW_latex)
FORMALPOW = function('powb', nargs=2, print_latex_func=_POW_latex)

def powb(basev,expv):
    r"""powb is an alternative to ``^`` from Sage that preserves ^ in latex.

    See similar idea for logb.

    INPUT:

    - ``basev`` - the basis argument.

    - ``expv`` - the exponent value.

    OUTPUT:

    - an expression based on ``powb`` that is converted by latex() to a^b without calculating.

    Basic cases::

        sage: powb(0,1)
        0
        sage: powb(1,2)
        1
        sage: powb(2,3)
        powb(2, 3)
        sage: latex( powb(2,3) )
        2^{3}

    """
    if basev==0 and expv!=0:
        return 0
    elif basev==1:
        return 1
    else:
        return FORMALPOW(basev,expv)


#=======================
# factorial for "high school"
#=======================

def _FACT_latex(fun,x):
    #fun is the new function name
    return r'%s!' % latex(x)


# x=SR.var('x')  see above.
#inerte: does not calulate factorial, only put "!".
#FACT_ = function('factb', x, print_latex_func=_FACT_latex)
FORMALFACT = function('factb', nargs=1, print_latex_func=_FACT_latex)


def factb(xv):
    r"""factb is an alternative to ``factorial`` from Sage in the sense of representation: factb(x) is never calculated.

    This version correct latex(120/factorial(5), hold=true) bug.

    INPUT:

    - ``xv`` - the argument of log.

    OUTPUT:

    - x! without calculating

    Basic cases::

        sage: factb(0)
        factb(0)
        sage: factb(1)
        factb(1)
        sage: factb(2)
        factb(2)
        sage: factb(5)
        factb(5)
        sage: latex( factb(5) )
        5!
        sage: latex( 120/ factb(5) )
        \frac{120}{5!}

    """
    return FORMALFACT(xv)





#===================================
# Old functions 
#  (that are in use in old problems)
#===================================


def showmul(x):
    """Deprecated:
    Old way of writing parentesis on negative numbers.
    """
    if x<0:
        return '(' + latex(x) + ')'
    else:
        return x


# ==================
# MSC 15 -- Algebra
# ==================


def before_minor(M,pivot_row,pivot_col):
    """
    A minor is the determinant of a submatrix of M.
    This routine gives the matrix to which the determinant is calculated.
    
    INPUT:
        
    - ``M``: a square matrix n by n.

    - ``pivot_row, pivot_col``: row and column nunbers (0 to n-1).
    
    OUTPUT:
        
        The submatrix of ``M`` extracting row ``pivot_row`` and column ``pivot_col``.

    EXAMPLES::

       sage: from megua.mathcommon import before_minor 
       sage: M = matrix(ZZ, [ [  1, -25,  -1,   0], [  0,  -2,  -5,  -2], [  2,   1,  -1,   0], [  3,   1,  -2, -13] ]); M
       [  1 -25  -1   0]
       [  0  -2  -5  -2]
       [  2   1  -1   0]
       [  3   1  -2 -13]
       sage: before_minor(M,0,0)
       [ -2  -5  -2]
       [  1  -1   0]
       [  1  -2 -13]
       sage: before_minor(M,0,3)
       [ 0 -2 -5]
       [ 2  1 -1]
       [ 3  1 -2]
       sage: before_minor(M,3,3)
       [  1 -25  -1]
       [  0  -2  -5]
       [  2   1  -1]
       sage: before_minor(M,3,0)
       [-25  -1   0]
       [ -2  -5  -2]
       [  1  -1   0]
       sage: before_minor(M,0,2)
       [  0  -2  -2]
       [  2   1   0]
       [  3   1 -13]
       sage: before_minor(M,3,2)
       [  1 -25   0]
       [  0  -2  -2]
       [  2   1   0]
       sage: before_minor(M,2,0)
       [-25  -1   0]
       [ -2  -5  -2]
       [  1  -2 -13]
       sage: before_minor(M,2,3)
       [  1 -25  -1]
       [  0  -2  -5]
       [  3   1  -2]
       sage: before_minor(M,1,1)
       [  1  -1   0]
       [  2  -1   0]
       [  3  -2 -13]


    AUTHORS:
    - Pedro Cruz (2012/April)
    - Paula Oliveira (2012/April)
    
    """
    
    nrows,ncols = M.parent().dims()
    
    #put values in 0-n-1 range.
    nrows -= 1
    ncols -= 1
    
    if pivot_row==0 and pivot_col==0:
        #pivot is at left top corner
        return M[1:,1:]

    elif pivot_row==0 and pivot_col==ncols:
        #pivot is at right top corner
        return M[1:,:-1]

    elif pivot_row==nrows and pivot_col==ncols: 
        #pivot is at right bottom corner
        return M[:-1,:-1]

    elif pivot_row==nrows and pivot_col==0:     
        #pivot is at left bottom corner
        return M[:-1,1:]

    elif pivot_row==0: 
        #pivot is at first row any other col
        M.subdivide( 1, [pivot_col,pivot_col+1])
        return block_matrix( [ [M.subdivision(1,0),M.subdivision(1,2)]], subdivide=False)

    elif pivot_row==nrows: 
        #pivot is at last row any other col
        M.subdivide( nrows, [pivot_col,pivot_col+1])
        return block_matrix( [ [M.subdivision(0,0),M.subdivision(0,2)]], subdivide=False)

    elif pivot_col==0:
        #pivot is at column 0 and any other row
        M.subdivide( [pivot_row,pivot_row+1], 1)
        return block_matrix( [ [M.subdivision(0,1)],[M.subdivision(2,1)]], subdivide=False)

    elif pivot_col==ncols: 
        #pivot is at last column and any other row
        M.subdivide( [pivot_row,pivot_row+1], ncols)
        return block_matrix( [ [M.subdivision(0,0)],[M.subdivision(2,0)]], subdivide=False)

    else:
        M.subdivide( [pivot_row,pivot_row+1], [pivot_col,pivot_col+1])
        return block_matrix( [ [M.subdivision(0,0),M.subdivision(0,2)], [M.subdivision(2,0),M.subdivision(2,2)] ], subdivide=False)




# ==================
# MSC 26 -- 
# ==================


# ==================
# MSC 60 -- probability
# ==================


def random_alpha():
    """
    Returns a random alpha value (significance level). 
    (Used in statistics).

    EXAMPLES::

    sage: from megua.mathcommon import random_alpha
    sage: random_alpha()
    (5.00000000000000, 0.0500000000000000)

    """
    #Significance Level
    d = ur.iunif(0,3)
    if d==0:
        return (RealNumber('0.1'),RealNumber('0.001'))
    elif d==2:
        return (RealNumber('1'),RealNumber('0.01'))
    elif d==3:
        return (RealNumber('5'),RealNumber('0.05'))
    else:
        return (RealNumber('10'),RealNumber('0.1'))


def Percent(value):
    """
    Given an alpha or 1-alpha value return the textual version without %.

    EXAMPLES::

    sage: from megua.mathcommon import Percent
    sage: Percent(0.1) + "%"
    '10%'
    sage: Percent(0.12) + "%"
    '12%'
    """
    value = float(value)
    if value == 0.01:
        return r"1"
    elif value == 0.05:
        return r"5"
    elif value == 0.10:
        return r"10"
    elif value == 0.90:
        return r"90"
    elif value == 0.95:
        return r"95"
    elif value == 0.975:
        return r"97.5"
    elif value == 0.99:
        return r"99"
    elif value == 0.995:
        return r"99.5"
    else:
        return r"{0:g}".format(value*100)




#def random_pmf(n=6):
#    #restart random number generator
#    # See class Exercise for seed.activate()
#    #Support (random)
#    x0 = ur.iunif(-2,3) #start x_0
#    h = ur.runif(0,2,1) #h space between
#    #n = iunif(4,6) # fixed for start
#    values = [x0 + h * i for i in range(n)]
#    #Probabilities (random)
#    lst = [runif(0,1,1) for i in range(n)]
#    sumlst = sum(lst)#weighted sum
#    probabilities = [fround(i/sumlst,2) for i in lst]
#    #Correction
#    newsum = sum(probabilities)
#    probabilities[0] =  probabilities[0] + (1-newsum)
#    return {'values': values,'probabilities': probabilities}




# ==================
# MSC 62 -- statistics
# ==================


#Random numbers from R using RPy2
# 1. Always do casts to python rpy2 commands.
# 2. To do: study how does rpy2 works.

import rpy2
import rpy2.robjects as robjects


def qt(p,df,prec=None):
    """
    Quantil from a t-student distribution.

    NOTES:

    * Based on RPy2 module (seed is from RPy2).

    INPUT:

    - ``p`` -- probability.
    - ``df`` -- degree of freedom (distribution parameter).
    - ``prec`` -- number of decimal digits (default all).

    OUTPUT:
        Quantil from t-student distribution.

    EXAMPLES::

        sage: from megua.mathcommon import qt
        sage: qt(0.95,12)
        1.7822875556493196
        sage: qt(0.95,12,2)
        1.78

    """
    #qt(p, df, ncp, lower.tail = TRUE, log.p = FALSE)
    qt = robjects.r['qt']
    res = qt(float(p),int(df))[0]
    if prec:
        res = round(res,prec)
    return res

def pnorm(x,mean,stdev,prec=None):
    """
    Probability of a normal distribution(mean, stdev).

    NOTES:

    * Based on RPy2 module (seed is from RPy2).

    INPUT:

    - ``x`` -- some quantil.
    - ``mean`` -- mean of the normal distribution.
    - ``stdev`` -- standar deviation.
    - ``prec`` -- number of decimal digits (default all).

    OUTPUT:
        :math:``P(X<=x) where X~Norm(mean,stdev).

    EXAMPLES::

        sage: from megua.mathcommon import pnorm
        sage: pnorm(0,0,1)
        0.5
        sage: pnorm(1.644854,0.0,1.0)
        0.9500000384745869

    """
    #qt(p, df, ncp, lower.tail = TRUE, log.p = FALSE)
    pnorm = robjects.r['pnorm']
    res = pnorm(float(x),float(mean),float(stdev))[0]
    if prec:
        res = round(res,prec)
    return res



#from sage.rings.integer import Integer

def r_stem(p_list,html=True):
    """
    Return a string with a stem-and-leaf diagram based on R.

    INPUT:

    - `p_list': a python list
    
    OUTPUT:

       Return string with the diagram.

    EXAMPLES:

       TODOsage: from megua.mathcommon import r_stem
       TODOsage: r_stem( [random() for _ in range(20)] ) #random
       u'\n  O ponto decimal est\xe1 1 d\xedgitos para a esquerda de |\n\n  0 | 283\n  2 | 334\n  4 | 468117\n  6 | 3348169\n  8 | 5\n\n'
       TODOsage: r_stem( [int(100*random()) for _ in range(20)] ) 
       u'\n  O ponto decimal est\xe1 1 d\xedgito para a direita de |\n\n  0 | 60\n  2 | 1660\n  4 | 169\n  6 | 03457\n  8 | 091779\n\n'

    #TODO : put this examples to work !
    from random import random
    l = [int(100*random()) for _ in range(20)]
    print l
    b = r_stem2( l ) 
    #b = r_stem( [random() for _ in range(30)] )
    print b
       
       This module defines functions that use R software for statistics.

    AUTHORS:

    - Pedro Cruz (2014-03-07): initial version

    LINKS:

     - http://www.sagemath.org/doc/reference/interfaces/sage/interfaces/r.html


    CODE STARTS HERE:
    =============================    
    TODO: rebuild  this function.
    =============================    
    
    stemf = robjects.r['stem']

    buf = []
    def f(x):
        # function that append its argument to the list 'buf'
        buf.append(x)

    # output from the R console will now be appended to the list 'buf'
    rpy2.rinterface.setWriteConsole(f)


    if type(p_list[0])==int: # or type(p_list[0])==sage.rings.integer.Integer:
        stemf( robjects.IntVector(p_list) )
    else:
        stemf( robjects.FloatVector(p_list) )



    #Parsing: The decimal point is 1 digit(s) to the right of the |
    #The answer is a list of string in the "buf" variable.

    #Keep record
    buf1 = buf[1]
    buf2 = buf[2]


    #if buf[1] == '  The decimal point is ':
    buf[1] = u"  O ponto decimal está "
    
    #get space position after the number.
    sp = buf[2].index(' ')

    
    if 'left' in buf[2]:
        sideword = 'esquerda'
        sideflag = True
    elif 'right' in buf[2]:
        sideword = 'direita'
        sideflag = True
    else:
        sideword = 'em |\n'
        sideflag = False

    
    if sideflag:
        if buf[2][:sp]=='1':
            buf[2] = buf[2][:sp] + u" dígito para a %s de |\n\n" % sideword
        else:
            buf[2] = buf[2][:sp] + u" dígitos para a %s de |\n\n" % sideword
    else:
        buf[2] = sideword

    #For debug only
    buf.insert(3,buf1)
    buf.insert(4,buf2)

    jbuf = u''.join(buf)

    #print jbuf
    #print type(jbuf)

    if html:
        jbuf = u'''<div style="font-family: 'Courier New', monospace;"><pre>''' + jbuf + u"</pre></div>"

    return jbuf
    """
    
    return 'stem: todo things. call the programmer.'



# ==================
# MSC 65 -- numerical analysis
# ==================



"""
About polynomials

https://groups.google.com/group/sage-support/msg/4abc7d2c5ea97c2b?hl=pt
http://ask.sagemath.org/question/202/identification-polynomial

http://www.sagemath.org/doc/reference/sage/rings/polynomial/polynomial_ring_constructor.html
http://www.sagemath.org/doc/reference/sage/rings/polynomial/multi_polynomial_ring_generic.html
 P.<x,y,z> = PolynomialRing(QQ)
 P.random_element(2, 5)
-6/5*x^2 + 2/3*z^2 - 1
 P.random_element(2, 5, choose_degree=True)
-1/4*x*y - 1/5*x*z - 1/14*y*z - z^2

"""



def support_set(fun,a,b,n,rdecimals):
    """ 
    INPUT:
     - ``fun``: some expression or function.
     - ``a``: lower interval limit.
     - ``b``: upper interval limit.
     - ``n``: number of intervals.
    OUTPUT:
     -
    """
    h = (b-a)/n
    xset = [a + i * h for i in range(n+1)] #n+1points
    xyset = [ (xv,fun.subs(x=xv)) for xv in xset]
    return xyset


def random_basicLU3():
    """
    Generate random matrix A (3x3) and decomposition LU where A=LU without permutation.

    TODO: create a random dominant diagonal matrix module. MatrixSpace(QQ,3,3).
    Used on exercise: E65F05_LU_001. Any change could afect it.
    """

    A = random_matrix(ZZ,3,x=-3,y=3)
    #d = A.diagonal()
    A[0,0] = max( abs(A[0,0]) , abs(A[0,1])+abs(A[0,2])+ZZ.random_element(1,3) ) 
    A[1,1] = max( abs(A[1,1]) , abs(A[1,0])+abs(A[1,2])+ZZ.random_element(1,3) )
    A[2,2] = max( abs(A[2,2]) , abs(A[2,0])+abs(A[2,1])+ZZ.random_element(1,3) )

    import numpy as np
    import scipy.linalg as sl
    npA = np.matrix(A)
    npP,npL,npU = sl.lu(npA)
    #print "MATRIZ A=",A
    #print sl.lu(npA)
    L = matrix(R15,npL)
    U = matrix(R15,npU)
    return A,L,U





#END mathcommon.py

