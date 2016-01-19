"""
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

from sage.all import *

import jinja2


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


def to_unicode(s):
    if type(s)!=unicode:
        return unicode(s,'utf-8')
    else:
        return s



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


# =========
# TikZ Graphics
#================


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



#END mathcommon.py

