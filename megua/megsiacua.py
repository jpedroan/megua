# coding=utf-8

r"""
MegSiacua -- Functions to work with one or a list of ExSiacua exercises.

See MegBook that an author uses as a front-end.

AUTHORS:

- Pedro Cruz (2016-01): first modifications for use in SMC.


TESTS:

::

    sage -t megsiacua.py


#TODO megsiacua: create docstring examples.

Create or edit a database using front-end MegBook with ExSiacua exercises:

::


  sage: from megua.megbook import MegBook 
  sage: #from megua.exsiacua import ExSiacua
  sage: meg = MegBook(r'_input/megbook.sqlite') 
  sage: meg.save(r'''
  ....: %summary Regra de Laplace
  ....:  
  ....: SIACUAstart
  ....: level=1
  ....: slip=0.2
  ....: guess=0.25
  ....: discr=0.3
  ....: concepts = [(4731, 1)]
  ....: SIACUAend 
  ....:  
  ....: %problem Números Bolas e Caixas
  ....:  
  ....: Considera uma caixa com v1 bolas indestiguiveis ao tato, numeradas de 1 a v1.
  ....: Considera também um dado equilibrado com as faces numeradas de 1 a 6.
  ....: Lança-se o dado e tira-se, ao acaso, uma bola da caixa.
  ....: Qual é a probabilidade de os números saídos serem ambos menores que v2?  
  ....:  
  ....: <multiplechoice>
  ....: <choice> $$vresp$$ </choice>
  ....: <choice> $$err1$$ </choice>
  ....: <choice> $$err2$$ </choice>
  ....: <choice> $$err3$$ </choice>
  ....: </multiplechoice>
  ....:  
  ....: %answer
  ....:  
  ....: A resposta é $vresp$.
  ....:  
  ....: <br> Pretendemos saber a probabilidade de os números obtidos serem ambos menores que v2.<br>
  ....:  
  ....: <br> Para determinar a probabilidade pedida utilizaremos a Regra de Laplace 
  ....: $$P(\text{ambos os números menores que v2})=\frac{\text{nº de casos favoráveis}}{\text{nº de casos possíveis}}$$
  ....:  
  ....: Comecemos por construir uma tabela que nos permita verificar todas as hipóteses possíveis de resultado:<br>
  ....:  
  ....: $$\begin{array}{|a|a|c|c|c|c|c|}
  ....: \hline
  ....:     B/D & 1 & 2 & 3 & 4 & 5 & 6\\ \hline
  ....:      
  ....:     linhas
  ....: \end{array}$$
  ....:  
  ....: A caixa tem v1 bolas numeradas de 1 a v1 e o dado tem 6 faces também numeradas de 1 a 6. Portanto:
  ....:   
  ....:    $$\text{O número de casos possíveis é dado por: } v1 \times 6 = v3$$
  ....:  
  ....: Pretendemos saber a probabilidade de, ao retirar uma bola do saco e lançar o dado, 
  ....: obter dois numeros menores que v2.<br>
  ....: <br> Pela tabela podemos verificar que 
  ....:     $$\text{O número de casos favoráveis são } cf$$ 
  ....:      
  ....: Logo a probabilidade pedida é dada por:
  ....:     $$P(\text{ambos os números menores que v2}) = \frac{cf}{cp} = vresp$$  
  ....:  
  ....: class E97K50_Laplace_001(ExSiacua):
  ....:  
  ....:     def make_random(s):
  ....:  
  ....:         s.v1 = ur.iunif(6,10)
  ....:         s.v2 = ur.iunif(2,s.v1)
  ....:  
  ....:         #d={1:0,2:1,3:4,4:9,5:16,6:25,7:36}
  ....:         if s.v2<=7:
  ....:             s.cf = (s.v2-1)^2
  ....:         else:
  ....:             s.cf = 36 + 6*(s.v2 - 7)
  ....:         s.cp = 6*s.v1
  ....:         #s.cf = d[s.v1]
  ....:         s.vresp= round(s.cf/s.cp,2)
  ....:          
  ....:         s.linhas = ""
  ....:         for i in range(s.v1):
  ....:             linha = str(i+1) 
  ....:             for j in range(6):
  ....:                 linha = linha + s.C(i+1,j+1)
  ....:             s.linhas = s.linhas + linha + r" \\ \hline" 
  ....:         s.v3 = s.v1 * 6
  ....:          
  ....:         #Opções Erradas 
  ....:         s.err1 = round(s.vresp*0.9,2)
  ....:         s.err2 = round(s.vresp*1.2,2)
  ....:         s.err3 = round(s.vresp*1.3,2)
  ....:      
  ....:     def C(s,B,D):
  ....:         if B < s.v2 and D < s.v2:
  ....:             return '&(%d,%d)' % (B,D)
  ....:         else:
  ....:             return '& '
  ....:  
  ....: ''')
  exsiacua module: open file _output/E97K50_Laplace_001/E97K50_Laplace_001.html in the browser and press F5.
  sage: #meg.siacua("E97K50_Laplace_001",ekeys=[9],sendpost=True,course="matsec",usernamesiacua="f1183",siacuatest=True) #long random output


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
    def siacua(self,unique_name,ekeys=[],sendpost=False,course="calculo3",usernamesiacua="",grid2x2=0,siacuatest=False):
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

            ssssage: meg.siacua(exname="E12X34",ekeys=[1,2,5],sendpost=True,course="calculo2",usernamesiacua="jeremias")


        LINKS:
            http://docs.python.org/2/library/json.html
            http://stackoverflow.com/questions/7122015/sending-post-request-to-a-webservice-from-python

        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.


        """

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

    
    def siacuapreview(self,unique_name,ekeys):
        r"""

        INPUT:

        - ``unique_name``: unique exercise name (name in "class E12X34_something_001(Exercise):").

        - ``ekeys``: list of numbers that generate the same problem instance.

        OUTPUT:

        - this command writes an html file with all instances.

        NOTE:

        - you can export between 3 and 6 wrong options and 1 right.

        EXAMPLE:

            sssssage: ex.siacuapreview(ekeys=[1,2,5])


        Algorithm:
            1. Read from "%ANSWER" until "</generalfeedback>" and parse this xml string.

        """
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
        
        
