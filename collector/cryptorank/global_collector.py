import requests
import json
from datetime import datetime
import os
from os.path import expanduser

print('Cryptorank global collector begin!')

url = 'https://api.cryptorank.io/v1/global'
key = open(expanduser('~')+'/.zeno/cryptorank_api_key.txt').read()[0:-1]
params={'api_key':key}
print('key',key)

r = requests.get(url = url, params = params)
jdata = json.loads(r.text)

folder = './collector/cryptorank/global'
if not os.path.isdir(folder): os.makedirs(folder)

fname = folder + '/' + datetime.today().strftime('%Y-%m-%d') + '.json'
with open(fname, 'w') as f: json.dump(jdata,f)

print('All done. The fetched data path is: ' + fname)
