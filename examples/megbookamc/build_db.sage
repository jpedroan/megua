# -*- coding: utf-8 -*-

from megua.all import *
meg = MegBook('amc.sqlite')



# ==================
# Base de Exercícios
# ==================

meg.save(r'''


%SUMMARY  Equações diferenciais; Equações diferenciais lineares de 1ª ordem; Fator integrante

Resolver equações lineares de 1ª ordem.

34-XX Equações diferenciais ordinárias; 34A30 Linear equations and systems, general

Palavras chave: Equações diferenciais lineares de 1ª ordem;  Fator integrante; Solução de uma equação diferencial.


SIACUAstart
level=2;  slip= 0.2; guess=0.25; discr=0.3
concepts = [(2223,1)]
SIACUAend
 
%PROBLEM Polinómio

Considere a equação diferencial
$$left1=right1$$
A sua solução geral é




%ANSWER

<multiplechoice>
<choice> $$y=sol1, \; \mbox{com}\; k \in \mathbb{R}$$ </choice>
<choice> $$y=errada1, \; \mbox{com}\; k \in \mathbb{R}$$ </choice>
<choice> $$y=errada2, \; \mbox{com}\; k \in \mathbb{R}$$ </choice>
<choice> $$y=errada3, \; \mbox{com}\; k \in \mathbb{R}$$ </choice>
</multiplechoice>


Uma equação diferencial linear de 1ª ordem é do tipo
$$a_0(x)y'+a_1(x)y=b(x)$$
onde $a_0$ é uma função não nula. Pode ser também escrita na forma $y'+P(x)y=Q(x)$. 
A equação dada é equivalente a 
$$f1=f2$$
que é uma equação do tipo $y'+P(x)y=Q(x)$, onde $\displaystyle P(x)=P1$ e $\displaystyle Q(x)=Q1$.

Procuremos um factor $\mu(x)$ que transforme a equação numa equação diferencial fácil de integrar:
$$\mu(x)(y'+P(x)y)=\mu(x)Q(x)$$    
este fator será dado por $\mu(x)=e^{\int{P(x)dx}}$

$$\int{P(x)dx}=P1i$$
Assim, $\mu$ pode ser
$$\mu(x)=e^{P1i}$$
Reescrevendo a equação diferencial teremos
$$left11=right11$$
Como 
$$left11=\left(aux2\right)'$$
podemos afirmar que
$$aux2=\int{right11 \, dx}=right11i+k$$
    
Então $$y=sol1,\; k \in \mathbb{R}$$


class E34A30_FatorIntegrante_002(Exercise):
    
    def make_random(s):

        #s.sv=SR.var('s')
        x=var('x',latex_name='x')
        #y=var('y')
        t=var('t')
        s.yv = var('y') #define y como var
        s.yd = var('yd', latex_name='y^\prime') #define y' como var e aparece y'
        s.ydd = var('ydd', latex_name='y^{\prime\prime}') #define y'' como var e aparece y''
        #y = function('y',t)
        s.dy=SR.var('dy', latex_name='dy')
        s.dx=SR.var('dx', latex_name='dx')
        s.a1=ur.iunif_nonset(-8,8,[0])
        s.b1=ur.iunif_nonset(-8,8,[0])
        s.c1=ur.iunif_nonset(-8,8,[0])
        s.c2=ur.iunif_nonset(-8,8,[0])
        s.c3=ur.iunif_nonset(0,8,[0])
        
        
        
        #defining P and Q on the equation y'+P(x)y=Q(x)
        s.P1=s.a1*x/(s.b1+x^2)
        #choosing Q
        s.j1=ur.iunif(1,2)
        if s.j1==1:
            s.Q1=s.c2*x+s.c3
        else:    
            s.Q1=s.c2*x^2
        #i1- decides how the equation is presented
        s.i1=ur.iunif(1,4)
        if s.i1==1:
            s.left1=1/s.P1*s.yd+s.yv
            s.right1=s.Q1/s.P1
        elif s.i1==2:
            s.left1=s.yd
            s.right1=s.Q1-s.P1*s.yv
        elif s.i1==3:
            s.left1=s.dy/s.P1
            s.right1=(-s.yv+s.Q1/s.P1)*s.dx
        else:
            s.left1=s.yd+s.P1*s.yv-s.Q1 
            s.right1=0
        #normal equation
        s.f1=s.yd+s.P1*y
        s.f2=s.Q1     
                
                
    def solve(s):
        k=var('k')
        z=var('z')
        s.M1=s.P1*s.yv-s.Q1
        s.N1=1
        #auxiliary function
        s.aux1=s.M1*s.dx+s.N1*s.dy
        s.M1d=derivative(s.M1,y)
        s.N1d=derivative(s.N1,x)
        #integrant factor
        s.P1i=integrate(s.P1,x)
        #rewriting the equation
        s.aux21=simplify(e^s.P1i)
        s.left11=s.aux21*s.yd+s.aux21*s.P1*s.yv
        s.right11=s.aux21*s.Q1
        s.aux2=s.aux21*s.yv
        #integrating e^mu Q1
        s.right11i=integrate(s.right11,x)
        s.sol1=(s.right11i+k)/s.aux21
        #multiple choice
        s.errada1=s.right11i+k
        s.errada2=s.right11i/s.aux21+k
        s.errada3=(s.right11i+k)*s.aux21
        
        
  
    def cp(s,p,x):
        #ver http://ask.sagemath.org/question/1101/coefficients-of-a-constant-polynomial
        
        SRp = SR(p)
        deg = SRp.degree(x)
        nc = []
        co = SRp.coefficients(x)
        i=0
        for ce in range(deg+1):
            if co[i][1] == ce:
                nc.append( co[i][0] )
                i=i+1
            else:
                nc.append( 0 )
        return nc    
    
        
        
    
    def rewrite(self,text0):

        modifications = [
            ( ur'e\^\{\\left\((.+?)\\right\)\}'  ,   r'e^{\1}'  ),
            ( ur'\\log\\left\((.+?)\\right\)'  ,   ur'\ln\left(\1\\right)'  ),
            ( ur'dy x y', ur'x y dy' ), 
            ( ur'dx x y', ur'x y dx' ), 
            ( ur'dy x', ur'x dy' ),
            ( ur'dy y', ur'y dy' ),
            ( ur'dx x', ur'x dx' ),
            ( ur'dx y', ur'y dx' )
        ]
        
        text = text0
        for m in modifications:
            text =  re.sub( m[0], m[1], text, re.U )
                
        return text  
                 
        
                        
''')


