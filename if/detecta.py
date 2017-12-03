#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
palabra_end="END"
palabra = "IF"
palabra_v="TRUE:"
palabra_f="FALSE:"
#cuanos if hay, se permite solo uno
repetidas = 0
#cuantos TRUE hay, se permite solo uno
rep_true = 0
#cuantos FALSE hay, se permite solo uno
rep_false = 0
rep_end = 0

f = open("file.txt","r")
lines = f.readlines()
for line in lines:
	#se busca if en el archivo
    palabras = line.split()
    for p in palabras:
        if p==palabra:
            repetidas = repetidas+1
#No encontro if
if repetidas==0:
	print "No hay if, el programa puede seguir"
	sys.exit()
#encontro if
else:
	repetidas=0
	for line in lines:
		palabras = line.split()
		#busca true
		for t in palabras:
			if t==palabra_v:
				print palabras
				rep_true = rep_true+1
				if rep_true==1:
					#busca la posición de true (j)
					for j in range(0,len(palabras)):
						if(palabras[j] == palabra_v):
							print"posocion de true"
							print j
							#se busca equ
							x=palabras[j+1]
							if x=='EQU':
								z=palabras[j+2]
								print z
								#z almacena el -1 o 0 del true
							else:
								print"Error, no se ha igualado el TRUE"
								sys.exit()
				if repetidas>1:
					print 'Error, no puede haber trues anidados'
					sys.exit()
		#busca false
		for f in palabras:
			if f==palabra_f:
				print palabras
				rep_false = rep_false+1
				if rep_false==1:
					#busca la posición de false (l)
					for l in range(0,len(palabras)):
						if(palabras[l] == palabra_f):
							print "posicion del false"
							print l
							#se busca equ
							a=palabras[l+1]
							if a=='EQU':
								w=palabras[l+2]
								print "palabra despues de equ en false, valor del f"
								print w
								#w almacena el -1 o 0 del true
							else:
								print"Error, no se ha igualado el FALSE"
								sys.exit()
				if rep_false>1:
					print 'Error, no puede haber trues anidados'
					sys.exit()
		#busca if
		for p in palabras:
			if p==palabra:
				print palabras
				repetidas = repetidas+1
				if repetidas==1:
					#busca la posición de if (i)
					for i in range(0,len(palabras)):
						if(palabras[i] == palabra):
							print "posicion del if"
							print i
							y=palabras[i+1]
							print "Lo siguiente tiene que ser not, si es band, hay que verificar que se haya declarado antes"
							print y
							if y=='NOT':
								b=palabras[i+2]
								#verificamos que la variable a comparar se haya definido
								
							else:
								print'No hay not, puede ser band y hay que verificar que se haya declarado'
				if rep_false>1:
					print 'Error, no puede haber "if" anidados'
					sys.exit()
		for e in palabras:
			if e==palabra_end:
				print palabras
				rep_end = rep_end+1
				if rep_end==1:
					#busca la posición de if (i)
					for end in range(0,len(palabras)):
						if(palabras[end] == palabra_end):
							print "posicion del end"
							print end
							fin=palabras[end+1]
							print "Lo siguiente tiene que ser if"
							print fin
							if fin=='IF':
								#elia hernandez labra taza para una doctora
								repetidas=0
								#verificamos que la variable a comparar se haya definido
							else:
								print'No hay not'
				if rep_end>1:
					print 'Error, no puede haber "if" anidados'
					sys.exit()