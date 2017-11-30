#Funcion que busca la macro en la MNT
def Busca(linea, lista_MNT):

	
	for i in range(len(lista_MNT)):
		#Recorre lista_MNT y cada elemento lo separa con un |
		#Guarda los elementos de lista_MNT en otra lista
		arr = lista_MNT[i].split("|")
		#Compara la linea que va leyendo con el segundo elemento
		#del respaldo de lista_MNT
		op = linea.find(arr[1])
		#Si la linea es igual, entonces devuelve el indice

		if op != -1:
			return i
	return -1

#Funcion que actualiza la lista ALA
def Actualiza(linea, lista_ALA, contIni):

	#Se crea una lista auxiliar
	lista_aux = []
	#Se compara la linea el la lista arr y separa sus elementos
	arr = linea.split(",")
	for i in range(len(arr)):
		#Agrega a la lista_aux el elemento de la lista ALA
		#Si encuentra ? lo reemplaza por el elemento de arr
		lista_aux.append(lista_ALA[contIni+i-1].replace("?", arr[i]))
	return lista_aux



def Vacia(lista_aux, lista_MDT, contMDT, archivo_entrada):

	#Crea una lista auxiliar de AL
	aux_ALA = []
	for i in range(len(lista_aux)):
		#Recorre lista_aux y guarda sus elementos en  otra lista
		cadena = lista_aux[i]
		#Agrega los elementos de cadena con la separación | a 
		# la lista aux_ALA
		aux_ALA.append(cadena.split("|"))

	#Separa los elementos de la lista_MDT con un |
	linea = lista_MDT[contMDT]
	linea = linea.split("|")

	#Simulación de un do while
	while True:

		#Se busca a partir de la posición 1 de línea la parabra "MACRO"
		op = linea[1].find("MACRO")
		#Si encontro la palabra retorna un cero 
		if op != -1:
		
		return 0

		#Ciclo desde j hasta terminar de leer aux_ALA 
		for j in range(len(aux_ALA)):

			#A partir de la pocision 1 de la linea busca & concatenado con 
			#el contenido de aux_ALA
			om = linea[1].find("&"+aux_ALA[j][0])

			#Si encontro la coincidencia, reemplazar la linea con aux_ALA y 
			# distintos indices 
			if om != -1:
				linea[1] = linea[1].replace("&"+aux_ALA[j][0], aux_ALA[j][2])

		#Escribe en el archivo de entrada
		archivo_entrada.write(linea[1])
		
		#Aumenta el contador 
		contMDT += 1

		#Si el contador es igual al tamaño de lista_MDT
		# retorna un 0

		if contMDT == len(lista_MDT):
			return 0

		#Separa lista_MDT con un | 

		linea = lista_MDT[contMDT]
		linea = linea.split("|")
			
	return 1

#funcion para escribir en los archivos

def EscribirArch(file, lista, op):

	#Si op es igual a 0 entonces escribe en el archivo el contenido de lista
	if op == 0:
		for i in range(len(lista)):
			file.write(lista[i])
	#si no entonces escribe el contenido de lista concatenado con un salto de linea
	else:
		for i in range(len(lista)):
			file.write(lista[i]+"\n")

#Funcion que realiza la segunda pasada del macroensamblador
def SegundaPasada(lista_ALA, lista_MDT, lista_MNT, archivo_original):

	#Se declaran algunas variables
	global pos
	cont = 0
	es = 1

	#En el archivo original se rempleza "." por "ME."
	archivo_original = archivo_original.replace(".", "ME.")
	#Se abre en modo lectura el archivio que sera de salida
	archivo_salida = open("MacroEnsamble.ASM", "r")
	#Se abre en modo de escritura el archivo original 
	archivo_entrada = open(archivo_original, "w")
	#Simulacion de un do while
	while True:
		#Lee linea por linea el archivo de salida 
		linea = archivo_salida.readline()
		if not linea:
			break
		#Llama a la funcion Busca, con sus parametros correspondientes 
		op = Busca(linea, lista_MNT)

		#Si op es distinto de -1:
		if op != -1:
			#Separa los elementos de arr con un |
			arr = lista_MNT[op].split("|")
			#Se sustituye la posicion de arr 1 por "" 
			linea_aux = linea.replace(arr[1], "")
			#Elimina el los saltos de linea y los tabuladores de la lista 
			linea_aux = linea_aux.strip("\n\t")
			#Reemplaza los espacios
			linea_aux = linea_aux.replace(" ", "")
			#Llama a la funcion Actualiza 
			lista_aux = Actualiza(linea_aux, lista_ALA, int(arr[3]))
			#Llama a la funcion vacia
			es = Vacia(lista_aux, lista_MDT, int(arr[2]), archivo_entrada)
		
		#Si la variable es distinta de cero, escribe la linea en el archivo de entrada
		if es != 0: 
			archivo_entrada.write(linea)

		#Inicia de nuevo con uno la variable. 
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
	return 