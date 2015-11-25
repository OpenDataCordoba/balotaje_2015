# -*- coding: utf-8 -*-

"""
Abrir el archivo con los datos de las mesas y buscar fallas
"""

# un regitro por partido en cada mesa
path_mesas_partidos = 'original_data/MesasCandidaturaPresidente.csv'
# una fila por cada mesa con totales validos, positivos, etc
path_mesas_totales = 'original_data/MesasPresidente.csv'

mesas = {}

import csv
with open(path_mesas_totales, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    first = True
    for row in reader:
        if first:
            first=False
            continue
        provincia = int(row[0].strip())
        depto = int(row[1].strip())
        circuito = row[2].strip()
        muni = int(row[3].strip())
        mesa = int(row[4].strip())
        mesa_id = "{}_{}_{}_{}_{}".format(provincia, depto, muni, circuito, mesa)
        estado = int(row[6].strip())
        validos = int(row[7].strip())
        positivos = int(row[8].strip())
        blancos = int(row[9].strip())
        nulos = int(row[10].strip())
        recurridos = int(row[11].strip())
        impugnados = int(row[12].strip())
        electores = int(row[13].strip())
        votantes = int(row[14].strip())
        
        url = "http://www.resultados.gob.ar/bltgetelegr/{0}/{1}/{2}/{0}{1}{2}_{3}.pdf".format(row[0].strip(), row[1].strip(), row[2].strip(), row[4].strip())
        
        
        mesas[mesa_id] = {"provincia": provincia, 
                            "depto": depto,
                            "circuito": circuito,
                            "muni": muni,
                            "mesa": mesa,
                            "estado": estado, 
                            "validos": validos,
                            "positivos": positivos,
                            "blancos": blancos,
                            "nulos": nulos, 
                            "recurridos": recurridos,
                            "impugnados": impugnados,
                            "electores": electores, 
                            "votantes": votantes,
                            "url": url}
        

with open(path_mesas_partidos, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    first = True
    for row in reader:
        if first:
            first = False
            continue
        provincia = int(row[0].strip())
        depto = int(row[1].strip())
        muni = int(row[2].strip())
        circuito = row[3].strip()
        mesa = int(row[4].strip())
        mesa_id = "{}_{}_{}_{}_{}".format(provincia, depto, muni, circuito, mesa)
        
        partido = int(row[6].strip())
        votos = int(row[8].strip())

        if partido == 131:
            mesas[mesa_id]['FPV'] = votos
        elif partido == 135:
            mesas[mesa_id]['CAMBIEMOS'] = votos

# detectar errores
for k, mesa in mesas.iteritems():
    # mucho porc para alguno de los dos
    pos = 1 if mesa["positivos"] == 0 else mesa["positivos"]
    mesa["porc_fpv"] = round(100 * mesa['FPV'] / pos, 2)
    mesa["porc_cambiemos"] = round(100 * mesa['CAMBIEMOS'] / pos, 2)

    electores = 1 if mesa["electores"] == 0 else mesa["electores"]
    
    mesa["participacion"] = round(100* mesa['votantes'] / electores,2)
    mesa["diferencia_positivos"] = abs(mesa["positivos"] - (mesa['FPV'] + mesa['CAMBIEMOS']))
    mesa["diferencia_validos"] = abs(mesa["validos"] - (mesa["positivos"] + mesa["blancos"]))
    mesa["diferencia_votos"] = abs(mesa["votantes"] - (mesa["positivos"] + mesa["blancos"] + mesa["nulos"] + mesa["recurridos"] + mesa["impugnados"]))
    mesa["diferencia_votantes"] = '' if mesa['electores'] >= mesa['votantes'] else 'mas votantes que electores'
    
    
with open('mesas_final_balotaje_2015.csv', 'w') as csvfile:
    fieldnames = ["provincia", "depto", "circuito", "muni", "mesa", "estado", 
                  "validos", "positivos", "blancos", "nulos", "recurridos", 
                  "impugnados","electores", "votantes", "FPV", "CAMBIEMOS", 
                  "participacion", "porc_cambiemos", "porc_fpv", "diferencia_votos",
                  "diferencia_positivos", "diferencia_validos", "diferencia_votantes", 
                  "url"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for k, mesa in mesas.iteritems():
        writer.writerow(mesa)