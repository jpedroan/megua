# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 15:54:01 2016

@author: jpedro
"""


    def r_graphic(self, r_commands, varname,dimx=7,dimy=7): #cm
        """This function executes r_commands in a shell that should produce a plot (boxplot, etc) 
           to a file that will be located inside
           a "image/" directory.

        NOTE: the sage interface "r." is not capable of ploting at 
        least in version 5.2" because png was not compiled with R.
        This function uses an external (to Sage) fresh R instalation.

        INPUT:

            - `r_commands`: valid sequence of R commands to be executed that should produce a graphic.

            - `varname`: user supplied string that will be part of the filename.

            - `dimx` and `dimy`: size in centimeters.
        
        OUTPUT:

            - a graphic png boxplot inside directory "image/".

        """

        #base name for the graphic file
        gfilename = '%s-%s-%d'%(self.name,varname,self.ekey)
        #create if does not exist the "image" directory
        #os.system("mkdir -p images") #The "-p" ommits errors if it exists.

        f = open("_images/%s.R" % gfilename,"w")
        #f.write("setwd('images')")
        f.write("png('%s.png',width = %d, height = %d, units = 'cm', res=100)\n" % (gfilename,dimx,dimy) )
        f.write(r_commands + '\n')
        f.write("dev.off()\n")
        f.close()
        #os.system("/usr/bin/R --silent --no-save < _images/%s.R" % gfilename)
        os.system("cd _images; unset R_HOME; /usr/bin/R CMD BATCH --quiet --no-environ --no-save --slave -- %s.R" % gfilename)
        #os.system("/usr/bin/R --slave --no-save -f _images/%s.R" % gfilename)

        #Check ex.py:sage_graphic(): this will add a new image to the exercise.
        self.image_list.append(gfilename) 
        return r"<img src='_images/%s.png'></img>" % gfilename
