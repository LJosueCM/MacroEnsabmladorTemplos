import sys
def nombre(linea, lista_MNT, lista_MDT, lista_ALA, aux_ALA, dir_ALA):
	linea = linea.split("|")
	pos = linea[1].find("MACRO")
	linea = linea[1]
	linea = linea[0:pos]
	linea = linea.strip(" :\t")
	linea = linea.replace(" ", "")

	for j in range(len(aux_ALA)):
		om = linea.find("&"+aux_ALA[j][0])
		if om != -1:
			linea = linea.replace("&"+aux_ALA[j][0], aux_ALA[j][2])

	aux=str(len(lista_MNT)+1)
	cMDT=str(len(lista_MDT)+1)
	linea_aux=aux+"|"+linea+"|"+cMDT+"|"+dir_ALA
	lista_MNT.append(linea_aux)

def guardaMACRO(lista_MDT, contMDT):
	linea = lista_MDT[contMDT]
	pos = linea.find("MACRO")
	linea = linea[pos:]
	linea = str(len(lista_MDT)+1)+"|"+linea
	lista_MDT.append(linea)
	contMDT += 1
	linea = lista_MDT[contMDT]

	while True:
		op = linea.find("MACRO")
		if op != -1:
			break
			
		arr = lista_MDT[contMDT].split("|")
		arr[0] = len(lista_MDT)
		linea = str(arr[0]+1)+"|"+arr[1]
		lista_MDT.append(linea)
		contMDT += 1
		linea = lista_MDT[contMDT]

	return lista_MDT

def MAnidadas(lista_MDT, lista_MNT, lista_ALA, contMDT, aux_ALA, dir_ALA):
	linea = lista_MDT[contMDT]
	nombre(linea, lista_MNT, lista_MDT, lista_ALA, aux_ALA, dir_ALA)
	guardaMACRO(lista_MDT, contMDT)

	return