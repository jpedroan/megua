# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 18:52:22 2016

@author: jpedro
"""

        #To be used on sphinx
        #TODO: move this somewhere.
        #f = codecs.open(sname+'.rst', mode='w', encoding='utf-8')
        #f.write(html_string)
        #f.close()

        #file with html to export.
        #f = open(sname+'.html','w')
        #f.write(html_string.encode('latin1'))
        #f.close()

        #Problems with many things:
        #html(html_string.encode('utf-8'))
    

        #Arrows #TODO: this is not working
        #if arrows:
        #    xmin = graphobj.xmin()
        #    xmax = graphobj.xmax()
        #    ymin = graphobj.ymin()
        #    ymax = graphobj.ymax()
        #    xdelta= (xmax-xmin)/10.0
        #    ydelta= (ymax-ymin)/10.0
        #    graphobj += arrow2d((xmin,0), (xmax+xdelta, 0), width=0.1, arrowsize=3, color='black') 
        #    graphobj += arrow2d((0,ymin), (0, ymax+ydelta), width=0.1, arrowsize=3, color='black') 
