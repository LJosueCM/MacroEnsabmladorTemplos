#Se importan las funciones del sistema operativo para poder borar archivos
import os
#Funcion que busca la macro en la MNT
def Busca(linea, lista_MNT):
	for i in range(len(lista_MNT)):
		arr = lista_MNT[i].split("|")
		op = linea.find(arr[1])
		if op != -1:
			return i
	return -1

def Actualiza(linea, lista_ALA, contIni):
	lista_aux = []
	arr = linea.split(",")
	for i in range(len(arr)):
		lista_aux.append(lista_ALA[contIni+i-1].replace("?", arr[i]))
	return lista_aux

def Vacia(lista_aux, lista_MDT, contMDT, archivo_entrada):
	aux_ALA = []
	for i in range(len(lista_aux)):
		cadena = lista_aux[i]
		aux_ALA.append(cadena.split("|"))

	linea = lista_MDT[contMDT]
	linea = linea.split("|")
	while True:
		op = linea[1].find("MACRO")
		if op != -1:
			return 0

		op = linea[1].find(":\tMACRO")
		if op != -1:
			print(">> Error: Falta MEND\n")
			return -1 

		for j in range(len(aux_ALA)):
			om = linea[1].find("&"+aux_ALA[j][0])
			if om != -1:
				linea[1] = linea[1].replace("&"+aux_ALA[j][0], aux_ALA[j][2])

		
		archivo_entrada.write(linea[1])
		
		contMDT += 1

		if contMDT == len(lista_MDT):
			return 0

		linea = lista_MDT[contMDT]
		linea = linea.split("|")
			
	return 1

def EscribirArch(file, lista, op):
	if op == 0:
		for i in range(len(lista)):
			file.write(lista[i])
	else:
		for i in range(len(lista)):
			file.write(lista[i]+"\n")

#Funcion que realiza la segunda pasada del macroensamblador
def SegundaPasada(lista_ALA, lista_MDT, lista_MNT, archivo_original):
	global pos
	cont = 0
	es = 1
	archivo_original = archivo_original.replace(".", "ME.")
	nombre = archivo_original
	archivo_salida = open("MacroEnsamble.ASM", "r")
	archivo_entrada = open(archivo_original, "w")
	while True:
		linea = archivo_salida.readline()
		if not linea:
			break
		op = Busca(linea, lista_MNT)
		if op != -1:
			arr = lista_MNT[op].split("|")
			linea_aux = linea.replace(arr[1], "")
			linea_aux = linea_aux.strip("\n\t")
			linea_aux = linea_aux.replace(" ", "")
			lista_aux = Actualiza(linea_aux, lista_ALA, int(arr[3]))
			es = Vacia(lista_aux, lista_MDT, int(arr[2]), archivo_entrada)
		
		if es != 0: 
			archivo_entrada.write(linea)
		elif es == -1:
			archivo_original.close()
			os.remove(nombre)
			archivo_salida.close()
			os.remove("MacroEnsamble.ASM")
			return -1

		es = 1

	#Archivo que contiene las macro definiciones
	archivo_MDT = open("MDT.txt", "w")
	#Archivo donde esta la tabla con los nombres de las macro definiciones
	archivo_MNT = open("MNT.txt", "w")
	#Se crea el archivo ALA
	archivo_ALA = open("ALA.txt", "w")

	EscribirArch(archivo_MDT, lista_MDT, 0)
	EscribirArch(archivo_MNT, lista_MNT, 1)
	EscribirArch(archivo_ALA, lista_ALA, 1)

	#Cierre de archivos
	archivo_salida.close()
	archivo_entrada.close()
	archivo_MDT.close()
	archivo_MNT.close()
	archivo_ALA.close()
	archivo_original.close()
	return 