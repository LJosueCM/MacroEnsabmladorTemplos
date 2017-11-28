#Modulo para obtener los parametros de la consola y terminar el programa
#Tiene el enlace con el traductor
import sys
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

encontaux=0

#Funcion que busca conincidencias con la palabra MACRO y MEND
def Ver_Macro(linea):
	#Declaracion de la variable global para utilizarla
	global pos_macro
    
    


	#Se busca en la linea si está escrita la palabra MACRO
	encont = linea.find("MACRO")
	#Si find regresa un -1 es que no está en la linea
	if encont != -1:
		pos_macro = encont
		return 1
    else: 
        encontaux=linea.find("MEND")
        if encontaux ==-1: 
            print(">>ERROR: MACRO no encontrada")

	#Se busca si en la linea se ha escrito un MEND
	encont = linea.find("MEND")
	#Si find regresa un -1 es que no está en la linea
	if encont != -1:
		return 2
    

#Función que cambia las referencias de los argumentos
def BusqALA(linea):
	#Se hace global para que se pueda ocupar en la funcion
	global dic_arg
	global archivo_ALA
	#Se verifica en que posicion se encuentra el primer #
	pos = linea.find("#")
	#Si hay argumentos en la linea se continua
	if pos != -1:
		#Se corta la cadena hasta donde estan las referencias
		linea_aux=linea[pos+1:]
		#Se eliminan los simbolos inecesarios
		linea_aux = linea_aux.replace(" ", "")
		linea_aux = linea_aux.replace("\t", "")
		linea_aux = linea_aux.replace("\n", "")
		linea_aux = linea_aux.replace(",", "")
		#Se hace una lista de los argumentos que estan en la linea
		arg = linea_aux.split("#")
		#Se revisa todo el documento de ALA para encontrar la referencia
		for line_ALA in archivo_ALA:
			#Cada linea se separa para saber los datos que contiene la tabla
			arr = line_ALA.split("|")
			#Se maneja la excepcion si no se encuentra la cadena en la lista
			try:
				#Buscamos la posicion del argumento en la lista
				op = arg.index(arr[1])
			except ValueError:
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
	global archivo_MDT
	global archivo_MNT
	global archivo_ALA
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
	#Se escribe en MDT
	archivo_MDT.write(aux+"|"+linea[pos_macro:])
	#Se lee otra linea del archivo
	linea = archivo_e.readline()

	#Verificamos si se encuentra en MEND
	op=Ver_Macro(linea)
	
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

		#Se escribe en el archivo
		archivo_MDT.write(aux+"|"+linea)
		#Se lee la nueva linea
		linea = archivo_e.readline()
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
	global archivo_MNT
	#Se toma la parte de la cadena donde viene el nombre
	linea = linea[0:pos_macro]
	#Se quitan los : y los espacios en blanco
	linea = linea.replace(" ", "")
	linea = linea.replace(":", "")
	linea = linea.replace("\t", "")
	#SE convierte el contador en cadena para poder escribirla
	aux=str(cont_MNT)
	cMDT=str(cont_MDT)
	cALA=str(cont_ALA_i)
	#Se escribe la macro en la tabla
	archivo_MNT.write(aux+"|"+linea+"|"+cMDT+"|"+cALA+"\n")
	#Aumentamos el contador para la siguiente linea
	cont_MNT += 1

def Argumentos(linea):
	#Declaracion del contador para poderlo ocupar en la función
	global cont_ALA
	global cont_ALA_i
	global archivo_ALA
	#Al momento de entrar se va a guardar la dir donde inicia los argumentos
	cont_ALA_i = cont_ALA
	#Se busca la posicion donde esta la primera instancia de #
	pos = linea.find("#")
	#Si se encuentra en la cadena se procede
	if pos != -1:
		#Tomamos la parte de la cadena donde estan los argumentso
		linea=linea[pos+1:]
		#Se eliminan todos los simbolos que no se necesitan
		linea = linea.replace(" ", "")
		linea = linea.replace("\n", "")
		linea = linea.replace("\t", "")
		linea = linea.replace(",", "")
		#Se separa la cadena cada vez que se encuentre un # y los argumentos se guardan en un arreglo
		arg = linea.split("#")
		#Se revisa todo el arreglo
		for i in range(len(arg)):
			#Cada elemento del arreglo se mete a la lista de argumentos (ALA)
			aux=str(cont_ALA)
			archivo_ALA.write(aux+"|"+arg[i]+"|\n")
			cont_ALA += 1
	#Regresamos el puntero del archivo al inicio 
	archivo_ALA.seek(0)

#Comprobación de el ingreso de el archivo de entrada
if len(sys.argv) == 2:
	if sys.argv[1].find(".ASM")==-1:
		print(">>ERROR en extensión")
		sys.exit(0)
	#Se ttrata la excepcion si no existe el archivo
	try:
		#Apertura del archivo
		archivo_e = open(sys.argv[1],"r")
	except OSError:
		print(">>Archivo no existente")
		sys.exit(0)

	#Archivo que contiene las macro definiciones
	archivo_MDT = open("MDT.txt", "w")
	#Archivo donde esta la tabla con los nombres de las macro definiciones
	archivo_MNT = open("MNT.txt", "w")
	#Se crea el archivo ALA
	archivo_ALA = open("ALA.txt", "w")
	archivo_ALA.close()
	#Se hace para poder manejar el archivo de escritura y de lectura
	archivo_ALA = open("ALA.txt", "r+")

	#Se lee cada linea en el archivo
	for linea in archivo_e:
		#Se manda esa linea a que se revise
		op=Ver_Macro(linea)
		if op == 1:
			CopiarMacro(linea)

	#Cierre de archivos
	archivo_MDT.close()
	archivo_MNT.close()
	archivo_ALA.close()
	archivo_e.close()
else:
	#Mensaje de error si no se ingresa el archivo
	if len(sys.argv) < 2:
		print(">>Error\n>>Faltan parametros")
	#Mensaje de error si se ingresan más cosas
	else:
		print(">>Error\n>>Parametros erroneos")