#!/usr/bin/python3.12

#
# Import libraries
#
import requests
import json

#
# Get & load data from homefarm
#
res = requests.get('http://192.168.2.154/farm-info')
j_obj = json.loads(res.text)

#
# Display information
#
print('Wasserstand ',j_obj['productTypeString'])
print('Reihe 1: ',j_obj['rows'][0]['waterLevel'],'%')
print('Reihe 2: ',j_obj['rows'][1]['waterLevel'],'%')
print('Reihe 3: ',j_obj['rows'][2]['waterLevel'],'%')
