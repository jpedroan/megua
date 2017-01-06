"""
platex -- routines to compile MegUA generated tex files with pdflatex.


AUTHORS:

- Pedro Cruz (2011): initial version
- Pedro Cruz (2016): first modifications for use in SMC.



DEVELOPMENT:

- see in "old_code" the old file platex.py.

- http://stackoverflow.com/questions/8085520/generating-pdf-latex-with-python-script

- Don't show output messages directly when using notebook because:
    * it too noisy in the screen.
    * many times users are not latex professionals.

- utf-8 ou latin1:
    * use latin1 files because they can be exported to windows. 

- TODO: call latex many times only when requested
    * for a single problem this is not neeeded. But for booklets it could be.

- Use 1>&  2>, etc etc
   ver http://www.linuxsa.org.au/tips/io-redirection.html

- pdflatex -halt-on-error
   pdflatex -interaction nonstopmode
   Check man pdflatex

- Code to convert to latin1 for use in windows.

    #Unicode or latin1
    if type(latexstr)==unicode:
        #Conversion for ISO-8859-1 http://pt.wikipedia.org/wiki/ISO_8859-1
        latexstr_latin1 = latexstr.encode('latin1')
        latexstr_latin1.replace("utf8","latin1")
        
        #Store latexstr in filename
        fullpath = os.path.join(workdir, 'windows-'+filename+'.tex')
        f = open(fullpath,'w')
        f.write(latexstr_latin1)
        f.close()



"""


#*****************************************************************************
#       Copyright (C) 2011,2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


# PYTHON modules  
import re
import os
import subprocess
import codecs


# SAGE modules
from sage.misc.latex import have_pdflatex


# MEGUA modules
from megua.tounicode import to_unicode



def pcompile(latex_text, workdir, filename):
    r"""

    INPUT:

    - ``latex_text'': source LaTeX *text* in `utf8` or `str` type.
    - ``workdir'': directory where compilation is going to occur.
    - ``filename'': where to store the latex_text (with or without extension .tex).

    OUTPUT:

    - No output.

    It compiles and in case of bad compilation the managment is left to
    calling procedure.

    """

    #See /home/jpedro/sage/devel/sage/sage/misc/latex.tex
    assert have_pdflatex()


    #filename must contain no spaces
    filename = os.path.splitext(filename)[0]  # get rid of extension
    if len(filename.split()) > 1:
        raise ValueError, "platex.py say: filename must contain no spaces."

    #in case it's not utf8
    latex_text = to_unicode(latex_text)

    #Store latex_text in filename
    if '.tex' != filename[-4:]: #4 last chars
        filename = filename+'.tex'

    fullpath = os.path.join(workdir, filename)
    with codecs.open(fullpath,encoding='utf-8', mode='w+') as f:
        f.write(latex_text)
        
    lt = ['pdflatex', '-interaction', 'nonstopmode', filename]
    try:
        output = subprocess.check_output(lt,cwd=workdir) #return output in a string
        
        # rerun?
        # http://tex.stackexchange.com/questions/265744/how-to-know-if-a-latex-file-needs-another-compilation-pass
        if "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right." in output:
            print "="*20
            print "platex.py say: Running laTeX a second time."
            print "="*20
            output = subprocess.check_output(lt,cwd=workdir) #return output in a string
            if "LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right." in output:
                print "="*20
                print "platex.py say: Running laTeX a third and last time"
                print "="*20
                output = subprocess.check_output(lt,cwd=workdir) #return output in a string
    except subprocess.CalledProcessError as err:
        #Try to show the message to user
        #print "Error:",err
        #print "returncode:",err.returncode
        #print "output:",err.output
        #print "================"

        #Try to get line information from latex output errors and messages
        latex_error_pattern = re.compile(r"!.*?l\.(\d+)(.*?)$",re.DOTALL|re.M)
        match = latex_error_pattern.search(err.output) #create an iterator
        if match:
            #Try to get a debug mark
            lines = latex_text.split('\n')
            error_line = int(match.group(1))-2 #see above

            #Find exercise name.
            #Note that tex file must have tags:
            #     %LATEX DEBUG START {{unique_name}}
            #     %LATEX DEBUG END {{unique_name}}
            #in order to extract its name. 
            for i in xrange(error_line-1,len(lines)):
                if lines[i].find(r"%LATEX DEBUG END")>-1:
                    #First the "end" mark to get 
                    m_end = re.search("%LATEX DEBUG END (.+)",lines[i])
                    ex_unique_name = m_end.group(1)
                    print "\nExercise with name '{}' has a LaTeX compilation error.".format(ex_unique_name)
                    break

            #Print lines where the error could be.
            print "\n"
            for dk in xrange(-4,0):
                print "| :",lines[error_line+dk]
            print "> :", lines[error_line]
            for dk in xrange(1,5):
                print "| :",lines[error_line+dk]


        print "\n\nYou can inspect\n  %s\nand use your LaTeX "\
              "editor to help find the error in exercise source code.\n" % fullpath

        if match:
            #print LaTeX error style "l.9 ........"
            print match.group(0) 
            
        print "\n"
        raise UserWarning("Check exercise for LaTeX errors")



