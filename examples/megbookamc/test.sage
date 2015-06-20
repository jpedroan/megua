# -*- coding: utf-8 -*-

from megua.all import *
meg = MegBook('amc.sqlite')

meg.getexercise("E97G40_produto_escalar2_R2_008", ekey=10)

print "Problem"
print meg.getproblem()
print "Answer"
print meg.getproblem()
print "Corret choice"
print meg.getoption(0)
print "Wrong choice 1"
print meg.getoption(1)
print "Wrong choice 2"
print meg.getoption(2)
print "Wrong choice 3"
print meg.getoption(3)

