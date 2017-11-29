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
	linea = lista_MDT[contMDT]
	#op = linea.find("MACRO")
	#print(linea)
	#print(op)
	#while op != -1:
	#	print(linea)
	#	contMDT += 1
	#	linea = lista_MDT[contMDT]
	#	op = linea.find("MACRO")
	#	if op != -1:
	#		return

	#archivo_salida.write("Hola")
	return

#Funcion que realiza la segunda pasada del macroensamblador
def SegundaPasada(lista_ALA, lista_MDT, lista_MNT, archivo_original):
	global pos
	cont = 0
	archivo_original = archivo_original.replace(".", "ME.")
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
			Vacia(lista_aux, lista_MDT, int(arr[2])-1, archivo_entrada)
		archivo_entrada.write(linea)


	archivo_salida.close()
	archivo_entrada.close()
	return lista_ALA