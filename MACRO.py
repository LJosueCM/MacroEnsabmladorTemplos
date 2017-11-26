#Modulo para obtener los parametros de la consola y terminar el programa
#Tiene el enlace con el traductor
import sys

#Funcion que busca conincidencias con la palabra MACRO y MEND
def Ver_Macro(linea):
	#Se busca en la linea si está escrita la palabra MACRO
	for i in range(0, len(linea)-5):
		if linea[i:i+5] == "MACRO":
			print("Coincidencia con MACRO")
			return 1

	#Se busca si en la linea se ha escrito un MEND
	for i in range(0,len(linea)-4):
		if linea[i:i+4] == "MEND":
			print("Coincidencia con MEND")
			return 2

#Comprobación de el ingreso de el archivo de entrada
if len(sys.argv) == 2:
	#Se ttrata la excepcion si no existe el archivo
	try:
		#Apertura del archivo
		archivo_e = open(sys.argv[1],"r")
	except OSError:
		print(">>Archivo no existente")
		sys.exit(0)

	#Se lee cada linea en el archivo
	for linea in archivo_e:
		#Se manda esa linea a que se revise
		op=Ver_Macro(linea)

	#Cierre del archivo
	archivo_e.close()
else:
	#Mensaje de error si no se ingresa el archivo
	if len(sys.argv) < 2:
		print(">>Error\n>>Faltan parametros")
	#Mensaje de error si se ingresan más cosas
	else:
		print(">>Error\n>>Parametros erroneos")