import requests
import json
from datetime import datetime
import os
from os.path import expanduser

def get_token_names():
    tokens = ''
    f = open(expanduser('~')+'/zeno/projects.json')
    data = json.load(f)
    for i in data:
        if i['token'] != '': tokens += i['token'] + ','

    return tokens[0:-1]

print('Cryptorank basic collector begin!')

token_names = get_token_names()

url = 'https://api.cryptorank.io/v1/currencies'
key = open(expanduser('~')+'/.zeno/cryptorank_api_key.txt').read()[0:-1]
params={'symbols': token_names, 'api_key':key}
print('key',key)

r = requests.get(url = url, params = params)
jdata = json.loads(r.text)

folder = './collector/cryptorank/basic'
if not os.path.isdir(folder): os.makedirs(folder)

fname = folder + '/' + datetime.today().strftime('%Y-%m-%d') + '.json'
with open(fname, 'w') as f: json.dump(jdata,f)

print('All done. The fetched data path is: ' + fname)
