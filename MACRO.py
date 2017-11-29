#Modulo para obtener los parametros de la consola y terminar el programa
#Tiene el enlace con el traductor
import sys
#Importamos el modulo donde esta la segunda pasada
import SP
#Para acceder a funcionalidades dependientes del sisteme operativo
import os
#Variable que guarda donde inicia la palabra MACRO
pos_macro = 0
#Contador que guarda las lineas del que hay en em MDT
cont_MDT = 0
#Contador de la cantidad de lineas en MNT
cont_MNT = 1
#Contador de los elementos de la tabla ALA
cont_ALA = 1
#Guarda donde empiezan los argumentos de la macro que se este leyendo
cont_ALA_i = 0
#Se crea un diccionario para los argumentos
dic_arg = {}
#Bandera que sirve para ver si se ha declarado una macro
enaux = 0
#Listas donde se van a guardar la información de las tablas temporalmente
lista_ALA = []
lista_MDT = []
lista_MNT =[]

#Funcion que busca conincidencias con la palabra MACRO y MEND
def Ver_Macro(linea):
	#Declaracion de la variable global para utilizarla
	global pos_macro
	global enaux
    
	#Se busca en la linea si está escrita la palabra MACRO
	encont = linea.find("MACRO")
	#Si find regresa un -1 es que no está en la linea
	if encont != -1:
		pos_macro = encont
		#Marcamos la bandera de que se encontró MACRO
		enaux=1
		#Regresamos la opcion para decir que encontramos la palabra MACRO
		return 1
	
	#Se busca si en la linea se ha escrito un MEND
	encont = linea.find("MEND")
	#Si find regresa un -1 es que no está en la linea
	if encont != -1:
<<<<<<< HEAD
		return 2
	else:
		if enaux==1: 
			print("ERROR: MEND no declarada")
		else: 
=======
		#Se verifica que antes se haya declarado MEND
		if enaux != 1:  
>>>>>>> fe32d71a834a3d61cd0f3d4a54aecc37be074d87
			print("ERROR: MACRO no declarada")
<<<<<<< HEAD
			#Se manda un -1 que significa un error
			return -1
		#Se pone la bandera en cero si se encontro el MEND
=======
			enaux=0
			sys.exit(0)

>>>>>>> f7eb4ddee3d84aa24ddad5783bcb624f9a320b29
		enaux = 0
		#Se regresa la opcion de encontrado MEND
		return 2
    
#Función que cambia las referencias de los argumentos
def BusqALA(linea):
	#Se hace global para que se pueda ocupar en la funcion
	global dic_arg
	global lista_ALA
	#Se verifica en que posicion se encuentra el primer #
	pos = linea.find("#")
	#Si hay argumentos en la linea se continua
	if pos != -1:		#Se corta la cadena hasta donde estan las referencias
		linea_aux=linea[pos+1:]
		#Se eliminan los simbolos inecesarios
		linea_aux = linea_aux.strip(" ,\t\n")
		linea_aux = linea_aux.replace(" ", "")
		linea_aux = linea_aux.replace(",", "")
		#Se hace una lista de los argumentos que estan en la linea
		arg = linea_aux.split("#")
		#Se revisa todo el documento de ALA para encontrar la referencia
		for i in range(len(lista_ALA)):
			#Cada linea se separa para saber los datos que contiene la tabla
			arr = lista_ALA[i].split("|")
			#Se maneja la excepcion si no se encuentra la cadena en la lista
			try:
				#Buscamos la posicion del argumento en la lista
				op = arg.index(arr[1])
			except ValueError:
				#Si marca excepcion es que no se encuentra y se pasa al siguiente ciclo
				continue
			#Se guarda el valor en el diccionario para usarlo con las demas lineas
			dic_arg[arg[op]] = arr[0]
			#Se remplazan con las referencias
			linea = linea.replace("#"+arg[op], "&"+arr[0])
		#La linea se regresa para que se escriba en el archivo
		return linea

#Funcion que copia la macro en MDT
def CopiarMacro(linea):
	#Se declaran las variables globales para poder utilizarlas en la funcion
	global cont_MDT
	global pos_macro
	global dic_arg
	global archivo_e
	global lista_MDT
	#Se aumenta el contador de linas del documento MDT
	cont_MDT += 1
	#Se mandan los argumentos a la tbala
	Argumentos(linea)
	#Se manda el nombre a la tabla de MNT
	NombMacro(linea)
	#Se pasa la linea por la funcion de busqueda para sustituir # por & y la posicion del arg en la ALA
	linea = BusqALA(linea)
	#Se transforma en cadena el contador para poder escribirla
	aux=str(cont_MDT)
	#Se escribe en la lista auxiliar de MDT
	linea_aux = aux+"|"+linea[pos_macro:]
	lista_MDT.append(linea_aux)
	#Se lee otra linea del archivo
	linea = archivo_e.readline()

	#Verificamos si se encuentra en MEND
	op=Ver_Macro(linea)
	#Se verifica que no haya un error
	if op == -1:
		#Si lo hay manda una señal de error
		return -1

	#Se va a seguir haciendo lo anterior hasta que se encuentre en MEND
	while op != 2:
		cont_MDT += 1
		#Se vuelve cadena el contador para poder concatenar
		aux=str(cont_MDT)
		#Se revisa el diccionarios de los argumentos para esta macro
		for key in dic_arg:
			#Buscamos la llave en la linea
			pos = linea.find("#"+key)
			#Si si está el argumento se continua
			if pos != -1:
				#Se hace el remplazo de la linea
				linea = linea.replace("#"+key, "&"+dic_arg[key])

		#Se escribe en la lista auxiliar de MDT
		linea_aux = aux+"|"+linea
		lista_MDT.append(linea_aux)
		#Se lee la nueva linea
		linea = archivo_e.readline()
		#Verificamos que no sea el fin de archivo
		if not linea:
			#Si es el fin de archivo se rompe el ciclo
			break
		#Se verifica si no en MEND para hacer el otro ciclo
		op=Ver_Macro(linea)
	#Se reinicia el diccionario
	dic_arg={}

