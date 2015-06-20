# -*- coding: utf-8 -*-

from megua.all import *
meg = MegBook('amc.sqlite')

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


Indique o valor do produto escalar $\overrightarrow{AD} \centerdot \overrightarrow{AE}$.

    

%ANSWER

<multiplechoice>

<choice>
$$  \overrightarrow{AD} \centerdot \overrightarrow{AE}=c6  $$
</choice>

<choice>
<showone errada1>
<thisone 0>
$$ \overrightarrow{AD} \centerdot \overrightarrow{AE}=c7 $$
</thisone>

<thisone 1>
$$ \overrightarrow{AD} \centerdot \overrightarrow{AE}=e1 $$
</thisone>
</showone>
</choice>

<choice>
<showone errada2>
<thisone 0>
$$ \overrightarrow{AD} \centerdot \overrightarrow{AE}=c8 $$
</thisone>

<thisone 1>
$$ \overrightarrow{AD} \centerdot \overrightarrow{AE}=e2 $$
</thisone>
</showone>
</choice>

<choice>
<showone errada3>
<thisone 0>
$$ \overrightarrow{AD} \centerdot \overrightarrow{AE}=c9 $$
</thisone>

<thisone 1>
$$ \overrightarrow{AD} \centerdot \overrightarrow{AE}=e3 $$
</thisone>
</showone>
</choice>

</multiplechoice>


Resolução:
Por definição de produto escalar, sabe-se que
$$ \overrightarrow{AD} \centerdot \overrightarrow{AE}=||\overrightarrow{AD}|| \, ||\overrightarrow{AE}|| \, \cos\alpha,$$
em que $\alpha$ é o ângulo formado pelos dois vetores.<p>
Uma vez que é dada a norma de cada um dos vetores, é necessária a determinação do valor de $\cos\alpha$ para posterior cálculo do produto escalar.<p>
Num triângulo retângulo, o cosseno de um ângulo agudo pode ser determinado pela razão entre a medida do cateto que lhe é adjacente e a medida da hipotenusa. Sendo $[ABC]$ um triângulo retângulo, para $\alpha=\angle CAB$, tem-se que $\displaystyle \cos \alpha =\frac{\overline{AC}}{\overline{AB}}$.<p> Determine-se, aplicando o Teorema de Pitágoras, $\overline{AB}$:
    $$\overline{AB}^2=\overline{AC}^2+\overline{BC}^2=a1^2+a2^2= c3.$$
Sendo $\overline{AB}$ a medida do segmento de reta $[AB]$, tem-se que $\overline{AB}=\sqrt{c3}=c4$.<p>

Pode, agora, determinar-se o valor de $\cos\alpha$:
    $$\cos\alpha=\frac{a1}{c4}=c5.$$
Assim,


\begin{eqnarray*}
    \overrightarrow{AD} \centerdot \overrightarrow{AE}&=& ||\overrightarrow{AD}|| \,||\overrightarrow{AE}|| \, \cos\alpha \\
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



