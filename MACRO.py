#Modulo para obtener los parametros de la consola y terminar el programa
#Tiene el enlace con el traductor
import sys
#Variable que guarda donde inicia la palabra MACRO
pos_macro = 0
#Contador que guarda las lineas del que hay en em MDT
cont_MDT = 0

#Funcion que busca conincidencias con la palabra MACRO y MEND
def Ver_Macro(linea):
	#Declaracion de la variable global para utilizarla
	global pos_macro
	#Se busca en la linea si está escrita la palabra MACRO
	for i in range(0, len(linea)-5):
		if linea[i:i+5] == "MACRO":
			pos_macro = i
			return 1

	#Se busca si en la linea se ha escrito un MEND
	for i in range(0,len(linea)-4):
		if linea[i:i+4] == "MEND":
			return 2

def CopiarMacro(linea,archivo_e,archivo_MDT):
	#Se declaran las variables globales para poder utilizarlas en la funcion
	global cont_MDT
	global pos_macro
	#Se aumenta el contador de linas del documento MDT
	cont_MDT += 1
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
		aux=str(cont_MDT)
		archivo_MDT.write(aux+"|"+linea)
		linea = archivo_e.readline()
		op=Ver_Macro(linea)
		


#Comprobación de el ingreso de el archivo de entrada
if len(sys.argv) == 2:
	#Se ttrata la excepcion si no existe el archivo
	try:
		#Apertura del archivo
		archivo_e = open(sys.argv[1],"r")
	except OSError:
		print(">>Archivo no existente")
		sys.exit(0)

	#Archivo que contiene las macro definiciones
	archivo_MDT = open("MDT.txt", "w")

	#Se lee cada linea en el archivo
	for linea in archivo_e:
		#Se manda esa linea a que se revise
		op=Ver_Macro(linea)
		if op == 1:
			CopiarMacro(linea,archivo_e,archivo_MDT)

	#Cierre de archivos
	archivo_MDT.close()
	archivo_e.close()
else:
	#Mensaje de error si no se ingresa el archivo
	if len(sys.argv) < 2:
		print(">>Error\n>>Faltan parametros")
	#Mensaje de error si se ingresan más cosas
	else:
		print(">>Error\n>>Parametros erroneos")