meg.save(r'''

%SUMMARY Espaço vetorial e Referenciais Ortonormados; Produto escalar entre vetores
Neste exercício pretende determinar-se o produto escalar entre dois vetores, dadas as suas normas, com dados no enunciado que possibilitam a determinação do cosseno do ângulo por eles formado. Tanto as normas dos vetores, como as medidas dos catetos, são valores parametrizados. 
A figura foi inicialmente criada utilizando o software "Geogebra", exportada para linguagem "TikZ" e posteriormente parametrizada.
Neste exercício houve necessidade de efetuar arredondamentos de números, utilizando instrução "round", para a parametrização da figura.



Palavras chave: Produto escalar


SIACUAstart
level=1;  slip= 0.2; guess=0.25; discr = 0.3 
concepts = [(4341, 1)]
SIACUAend

Autor: Ana Palmeira, 2014


%PROBLEM Produto escalar

Na figura estão representados dois vetores, $\overrightarrow{AD}$ e $\overrightarrow{AE}$, de normas $b1$ e $b2$, respetivamente.

\begin{tikzpicture}[line cap=round,line join=round,>=triangle 45,x=1.0cm,y=1.0cm]
\clip(-0.56,-0.74) rectangle (f3,f4);
\draw [->] (0.0,-0.0) -- (b2,0.0);
\draw [->] (0.0,-0.0) -- (f1,f2);
\draw (a1,a2)-- (a1,0.0);
\draw (0,0)-- (a1,a2);   
\draw (0,0)-- (a1,0);
\draw (0,0) node[anchor=north] {$A$};
\draw (a1,0) node[anchor=north] {$C$};
\draw (b2,0.0) node[anchor=north] {$E$};
\draw (a1,a2) node[anchor=south east] {$B$};
\draw (f1,f2) node[anchor=south] {$D$};
\end{tikzpicture}

No segmento de reta $[AD]$ está assinalado um ponto $B$.

No segmento de reta $[AE]$ está assinalado um ponto $C$.

O triângulo $[ABC]$ é retângulo em $C$ e $\overline{AC}=a1$ e $\overline{CB}=a2$.


Indique o valor do produto escalar $\overrightarrow{AD} \cdot \overrightarrow{AE}$.

    

%ANSWER

<multiplechoice>

<choice>
$$  \overrightarrow{AD} \cdot \overrightarrow{AE}=c6  $$
</choice>

<choice>
<showone errada1>
<thisone 0>
$$ \overrightarrow{AD} \cdot \overrightarrow{AE}=c7 $$
</thisone>

<thisone 1>
$$ \overrightarrow{AD} \cdot \overrightarrow{AE}=e1 $$
</thisone>
</showone>
</choice>

<choice>
<showone errada2>
<thisone 0>
$$ \overrightarrow{AD} \cdot \overrightarrow{AE}=c8 $$
</thisone>

<thisone 1>
$$ \overrightarrow{AD} \cdot \overrightarrow{AE}=e2 $$
</thisone>
</showone>
</choice>

<choice>
<showone errada3>
<thisone 0>
$$ \overrightarrow{AD} \cdot \overrightarrow{AE}=c9 $$
</thisone>

<thisone 1>
$$ \overrightarrow{AD} \cdot \overrightarrow{AE}=e3 $$
</thisone>
</showone>
</choice>

</multiplechoice>


Resolução:
Por definição de produto escalar, sabe-se que
$$ \overrightarrow{AD} \cdot \overrightarrow{AE}=||\overrightarrow{AD}|| \, ||\overrightarrow{AE}|| \, \cos\alpha,$$
em que $\alpha$ é o ângulo formado pelos dois vetores.<p>
Uma vez que é dada a norma de cada um dos vetores, é necessária a determinação do valor de $\cos\alpha$ para posterior cálculo do produto escalar.<p>
Num triângulo retângulo, o cosseno de um ângulo agudo pode ser determinado pela razão entre a medida do cateto que lhe é adjacente e a medida da hipotenusa. Sendo $[ABC]$ um triângulo retângulo, para $\alpha=\angle CAB$, tem-se que $\displaystyle \cos \alpha =\frac{\overline{AC}}{\overline{AB}}$.<p> Determine-se, aplicando o Teorema de Pitágoras, $\overline{AB}$:
    $$\overline{AB}^2=\overline{AC}^2+\overline{BC}^2=a1^2+a2^2= c3.$$
Sendo $\overline{AB}$ a medida do segmento de reta $[AB]$, tem-se que $\overline{AB}=\sqrt{c3}=c4$.<p>

Pode, agora, determinar-se o valor de $\cos\alpha$:
    $$\cos\alpha=\frac{a1}{c4}=c5.$$
Assim,


\begin{eqnarray*}
    \overrightarrow{AD} \cdot \overrightarrow{AE}&=& ||\overrightarrow{AD}|| \,||\overrightarrow{AE}|| \, \cos\alpha \\
                                           &=& b1 \times b2\times c5 \\
                                           &=& c6. \\
\end{eqnarray*} 

A resposta correta é assim $\displaystyle c6$.




class E97G40_produto_escalar2_R2_008(Exercise):
   
    def make_random(s):
        
        s.a1=ur.iunif(1,5)
        s.a2=ur.iunif(1,5)
                            
            
    def solve(s):
        
        s.c1=s.a1^2
        s.c2=s.a2^2
        s.c3=s.c1+s.c2
        s.c4=sqrt(s.c3)
        s.c5=s.a1/s.c4
        s.g1=s.a1+1
        s.g2=round((s.c4+1),0)
        s.b1=ur.iunif(s.g2,8)
        s.b2=ur.iunif(s.g1,8)
        s.c6=s.b1*s.b2*s.c5
        s.c7=s.b1*s.b2*s.a2/s.c4
        s.c8=s.b1*s.b2*s.a1/s.a2
        s.c9=s.b1*s.b2*s.a2/s.a1
        s.f1=round((s.b1*s.a1/s.c4),50)
        s.f2=round((s.b1*s.a2/s.c4),50)
        s.f3=max(s.f1,s.b2)+0.5
        s.f4=max(s.f2+0.5,s.a2+0.5)    
        s.e1=s.b1*s.b2*s.a1/s.a2
        s.e2=s.b1*s.b2/s.a2
        s.e3=s.b1+s.b2
        
        #Escolhas múltiplas  
        s.errada1=0
        if (s.a1==s.a2):
            s.errada1=1
        s.errada2=0
        if (s.a1==s.a2):
            s.errada2=1
        s.errada3=0
        if (s.a1==s.a2):
            s.errada3=1
        if (s.a2==1):
            s.e2=s.c6*2
        
''')



