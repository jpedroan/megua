# coding=utf-8

r"""
UnifiedGraphics - This module defines common operations for graphics.

AUTHORS:

- Pedro Cruz (2016-01): First version (refactoring old "megua" for SMC).


DISCUSSION:

Image sources are:

- sage commands (plots, graphcs, etc)
- R commands
- Static images
- Python Matplotlib and other python libs
- LaTeX using "standalone" package
- TikZ (a particular case of the above)
- other sources...?

Exporting them to:

- <img> tags in html
- <svg> tags in html
- folder of images for some exercise (for example, a latex document)
- filesystem or database


EXAMPLES:


Test examples using:

::

    sage -t ug.py

    
Defining a new exercise template:
    
::    

    sage: from megua.exbase import ExerciseBase
    sage: class DrawSegment(ExerciseBase):
    ....:     #class variables
    ....:     _unique_name  = "DrawSegment"
    ....:     _suggestive_name = "Draw a segment"
    ....:     _summary_text = "Draw a segment."
    ....:     _problem_text = "Draw the segment a1 + a2@()x for x in [x1,x2]."
    ....:     _answer_text  = "<p>fig1</p><p>img1</p>"
    ....:
    ....:     def make_random(self,edict=None):
    ....:        self.a1 = ZZ.random_element(-10,10+1)
    ....:        self.a2 = ZZ.random_element(-10,10+1)
    ....:        self.x1 = ZZ.random_element(-5,0)
    ....:        self.x2 = ZZ.random_element( 1,5)
    ....:        p = plot( self.a1 + self.a2*x, x, self.x1, self.x2)
    ....:        self.fig1 = self.sage_graphic(graphobj=p,varname="fig1",dimx=50,dimy=50,dpi=10)
    ....:        self.img1 = self.static_image(url="http://www.sagemath.org/pix/sage-sticker-1x1_inch-small.png",dimx=50,dimy=50)
    ....:        ExerciseBase.make_random(self,edict)


Plot using embed images with base64 and svg:
       
::
open /projects/69b82f4f-dc00-498d-817e-f3575041e14e/.local/lib/python2.7/site-packages/megua/ug.py
       sage: ex = DrawSegment(ekey=0)
       sage: #ex.print_instance() #render = base64, long textual answer
       
Plot using file and <img> tag:       

::

       sage: ex.update(ekey=0,render_method="imagefile") #update graphic links, keep ekey=0
       sage: ex.print_instance()
       ------------------------
       Instance of: DrawSegment
       ------------------------
       ==> Summary:
       Draw a segment.
       ==> Problem instance
       Draw the segment 1 + (-7)x for x in [-4,2].
       ==> Answer instance
       <p>\n<img src='_output/DrawSegment/DrawSegment-fig1-0.png' alt='DrawSegment-fig1-0.png graphic' height='50' width='50'></img>\n</p><p>\n<img src='_output/DrawSegment/sage-sticker-1x1_inch-small.png' alt='sage-sticker-1x1_inch-small.png graphic' height='50' width='50'></img>\n</p>
       
Plot using ascii art:
       
::
       
       sage: ex.update(ekey=0,render_method="asciiart") #must be called to update graphic links
       sage: #ex.print_instance() #long output

Using LaTeX to generate graphics or extractions from LaTeX:

::

       sage: class LaTexBasedImages(ExerciseBase):
       ....:     #class variables   
       ....:     _unique_name  = "LaTexBasedImages"
       ....:     _suggestive_name = "LaTex Based Images"
       ....:     _summary_text = "LaTex Based Images."
       ....:     _problem_text = "Check this:"
       ....:     _answer_text  =  r'''<latex 100%>\[\sqrt x\]</latex> '''\
       ....:                      r'''<latex 100%>\fbox{Olá}</latex>'''
       sage: ex = LaTexBasedImages()
       sage: ex.update(ekey=0,render_method="imagefile")
       sage: print ex.latex_render(ex.answer()) #long output
       <BLANKLINE>
       <img src='_output/LaTexBasedImages/LaTexBasedImages-0-00.png' alt='LaTexBasedImages-0-00.png graphic' height='47' width='47'></img>
       <BLANKLINE>
       <img src='_output/LaTexBasedImages/LaTexBasedImages-0-01.png' alt='LaTexBasedImages-0-01.png graphic' height='59' width='47'></img>
       <BLANKLINE>


Example with an ascii art graphic:

::

       sage: class UnitCircle(ExerciseBase):
       ....:     #class variables   
       ....:     _unique_name  = "UnitCircle"
       ....:     _suggestive_name = "Draw a segment."
       ....:     _summary_text = "Plot a Circle"
       ....:     _problem_text = "Draw a unit circle."
       ....:     _answer_text  = "\nplot1\n"
       ....:     def make_random(self,edict=None):
       ....:        c = circle( (0,0),1,thickness=2,fill=True,facecolor='black')
       ....:        c.axes(False)
       ....:        self.plot1 = self.sage_graphic(graphobj=c,varname="plot1",dimx=10,dimy=10)
       sage: ex = UnitCircle(ekey=0,rendermethod="asciiart")   
       sage: print ex.answer() #expected graphic in asciiart
       <BLANKLINE>
       QQQQ??4QQQ
       QQ'     4Q
       Q'       4
       Q        ]
       f         
       f         
       6        _
       Q        j
       Q6      _Q
       QQga  _wQQ
       <BLANKLINE>
       sage: print ex.image_pathnames
       ['_output/UnitCircle/UnitCircle-plot1-0.png']       

       
DEVELOPMENT:

Install aalib insto SageMath using this:

$ sage -pip install --user https://pypi.python.org/packages/2d/3d/dca492960070685bc1bc12535d274a840f35cf5267f2a4a6ee36f3eb3dd7/python-aalib-0.3.tar.gz#md5=00afa7ef3479649cec99046449c07ef9Collecting https://pypi.python.org/packages/2d/3d/dca492960070685bc1bc12535d274a840f35cf5267f2a4a6ee36f3eb3dd7/python-aalib-0.3.tar.gz#md5=00afa7ef3479649cec99046449c07ef9
  Downloading python-aalib-0.3.tar.gz
Installing collected packages: python-aalib
  Running setup.py install for python-aalib ... done
Successfully installed python-aalib


"""


