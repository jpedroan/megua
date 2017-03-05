

Guia Rápido
===========

Apresentamos um guia para as etapas principais da construção de um exercício `parametrizado <http://www.priberam.pt/dlpo/parametrizado>`_.


Fase teórica e criativa
-----------------------

Começar com a **ideia apelativa** do exercício que motivam os **conceitos teóricos** escolhidos. Propomos as seguintes etapas:

1. Escrever o problema e seus parâmetros.
2. Escrever de imediato a resolução completa baseada nos parâmetros definidos no problema.
3. Só depois as opções de escolha múltipla (se estiver a escrever para a web).

A criação de exercícios baseados em parâmetros aleatórios tem que ter em conta aspetos que não são contemplados:

**Valores "apropriados"**

Os valores que o estudante irá ver no problema devem ser "apropriados":

* Valores muito grandes e que obriguem a contas demoradas não são em geral boa escolha pois desejamos a atenção seja focada no conceito e não nos números que vão ocorrer.
* Por vezes ocorre o contrário: um estudante habitua-se a derivar apenas $x^2$ ou $x^3$. Há registo de estudantes que não souberam responder se lhe pedirmos a derivada de $x^{1000}$.
* Por vezes a ocorrência de $e$ (número de Euler, ou Nepper) ou $\sqrt{2}$, embora sejam números, pode representar um problema dependendo do nível a que o problema é colocado.


**Prever todas as situações**

Tem que se prever todas as situações pois os parâmetros são gerados aleatoriamente. 
É fácil ver que se o cálculo da resolução envolver um passo $a/b$ então temos que impedir que $b$ seja zero. 
Por outras palavras, há que gerir os domínios das sucessivas transformações ocorridas numa resolução. Esta escolha faz com que
o domínio dos valores que ocorrem no problema deve ser bem pensada.

*Pense ao contrário*: para ter um certo tipo de solução final "amigável" e resolução "suave", de que domínios se devem escolher valores para 
os parâmetros do enunciado.



Fase da implementação
---------------------

Após a etapa teórica, vem a criação de um novo exercício no servidor.
Pretende-se nesta fase escrever o texto em LaTeX e HTML e codificar as regras de cálculo dos parâmetros na linguagem Python.

A melhor abordagem é a construção passo a passo. Começar só com um parâmetro e pouco texto e logo de seguida ver se funciona. Depois ir adicionando as várias situações. 
Espera-se deste modo capturar melhor situações de erro que são parte normal de quem usa uma linguagem de programação ou descrição.


1. Aceda ao site `megua.org <http://www.megua.org>`_ e faça *login*; usar o chrome ou firefox preferencialmente; se é docente e pretende um login contacte `Pedro Cruz <http://www.ua.pt/dmat/pageperson.aspx?id=1183>`_.
2. Abrir um qualquer exercício que já exista na sua conta e que servirá de modelo a um novo.
3. Faça ``File Copy Worksheet``.
4. Mude o nome (com *click* no nome). Se é aluno de mestrado a sugestão do nome é ``Mestrado:meuprimeironome_areadoexercicio_001`` para um primeiro exercício.
5. Faça ``share`` (botão no canto superior direito) com os utilizadores do projeto em que está.

Depois, o texto deve ser alterado nestes passos:

1. Alterar secções em ``%summary ....``, escrever um sumário do que é o exercício e catalogar (ver abaixo).
2. Criar problema (e seus parâmetros) em ``%problem <nome sugestivo não técnico para o estudante>``. Este nome deve ser curto. Por exmeplo, se o exercícios menciona o transporte de azeitonas então o exercício pode chamar-se "Azeitonas".
3. Criar resolução completa (e seus parâmetros) em ``%answer``. 
4. Alterar nome do exercício usando um formato análogo a ``class E97H60_determinantes_001`` em que 97H60 deve ser escolhido da MSC (ver `abaixo <msc>`_).

Em `Exercícios para a web <paraweb>`_ encontra-se um exercício completo e explicado bem como outras opções.
Em `Python/Sage <pythonsection>`_ encontra-se um guia para a programação de valores.



.. msc:

Mathematics Subject Classification
----------------------------------

Os exercícios devem ser catalogados com o sistema de classificação para a matemática conhecido por 
*Mathematics Subject Classification* (MSC2010). Pode usar-se mais que uma área mas uma delas deverá ser a principal.

Para a criação de material educativo é normal que a principal área pertença a esta classe::

  97-XX Mathematics education

dentro da qual se encontram os domínios principais para os quais se pretendem desenvolver exercícios:

* consulte as subáreas `97-XX <http://msc2010.org/mscwiki/index.php?title=97-XX>`_;
* a classificação completa em `msc2010.org <http://msc2010.org/mscwiki/index.php?title=MSC2010>`_.