meg.save(r'''

%SUMMARY Exercício Descritivo

uma soma

Palavras chave: Produto escalar

Autor: Ana Palmeira, 2014


%PROBLEM Exercício Descritivo


Calcule: $a1 + a2 = $    

%ANSWER

$a1 + a2 = res$   pois ....


class E97G40_soma_001(Exercise):
   
    def make_random(s):
        
        s.a1=ur.iunif(1,5)
        s.a2=ur.iunif(1,5)
                            
            
    def solve(s):
        
        s.res=s.a1 + s.a2
        
''')




# =================================================
# Documento em LaTeX (exame, caderno de exercícios)
# =================================================

# ficheiro principal

ltdoc = r''' 

\documentclass{article}

\usepackage{amsfonts}

\usepackage{tikz}
\usetikzlibrary{arrows}

\usepackage[utf8]{inputenc}

\begin{document}


\noindent\textbf{Exercício 1}

{{put_here("E34A30_FatorIntegrante_002", ekey=20)}}

\noindent\textbf{Exercício 2}

{{put_here("E97G40_produto_escalar2_R2_008",ekey=10)}}

\noindent\textbf{Exercício 3}

{{put_here("E97G40_soma_001",ekey=10)}}

\end{document}

'''


# formato de cada exercício

exercisetemplate=r'''

{{problem}}

Resposta:

{{answer}}

'''

# Gera o documento em LaTeX
#'''

meg.latex_document(ltdoc,exercisetemplate=exercisetemplate)
#meg.latex_document(ltdoc) #get standard exercise template




# ===========================
# Documento em LaTeX para AMC
# ===========================

meg.amc(["E34A30_FatorIntegrante_002",10,"E97G40_produto_escalar2_R2_008",20])

