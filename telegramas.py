# -*- coding: utf-8 -*-
"""
descargar telegramas
Permite usar multiples veces con un offset y un to.
Con esto se puede usar varias veces simultaneamente
El script iterara las veces necesarias hasta que todo se descargue
sin errores (timeouts)
"""

path_mesas_totales = 'original_data/MesasPresidente.csv'

import csv
import requests
from time import sleep
import os
import sys

offset = 0
to = 1000000
for arg in sys.argv:
    if arg.startswith('--offset'):
        offset = int(arg.split('=')[1])
        print "offset %d" % offset

if arg.startswith('--to'):
        to = int(arg.split('=')[1])
        print "to %d" % to

errores = 1 # inicial
while errores > 0:
    errores = 0
    c = 0
    with open(path_mesas_totales, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        first = True
        ssleep = 4.0
        for row in reader:
            if first:
                first=False
                continue
            c += 1
            if c < offset:
                continue
            if c > to:
                continue
            provincia = row[0].strip()
            depto = row[1].strip()
            circuito = row[2].strip()
            muni = row[3].strip()
            mesa = row[4].strip()
            
            # descargar telegrama
            # sample          http://www.resultados.gob.ar/bltgetelegr/22/008/0071/220080071_1182.pdf
            # algunos (?) son http://www.resultados.gob.ar/bltgetelegr/16/007/0031A/160070031A0324.pdf
            # supongo que si el circuito es largo evitan el ultimo "_"
            if len(circuito) == 4:
                url = "http://www.resultados.gob.ar/bltgetelegr/{0}/{1}/{2}/{0}{1}{2}_{3}.pdf".format(provincia, depto, circuito, mesa)
            elif len(circuito) == 5:
                url = "http://www.resultados.gob.ar/bltgetelegr/{0}/{1}/{2}/{0}{1}{2}{3}.pdf".format(provincia, depto, circuito, mesa)
                
            fname = "telegramas/{0}_{1}_{2}_{3}.pdf".format(provincia, depto, circuito, mesa)
            
            if not os.path.isfile(fname):
                print "%d GETTING %s (%.2f) %d errores" % (c, url, ssleep, errores)
                try:
                    req = requests.get(url, timeout=16.0)
                except Exception, e:
                    print "Error %s" % str(e)
                    ssleep = 4
                    errores += 1
                    sleep(4)
                    continue
                ssleep = 0.3 if ssleep <= 1.0 else ssleep - 0.5
                myfile = open(fname, "w")
                myfile.write(req.content)
                myfile.close()
                sleep(ssleep)
            # else:
            #     print "ALREADY %s" % url

    print " ########### "
    print " ########### "
    print " ERRORES %d" % errores
    print " ########### "
    print " ########### "
            
        
