
readme
======

1. Esta pasta tem exemplos para teste das novas funções em megbook.py e ex.py (mais algum?)

2. A base de dados é reconstruida com build_db.sage

3. A fazer:

(a) desenvolver/terminar/testar o meg.amc(....)  sendo meg=MegBook.

(b) criar meg.latex("base-de-da-dos.sqlite","nome-do-exercicio") sendo meg=megbookweb
que criar um ficheiro HTML com o aspeto:

  meg.save(r"""

  <aqui, todo o exercício em html>
 
  """)

para que o autor possa copiar/colar no worksheet do megbook, e depois, possar usar no amc.


Análise de casos
----------------

2a. questões fixas, questões tiradas dum saco, questões com parâmetros aleatórios

2b. opções baralhadas vs opções sempre o mesmo sítio

2c. questões baralhadas na página

2d. O docente escolhe as chaves ou elas são escolhidas automaticamente


LaTeX (sem AMC)
---------------

--> editor de exames LaTeX incorporado no megua, imitando o AMC.

código:
* MegBook.put_here
* MegBook.template_fromstring
* MegBook.template_fromfile
* MegBook.template_create

a fazer:

* criar exemplos para o tutorial.

* Valerá a pena usar tudo do AMC?
* {{ copy_here(...) }}
    - {{ copy_here(["ex1",10,"ex2",20], reps=100) }} #100 student exams
    - {{ copy_here(["ex1","ex2"], ekeys=[10,20], reps=100) }} #100 student exams
    - será que o jinja2 tolera strings grandes? Averiguar.
    - opções tipo AMC:
        - os parâmetros são sempre os mesmos e as 4 opções são baralhadas
        - os parâmetros variam e as 4 opções são baralhadas
        - a posição das questões é trocada

* alterar o código para encaixar o <multiplechoice>:
   * num futuro modelo do megua: esta questão deve ser tomada em conta:
        * explicação (um memo) de porquê da opção falsa
        * registo de dificuldade proposto e observado estatísticamente.
* permitir geração de chaves à sorte (no put_here ?)
* documentar
* alterar os nomes das funções "template_....."
* meg.html2latex(base-de-dados,nome-do-exercicio) => criar file html
* put_here:
    * mais opções preprogramadas para o output e não tanto deixar o template ao utilizador.

LaTeX (com AMC)
---------------

--> o conteúdo do ficheiro AMC guia a construção do exame com chamadas ao megua.





