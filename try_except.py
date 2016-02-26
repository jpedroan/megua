# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 20:19:42 2016

@author: jpedro
"""

        
        try:
            #exec compile(sage_class,row["unique_name"],'eval')
            #TODO: http://www.sagemath.org/doc/reference/misc/sage/misc/sage_eval.html
            # and spread this for more points in code.
            sage_class = preparse(row['class_text'])
            exec sage_class
        except: 
            tmp = tempfile.mkdtemp()
            pfilename = tmp+"/"+row["unique_name"]+".sage"
            pcode = open(pfilename,"w")
            pcode.write("# -*- coding: utf-8 -*\nfrom megua import *\n" + row['class_text'].encode("utf-8") )
            pcode.close()
            errfilename = "%s/err.log" % tmp
            os.system("sage -python %s 2> %s" % (pfilename,errfilename) )
            errfile = open(errfilename,"r")
            err_log = errfile.read()
            errfile.close()
            #TODO: adjust error line number by -2 lines HERE.
            #....
            #remove temp directory
            #print "=====> tmp = ",tmp
            os.system("rm -r %s" % tmp)
            print err_log #user will see errors on syntax.
            raise SyntaxError  #to warn user #TODO: not always SyntaxError
    
    
        #Get class name
        ex_class = eval(row['unique_name']) #String contents row['unique_name'] is now a valid identifier.
    
        #class fields
        ex_class._summary_text = row['summary_text']
        ex_class._problem_text = row['problem_text']
        ex_class._answer_text  = row['answer_text']
    
        return ex_class
