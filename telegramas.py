# -*- coding: utf-8 -*-
"""
descargar telegramas
"""

path_mesas_totales = 'original_data/MesasPresidente.csv'

import csv
import requests
from time import sleep
import os

c = 0
with open(path_mesas_totales, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    first = True
    ssleep = 4.0
    for row in reader:
        if first:
            first=False
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
        c += 1
        if not os.path.isfile(fname):
            print "GETTING %s" % url
            try:
                req = requests.get(url, timeout=10.1)
            except Exception, e:
                print "Error %s" % str(e)
                ssleep = 4
                continue
            ssleep = 0.3 if ssleep <= 1.0 else ssleep - 0.5
            myfile = open(fname, "w")
            myfile.write(req.content)
            myfile.close()
            print "sleep %d %.2f" % (c, ssleep)
            sleep(ssleep)
        else:
            print "ALREADY %s" % url
        
        