#======================
# Convert html to latex
#======================
 
#No groups, direct replacements
HTML2LATEX = [  (ur'(\d)%', ur'\1\%'),  # 3% --> 3\%
            (ur'(\d) %', ur'\1\%'),  # 3 % --> 3\%
#            (ur"'",ur"\prime"),
            (ur'<br>', u'\n\n'),
            (ur'<br/>', u'\n\n'),
            (ur'</br>', u'\n\n'),
            (ur'<b>', r'{\\bf '),
            (ur'</b>', u'}'),
            (ur'<p>', u'\n\n'),
            (ur'</p>', u'\n'),
            (ur'<ul>', u'\\begin{itemize}'),
            (ur'</ul>', u'\\end{itemize}'),
            (ur'<ol>', u'\\begin{enumerate}'),
            (ur'</ol>', u'\\end{enumerate}'),
            (ur'<li>', u'\\item '),    
            (ur'</li>', u'\n\n'),    
            (ur'<center>', '\n'+r'\\begin{center}'+'\n'),
            (ur'</center>', u'\\end{center}\n'),
            (ur'<style>(.*?)</style>', u'\n'),
            ("\\^'","^\\prime"),
            (ur'<pre>(.*?)</pre>',ur'\n%Falta colocar linhas vazias em baixo\n\\begin{alltt}\n\1\n\\end{alltt}\n\n'), 
        ]



def html2latex(htmltext):
    r"""
    Replace:

    * \n\n\n by \n\n (reduce to much blank lines);
    * <p> by \n\n; </p> by empty string;
    * not any more ==> * <center> by \n\n; </center> by empty string;
    """

    newtext = htmltext
    for pr in HTML2LATEX:
        (newtext, nr) = re.subn(pr[0], pr[1], newtext, count=0, flags=re.DOTALL|re.UNICODE)

    #Convert from <table> to \begin{tabular}
    newtext = table2tabular(newtext)
    

    #Removing spaces and lots of blank lines.
    nr = 1
    while nr >= 1:
        (newtext, nr) = re.subn(u'\n\n\n', u'\n\n', newtext, count=0, flags=re.UNICODE)
        #print "html2latex():", nr

    return newtext

HTML2TABULAR = [
            (u'<table(.*?)>', u'\n\n\\begin{tabular}{...}\n'),
            (u'</table>', u'\n\end{tabular}\n'),
            (u'<tr(.*?)>', u'\n'),
            (u'</tr>', u' \\\\ \hline\n'), 
            (u'<td(.*?)>', u' '),
            (u'</td>', u' & '),
        ]


def table2tabular(text):
    r"""Convert <table>...</table> to \begin{tabular} ... \end{tabular}"""

    newtext = text
    for pr in HTML2TABULAR:
        (newtext, nr) = re.subn(pr[0], pr[1], newtext, count=0, flags=re.DOTALL|re.UNICODE)
    
    return newtext

def latexcommentthis(txt):
    """Put % signs in each line"""
    txt += u'\n' #assure last line has "\n"
    tlist = re.findall('(.*?)\n', txt, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)
    return u'\n'.join( [ '%'+t for t in tlist] ) + u'\n'
        


def latexunderscore(txt):
    """Put \_  in each underscore"""
    return re.subn("_","\_",txt,flags=re.UNICODE)[0]

def equation2display(txt):
    """Put \displaystyle\$  in each $$"""
    return re.subn(r"\$\$(.*?)\$\$",r"$\displaystyle \1$",txt, re.DOTALL | re.MULTILINE | re.IGNORECASE | re.UNICODE)[0]
        
