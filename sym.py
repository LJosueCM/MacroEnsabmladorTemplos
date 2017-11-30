import os
import sys
import fileinput
if 'REPT' in file('symME.ASM','r'):
	print 'cadena encontrada'
else:
	print 'cadena no'
for line in fileinput.FileInput('symME.ASM',inplace=1):
  	line = line.replace("#SYM","0000")
   	print line
for line in fileinput.FileInput('symME.ASM',inplace=1):
  	line = line.replace("REPT","AQUI")
   	print line