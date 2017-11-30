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

#Funcion que realiza la segunda pasada del macroensamblador
def SegundaPasada(lista_ALA, lista_MDT, lista_MNT, archivo_original):
	global pos
	cont = 0
	es = 1
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
			es = Vacia(lista_aux, lista_MDT, int(arr[2]), archivo_entrada)
		
		if es != 0: 
			archivo_entrada.write(linea)

		es = 1


	archivo_salida.close()
	archivo_entrada.close()
	return lista_ALA