#Funcion para crear la tabla MNT		
def NombMacro(linea):
	#Declaracíon para poder utilizar MNT y pos_macro
	global cont_MNT
	global pos_macro
	global cont_ALA_i
	global cont_MDT
	global lista_MNT
	#Se toma la parte de la cadena donde viene el nombre
	linea = linea[0:pos_macro]
	#Se quitan los : y los espacios en blanco
	linea = linea.strip(" :\t")
	linea = linea.replace(" ", "")
	#Se convierte el contador en cadena para poder escribirla
	aux=str(cont_MNT)
	cMDT=str(cont_MDT)
	cALA=str(cont_ALA_i)
	#Se guarda en la lista auxiliar de MNT
	linea_aux=aux+"|"+linea+"|"+cMDT+"|"+cALA
	lista_MNT.append(linea_aux)
	#Aumentamos el contador para la siguiente linea
	cont_MNT += 1

#Funcion que busca los argumentos definidos en una MACRO
def Argumentos(linea):
	#Declaracion del contador para poderlo ocupar en la función
	global cont_ALA
	global cont_ALA_i
	global lista_ALA
	#Al momento de entrar se va a guardar la dir donde inicia los argumentos
	cont_ALA_i = cont_ALA
	#Se busca la posicion donde esta la primera instancia de #
	pos = linea.find("#")
	#Si se encuentra en la cadena se procede
	if pos != -1:
		#Tomamos la parte de la cadena donde estan los argumentso
		linea=linea[pos+1:]
		#Se eliminan todos los simbolos que no se necesitan
		linea = linea.strip(" ,\n\t")
		linea = linea.replace(",", "")
		linea = linea.replace(" ", "")
		#Se separa la cadena cada vez que se encuentre un # y los argumentos se guardan en un arreglo
		arg = linea.split("#")
		#Se revisa todo el arreglo
		for i in range(len(arg)):
			#Cada elemento del arreglo se mete a la lista de argumentos (ALA)
			aux=str(cont_ALA)
			#Su guarda el contenido en la lista ALA
			linea_aux = aux+"|"+arg[i]+"|?"
			lista_ALA.append(linea_aux)
			#Se incrementa las lineas de ALA
			cont_ALA += 1

#Comprobación de el ingreso de el archivo de entrada
if len(sys.argv) == 2:
	#Se busca que la extension sea ASM
	if sys.argv[1].find(".ASM") == -1:
		print(">>ERROR en extensión")
		#Si no es la extension deseada se termina el programa
		sys.exit(0)
	#Se trata la excepcion si no existe el archivo
	try:
		#Apertura del archivo
		archivo_e = open(sys.argv[1],"r")
	except OSError:
		#Se manda un aviso de que el archivo no esta en la carpeta
		print(">>Archivo no existente")
		#Se termina el programa
		sys.exit(0)

	#Archivo que contiene las macro definiciones
	archivo_MDT = open("MDT.txt", "w")
	#Archivo donde esta la tabla con los nombres de las macro definiciones
	archivo_MNT = open("MNT.txt", "w")
	#Se crea el archivo ALA
	archivo_ALA = open("ALA.txt", "w")
	#Se crea un archivo donde se va a guardar el código sin MACROS
	archivo_f = open("MacroEnsamble.ASM", "w")

	#Se lee cada linea en el archivo
	for linea in archivo_e:
		#Se manda esa linea a que se revise para ver si hay definida una MACRO
		op=Ver_Macro(linea)
		#Opcion que indica que se definio una MACRO
		if op == 1:
			#Se trata a la MACRO
			ex = CopiarMacro(linea)
			#Significa que hubo un error dentro de CopiarMacro
			if ex == -1:
				#Se elimina el archivo de salida y se cierra
				archivo_f.close()
				os.remove("MacroEnsamble.ASM")
				sys.exit(0)
		#Opcion que indica que se escribio un MEND sin definir la MACRO
		elif op == 2 and enaux == 0:
			print(">>Error, MACRO no declarada")
			sys.exit(0)
		#Opcion que indica que hubo un error en la funcion Ver_Macro
		elif op == -1:
			#Se elimina el archivo de salida y se cierra
			archivo_f.close()
			os.remove("MacroEnsamble.ASM")
			#Se deja de leer el archivo
			sys.exit(0)
		else:
			#Si no es una Macro se empieza a escribir el programa
			if linea != "\n":
				archivo_f.write(linea)

	#Se verifica si no ha quedado algun MACRO sin cerrar
	if enaux == 1:
		print(">>Error no se encuentra MEND")
		#Se elimina el archivo de salida y se cierra
		archivo_f.close()
		os.remove("MacroEnsamble.ASM")
		sys.exit(0)
	#Se cierra el archivo donde se guarda el programa
	archivo_f.close()
	#Se cierra el archivo de entrada
	archivo_e.close()

	#Llama a la función que empieza la segunda pasada del archivo
	SP.SegundaPasada(lista_ALA, lista_MDT, lista_MNT, sys.argv[1])

	#Cierre de archivos
	archivo_MDT.close()
	archivo_MNT.close()
	archivo_ALA.close()
else:
	#Mensaje de error si no se ingresa el archivo
	if len(sys.argv) < 2:
		print(">>Error\n>>Faltan parametros")
	#Mensaje de error si se ingresan más cosas
	else:
		print(">>Error\n>>Parametros erroneos")