#Se importan las funciones del sistema operativo para poder borrar archivos
import os
#Biblioteca de manejo del sistema
import sys
#También se importa el modulo que hrealiza las macron anidadas
import Anidadas

#Listas que contienen las tablas ALA, MNT y MDT
lista_ALA = []
lista_MNT = []
lista_MDT = []
#Variable global que contiene la dirección donde inician los argumentos en el ALA y donde termina
dir_ALA = ""
dir_ALA_fin = ""
#Contador de Macros anidadas
ANI = 0
#Arreglo donde se guardará la lista del ALA para la macro anidada de la principal 
aux_anterior = []

#Funcion que busca la macro en la MNT
def Busca(linea):
	#Variables globales que ocupa la función
	global lista_MNT
	global dir_ALA
	global dir_ALA_fin

	#Se lee cada renglon de la tabla MNT
	for i in range(len(lista_MNT)):
		#El renglon se separa para que cada elemento esté en un elemento del arreglo
		arr = lista_MNT[i].split("|")
		#Se verifica que el nombre de la macro del renglon de la MNT este en la linea
		op = linea.find(arr[1])
		#Si arroja -1 es que no se encuentra en la linea
		if op != -1:
			#Si es la macro que se necesita se guarda la dir de inicio de sus argumentos
			dir_ALA = arr[3]
			#Se separa la siguiente fila para ver donde inicia si no es la ultima
			if i != len(lista_MNT)-1:
				arr = lista_MNT[i+1].split("|")
				#Será el final de los argumentos de la macro en la tabla ALA
				dir_ALA_fin = arr[3]
			#Si es la ultima sólo se guarda el tamaño del arreglo
			else:
				dir_ALA_fin = str(len(lista_ALA)+1)
			#Se regresa la posición del renglon de la MNT
			return i
	#Ya que no hay ninguna macro en la linea se regresa un -1
	return -1

#Función que arroja una lista ALA con argumentos actuales
def Actualiza(linea, contIni, archivo_entrada):
	#Variables globales que necesita la función
	global lista_ALA
	global aux_anterior
	global dir_ALA_fin
	global dir_ALA
	#Lista auxiliar donde se guardará los argumentos de la ALA ya modificados sin alterar la principal
	lista_aux = []
	#Si no hay ningún anidamiento
	if ANI == 0:
		#Se guardan en un arreglo los parametros actuales de la macro
		arr = linea.split(",")
		tam = int(dir_ALA_fin) - int(dir_ALA)
		#Se verifica que no haya mas argumentos de los que acepta la macro
		if len(arr) > tam:
			print("Error: Demasiados argumentos")
			print("Linea: "+linea)
			#Se termina el programa
			sys.exit(0)
		#Se verifica que no se hayan puesto menos argumentos de los que necesita la macro
		elif len(arr) < tam:
			print("Error: Faltan argumentos")
			print("Linea: "+linea)
			#Se termina el programa
			sys.exit(0)
		#Por cada parámetro de la macro
		for i in range(len(arr)):
			#Se guarda el renglon ya modificado
			lista_aux.append(lista_ALA[contIni+i-1].replace("?", arr[i]))
		#Se guarda la lista por si se necesita para una macro anidada 
		aux_anterior = lista_aux
	#Si es una macro anidada la lista que se ocupará para los argumentos sera la anterior
	else: 
		lista_aux = aux_anterior
	#Se regresa la lista auxiliar de ALA con los parametros cambiados
	return lista_aux

#Función que escribe en el documento el contenido de la macro
def Vacia(lista_aux, contMDT, archivo_entrada):
	#Variables globales que ocupa la función
	global lista_MDT
	global lista_ALA
	global lista_MNT
	global dir_ALA
	global ANI

	#Matriz que contendrá parte de la tabla ALA
	aux_ALA = []
	#Se recorrera el tamño de la lista que arroja la función actualiza
	for i in range(len(lista_aux)):
		#Se lee cada renglos de la lista auxiliar de ALA y se le asigna a otra variable
		cadena = lista_aux[i]
		#Esa otra variable se separa en tokens y se agrega a la matriz que forma ahora la tabla 
		aux_ALA.append(cadena.split("|"))

	#Se lee el renglon en la MDT donde está el inicio de la macro y se separa en numero de linea y contenido	
	linea = lista_MDT[contMDT]
	linea = linea.split("|")

	#Cico infinito hasta cierta condición
	while True:
		#Se busca si hay una Macro anidada
		op = linea[1].find(":\tMACRO")
		#Si la hay...
		if op != -1:
			#Se marac la bandera de anidamiento como encendida
			ANI = 1
			#Se trata la anidación en la macro
			Anidadas.MAnidadas(lista_MDT, lista_MNT, lista_ALA, contMDT, aux_ALA, dir_ALA)
		
		#Se busca donde empieza la siguiente macro
		op = linea[1].find("MACRO")
		#Al encontrarla se regresa a la funcion principal del modulo
		if op != -1:
			return 0

		#Si no se encuentra se van a cambiar las lineas por los argumentos actuales
		for j in range(len(aux_ALA)):
			#Se busca el argumento en la linea
			om = linea[1].find("&"+aux_ALA[j][0])
			#Se se encuentra ese argumento se remplaza
			if om != -1:
				linea[1] = linea[1].replace("&"+aux_ALA[j][0], aux_ALA[j][2])

		#Se escribe la linea en el archivo
		archivo_entrada.write(linea[1])
		#Se sigue con la otra linea de MDT
		contMDT += 1
		#Si llegamos al final se acaba
		if contMDT == len(lista_MDT):
			return 0
		#Si no se actualiza la linea
		linea = lista_MDT[contMDT]
		linea = linea.split("|")
		#Y se pone la bandera de anidada en 0
		ANI = 0
	#Se regresa un 1 si lo que se leyo no es una macro
	return 1

