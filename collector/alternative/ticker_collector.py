import requests
import json
from datetime import datetime
import os
from os.path import expanduser

print('Ticker from alternative.me collector begin!')

url = 'https://api.alternative.me/v2/ticker/?limit=2000&sort=rank&structure=array'

r = requests.get(url = url)
jdata = json.loads(r.text)

folder = './collector/alternative/ticker'
if not os.path.isdir(folder): os.makedirs(folder)

fname = folder + '/' + datetime.today().strftime('%Y-%m-%d') + '.json'
with open(fname, 'w') as f: json.dump(jdata,f)

print('All done. The fetched data path is: ' + fname)