#*****************************************************************************
#       Copyright (C) 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************


#SAGEMATH modules
from sage.all import * #All Sage Graphics


#MEGUA modules
from megua.jinjatemplates import templates
from megua.platex import pcompile

#PYTHON modules
#import io
#import urllib2
import os

#TODO: postponed because of problems with python setup.py install
#import aalib
import PIL.Image

import re
import subprocess



class UnifiedGraphics:
    """Class ``UnifiedGraphics``: a class to handle graphics and images."""

    def __init__(self,imagedirectory,rendermethod='base64',dimx=150,dimy=150,dpi=100):

        #embed images in html (or other source)
        self.render_method(rendermethod)
        
        #default values
        #TODO: specify units !!
        self.dimx = dimx
        self.dimy = dimy
        self.dpi = dpi
        
        assert(imagedirectory)
        self.imagedirectory = imagedirectory        
        self.image_pathnames = []
        
        



    #TODO: tirar este método
    def render_method(self,rendermethod=None):
        if rendermethod in ['includegraphics','imagefile', 'base64', 'asciiart']:
            self._rendermethod = rendermethod
            return self._rendermethod
        elif not rendermethod:
            return self._rendermethod
        else:
            raise NotImplementedError("ug module: method '{0}' not implemented.".format(rendermethod))


    def __str__(self):
        return "UnifiedGraphics"


    def __repr__(self): 
        return "UnifiedGraphics({0})".format(self.__dict__)


    def get_ekey(self):
        raise NotImplementedError


    def unique_name(self):
        raise NotImplementedError


    #def _render(self,gfilename,dimx=None,dimy=None,dpi=None,dimsfromimage=False):
    def _render(self,gfilename):
        r"""render  image `gfilename` using one of the methods:
        - base64 and svg tag
        - <img> and file
        - asciiart
        and return a string with:
        - svg tag and a large base64 string
        - <img> tag pointing to a file on directory system
        - asciiart string.

        This method also adds the gfilename to exericse own image list.

        """

        assert(gfilename)

        pathname  = os.path.join(self.imagedirectory,gfilename)
        print "ug.py: self.imagedirectory=",self.imagedirectory
        self.image_pathnames.append(pathname)

        #Get dimensions
        (dimx,dimy) = PIL.Image.open(pathname).size

        if not dimx:
            dimx = self.dimx
        if not dimy:
            dimy = self.dimy

        print "ug.py for <img> tag: dimx=",dimx,"dimy=",dimy
            
        if self._rendermethod=='imagefile':
            return r"<p>IMAGEM inicio:<br/><img src='%s' alt='%s' height='%d' width='%d'></img>IMAGEM fim<br/></p>" % (pathname,gfilename+' graphic',dimx,dimy) #
        elif self._rendermethod=='includegraphics':
            return "\n\\includegraphics[height=%din,width=%din]{%s}\n" % (dimy,dimx,pathname)
        elif self._rendermethod=='asciiart':
            print "ug.py say: 'asciiart' is not yet implemented"
            #screen = aalib.AsciiScreen(width=dimx, height=dimy)
            #image = PIL.Image.open(pathname).convert('L').resize(screen.virtual_size)
            #screen.put_image((0, 0), image)
            #return screen.render()
            return "ug.py say: 'asciiart' is not yet implemented"
        elif self._rendermethod=='base64':
            #'\n<img height="%d" width="%d" src="data:image/png;base64,{0}"></img>\n'.format(....)
            data_uri = open(pathname, 'rb').read().encode('base64').replace('\n', '')
            img_tag = templates.render("ug_svg.html",
                                       dimx=dimx,
                                       dimy=dimy,
                                       base64=data_uri)
            return img_tag
        else:    
            raise("ug.py module: render method not implemented.")



    def static_image(self,imagefilename=None,url=None,dimx=150,dimy=150):
        """This function is to be called by the author in the make_random or solve part.

        INPUT:

        - `fullfilename`: full filename for the graphic or picture.
        - `dimx` and `dimy`: display image in (dimx,dimy) pixels.

        NOTES:
            - see also ``s.sage_graphic``.
        """ 
        if url:
            #TODO: use this instead of "wget"
            #fp = io.BytesIO(urllib2.urlopen('https://www.python.org/static/favicon.ico').read())
            #image = PIL.Image.open(fp).convert('L').resize(screen.virtual_size)
            os.system(r"""cd {0}; wget -q '{1}'""".format(self.imagedirectory,url))
            gfilename = os.path.split(url)[1]

        if imagefilename:
            os.system('cp "{0}" "{1}"'.format(imagefilename,self.imagedirectory))
            gfilename = os.path.split(imagefilename)[1]

        #print "gfilename=",gfilename

        return self._render(gfilename, dimx,dimy)




    def sage_graphic(self,graphobj,varname,dimx=15,dimy=15,dpi=100):
        """This function is to be called by the author in the make_random or solve part.
        INPUT:

        - `graphobj`: some graphic object.

        - `varname`: user supplied string that will be part of the filename.

        - `dimx` and `dimy`: size in centimeters.

        """ 

        gfilename = '%s-%s-%d.png'%(self.unique_name(),varname,self.get_ekey())
        #create if does not exist the "image" directory
        #os.system("mkdir -p images") #The "-p" ommits errors if it exists.

        #graphobj could be sage or matplotlib object.

        #print "ug.py: saving graphic in:", os.path.join(self.imagedirectory,gfilename)
        #TODO: protect agains too big images.
        if type(graphobj)==sage.plot.graphics.Graphics:
            graphobj.save(
                os.path.join(self.imagedirectory,gfilename),
                #figsize=(dimx,dimy), 
                figsize=(dimx/2.54,dimy/2.54),
                dpi=dpi)
        else: #matplotlib assumed
            #http://stackoverflow.com/questions/9622163/matplotlib-save-plot-to-image-file-instead-of-displaying-it-so-can-be-used-in-b
            import matplotlib.pyplot as plt
            from pylab import savefig
            fig = plt.gcf() #Get Current Figure: gcf
            fig.set_size_inches(dimx/2.54,dimy/2.54) #(dimx/2.54,dimy/2.54)
            savefig(os.path.join(self.imagedirectory,gfilename)) #,figsize=(dimx/2.54,dimy/2.54),dpi=100)
            
        txt = self._render(gfilename)
        #print "ug.py: ",txt
        #exit(-1)
        #ticket: https://sagemathcloud.zendesk.com/requests/2573
        return txt


    def latex_render(self,input_text):
        """Returns a new text obtained by transforming `input_text`: 
        * all tag pairs <latex percent%> ... </latex> that 
           are present in `input_text` are replaced by "images" created from 
           the LaTeX inside tag pairs and a `new_text` is returned.
        
        INPUT:
        
        - `input_text` -- some text (problem or answer) eventually with <latex percent%> ... </latex> tags.
        
        OUTPUT:
        
        - `string` -- with images created from latex inside tags

        NOTE:
        
        - Dimensions are specifyed in each <latex tag> and not in dimx=150,dimy=150.
        
        DEVELOPER NOTES:
        
        - check LATEXIMG.PY
        - important \\ and \{
        - old pattern:
            - tikz_pattern = re.compile(r'\\begin\{tikzpicture\}(.+?)\\end\{tikzpicture\}', re.DOTALL|re.UNICODE)
            
        Latex packages:
        - standalone: cuts "paper" around the tikzpicture (and other environments) 
        - adjustbox package: http://mirrors.fe.up.pt/pub/CTAN/macros/latex/contrib/adjustbox/adjustbox.pdf

        About the standalone package:
        
        - \documentclass[varwidth=true, border=10pt, convert={density=100,outfile="gfilename.png"} ]{standalone}
        - the above command generates a gfilename.png but needs --shell_escape in pdflatex command.

        old way to convert latex/tikz to png:

        ::        
                #The following is done by standalone package:
                ##convert -density 600x600 pic.pdf -quality 90 -resize 800x600 pic.png
                ##cmd = "cd _images;convert -density 100x100 '{0}.pdf' -quality 95 -resize {1} '{0}.png' 2>/dev/null".format(
                    #gfilename,match.group(1),gfilename)
                #print "============== CMD: ",cmd
                #os.system(cmd)
                #os.system("cp _images/%s.tex ." % gfilename)

        
        """
        
        #Organization of the tag pair:
        #print "Group 0:",match.group(0) #all
        #print "Group 1:",match.group(1) #scale (see http://www.imagemagick.org/script/command-line-processing.php#geometry)
        #print "Group 2:",match.group(2) #what is to compile

        latex_pattern = re.compile(r'<\s*latex\s+(\d+%)\s*>(.+?)<\s*/latex\s*>', re.DOTALL|re.UNICODE)
        latex_error_pattern = re.compile(r"!.*?l\.(\d+)(.*?)$",re.DOTALL|re.M)

        #Cycle through existent latex code and produce pdf and png files.
        graphic_number = 0
        match_iter = re.finditer(latex_pattern,input_text)#create an iterator
        for match in match_iter:
            #Graphic filename
            gfilename_base = '%s-%d-%02d'%(self.unique_name(),self.get_ekey(),graphic_number)
            gfilename      = '%s-%d-%02d.png'%(self.unique_name(),self.get_ekey(),graphic_number)

            #Compile what is inside <latex>...</latex> to a image
            latex_source = match.group(2) 

            try:
                
                latex_document = templates.render("standalone_latex.tex", 
                                gfilename=gfilename, 
                                latex_source=latex_source)
                pcompile(latex_document,self.imagedirectory,gfilename)
            
                cmd = "cd {2};convert -density 100x100 '{0}.pdf' -quality 95 -resize {1} '{0}.png' 2>/dev/null".format(
                    gfilename_base,match.group(1),self.imagedirectory)

                    
                #TODO: check that "convert" is installed
                os.system(cmd)

                graphic_number += 1
                
            except subprocess.CalledProcessError as err:
                
                # ==============================
                #TODO: modify this for standalone package:
                # ==============================

                #Try to show the message to user
                #print "Error:",err
                #print "returncode:",err.returncode
                #print "output:",err.output
                #print "================"
                match = latex_error_pattern.search(err.output) #create an iterator
                if match:
                    print match.group(0)
                else:
                    print "There was a problem with an latex image file."

                #TODO: check this code below:
                #if latex inside codemirror does not work
                #this is the best choice: 
                #print "You can download %s.tex and use your windows LaTeX editor to help find the error." % gfilename
#                os.system("mv _images/%s.tex ." % gfilename)
#
#                #Using HTML and CodeMirror to show the error.
#                print "You can open %s.html to help debuging." % gfilename
#                tikz_html = templates.render("latex_viewer.html", 
#                                pgfrealjobname=r"\pgfrealjobname{%s}"%self.name, 
#                                beginname=r"\beginpgfgraphicnamed{%s}"%gfilename, 
#                                tikz_tex=tikz_tex,
#                                sname=self.name,
#                                errmessage=match.group(0),
#                                linenum=match.group(1)
#                                )
#
#                f = codecs.open(gfilename+'.html', mode='w', encoding='utf-8')
#                f.write(tikz_html)
#                f.close()
#                print "================"
                raise err


        #Cycle through existent tikz code and produce a new html string .
        new_text = input_text
        for gn in range(graphic_number):
            gfilename = '%s-%d-%02d.png'%(self.unique_name(),self.get_ekey(),gn)
            img_string = self._render(gfilename,dimsfromimage=True)
            (new_text,number) = latex_pattern.subn(img_string, new_text, count=1)
            assert(number)    
        
        return new_text



    
#end of ug.py
    