# coding=utf-8

r"""
jinjatemplates -- Managing templates.


AUTHORS:

- Pedro Cruz (2016-01): first modifications for use in SMC.


EXAMPLES:

::
    
    sage -t jinjatemplates.py

::

    sage: from megua.jinjatemplates import templates
    sage: print templates.render("teste.txt",nomedopoema=u"Mar Portugu\xeas")
    X. Mar Português
    <BLANKLINE>
    Ó mar salgado, quanto do teu sal 
    São lágrimas de Portugal! 
    Por te cruzarmos, quantas mães choraram, 
    Quantos filhos em vão rezaram! 
    Quantas noivas ficaram por casar 
    Para que fosses nosso, ó mar! 
    <BLANKLINE>
    Valeu a pena? Tudo vale a pena 
    Se a alma não é pequena. 
    Quem quer passar além do Bojador 
    Tem que passar além da dor. 
    Deus ao mar o perigo e o abismo deu, 
    Mas nele é que espelhou o céu. 




DVELOPMENT:

Notes on Jinja2:

::
    from jinja2 import Environment, PackageLoader,FileSystemLoader,Template, TemplateNotFound
    di = { 'ex_10_0_4': 10 }
    template.stream(di).dump('new.tex')
    print "Template folders are: " + str(env.loader.searchpath)

Old way:

::

    try:
        tmpl = self.env.get_template(filename)
    except jinja2.exceptions.TemplateNotFound:
        return "MegBook: missing template %s"%filename


Solution using environment variables:

::

    #Templating (with Jinja2)
    if os.environ.has_key('MEGUA_TEMPLATE_PATH'):
        TEMPLATE_PATH = os.environ['MEGUA_TEMPLATE_PATH']
    else:
        from pkg_resources import resource_filename
        TEMPLATE_PATH = os.path.join(resource_filename(__name__,''),'template',natlang)



"""


#*****************************************************************************
#       Copyright (C) 2016 Pedro Cruz <PedroCruz@ua.pt>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************
  



#PYTHON modules
import jinja2  #see notes on Jinj2 above.
from os import environ

#SAGE modules
#OLD? from megua.mconfpackage import MEGUA_TEMPLATE_DIR

#tirar? from megua.mconfig import MEGUA_TEMPLATE_DIR




class JinjaTemplate:
    
    def __init__(self):
  
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(environ["MEGUA_TEMPLATE_DIR"]))
        

    def get_template(self,templatefilename):
        return self.env.get_template(templatefilename)

    def render(self, templatefilename, **user_context):
        """
        Returns HTML, CSS, LaTeX, etc., for a template file rendered in the given
        context.

        INPUT:

        - ``templatefilename`` - name of the template.

        - ``user_context`` - a dictionary; the context in which to evaluate
          the file's template variables

        OUTPUT:

        - a string - the rendered HTML, CSS, etc.

        BASED ON:

        - sage/devel/sagenb/sagenb/notebook/tempate.py

        """

        tmpl = self.env.get_template(templatefilename)

        return tmpl.render(**user_context)


templates = JinjaTemplate()