#Función que escribe las tablas ALA, MDT y MNT en archivos 
def EscribirArch(file, lista, op):
	#SE pone en su archivo la lista MDT
	if op == 0:
		for i in range(len(lista)):
			file.write(lista[i])
	#Se escriben en sus archivos las lista MNT y ALA
	else:
		for i in range(len(lista)):
			file.write(lista[i]+"\n")

#Funcion que realiza la segunda pasada del macroensamblador
def SegundaPasada(l_ALA, l_MDT, l_MNT, archivo_original):
	#Variables globales que se necesitan
	global lista_ALA
	global lista_MDT
	global lista_MNT
	global archivo_entrada
	#Inicializacion de la variable es
	es = 1
	#Listas que contienen las tablas
	lista_ALA = l_ALA
	lista_MNT = l_MNT
	lista_MDT = l_MDT

	#Se abre el archivo donde se escribirá el programa macroensamblado
	archivo_original = archivo_original.replace(".", "ME.")
	#Se guarda el nombre del archivo
	nombre = archivo_original
	#Se abre el archivo auxiliar donde esta el programa sin macrodefiniciones
	archivo_salida = open("MacroEnsamble.ASM", "r")
	#Se abre el archivo de salida  
	archivo_entrada = open(archivo_original, "w")
	#Mientras sea verdadero
	while True:
		#Se lee una linea del archivo auxiliar
		linea = archivo_salida.readline()
		#Si ya no hay linea se termina el ciclo
		if not linea:
			break
		#Se busca si en la linea hay una macrollamada
		op = Busca(linea)
		#si si la encuentra...
		if op != -1:
			#Se busca la referencia de la macro en la MNT
			arr = lista_MNT[op].split("|")
			linea_aux = linea.replace(arr[1], "")
			linea_aux = linea_aux.strip("\n\t")
			linea_aux = linea_aux.replace(" ", "")
			#Si en la dir de ALA hay un -1 no hay tabla de ALA
			if arr[3] != "-1":
				#Se obtiene una lista de la ALA con los argumentos ya remplazados
				lista_aux = Actualiza(linea_aux, int(arr[3]), archivo_entrada)
				#Se escribe el contenido de la macro en el archivo
				es = Vacia(lista_aux, int(arr[2]), archivo_entrada)
			else:
				#Vaciamos el archivo sin argumentos
				es = Vacia([], int(arr[2]), archivo_entrada)
		
		#Si es tiene un valor diferente de 0 (1) se escribe tal cual
		if es != 0: 
			archivo_entrada.write(linea)
		#Si es -1 hubo un error  y se remueve el archivo
		elif es == -1:
			archivo_original.close()
			os.remove(nombre)
			archivo_salida.close()
			os.remove("MacroEnsamble.ASM")
			return -1
		#Se vuelve a poner la var es en su valor	
		es = 1

	#Archivo que contiene las macro definiciones
	archivo_MDT = open("MDT.txt", "w")
	#Archivo donde esta la tabla con los nombres de las macro definiciones
	archivo_MNT = open("MNT.txt", "w")
	#Se crea el archivo ALA
	archivo_ALA = open("ALA.txt", "w")

	#Se escriben los archivos ALA, MNT y MDT
	EscribirArch(archivo_MDT, lista_MDT, 0)
	EscribirArch(archivo_MNT, lista_MNT, 1)
	EscribirArch(archivo_ALA, lista_ALA, 1)

	#Cierre de archivos
	archivo_salida.close()
	archivo_entrada.close()
	archivo_MDT.close()
	archivo_MNT.close()
	archivo_ALA.close()
	#Se retresa a el main principal
	return 