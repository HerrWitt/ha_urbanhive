#!/usr/bin/python3
import requests
import json

res = requests.get('http://192.168.2.154/farm-info')

print(res.text)
j_obj = json.loads(res.text)
print('Wasserstand ',j_obj['productTypeString'])
print('Reihe 1: ',j_obj['rows'][0]['waterLevel'],'%')
print('Reihe 2: ',j_obj['rows'][1]['waterLevel'],'%')
print('Reihe 3: ',j_obj['rows'][2]['waterLevel'],'%')
