import requests
import json
from datetime import datetime
import os
from os.path import expanduser

def get_twitter_accounts():
    accounts = []
    f = open(expanduser('~')+'/zeno/projects.json')
    data = json.load(f)
    for i in data:
        if i['twitter'] != '': accounts.append(i['twitter'])

    return accounts

print('Twitter basic collector begin!')

accounts = get_twitter_accounts()

key = open(expanduser('~')+'/.zeno/twitter_api_key.txt').read()
key = key[0:-1]
headers = { "Authorization": key }

items = 100
n = len(accounts)
batchs = int(n / items + 1)
for b in range(batchs):
    s = ''
    for c in range(b*items, min((b+1)*items, n)): s += accounts[c] + ','

    s = s[0:-1]
    print('Fetching data for ' + s)

    url = 'https://api.twitter.com/2/users/by?usernames='
    url  += s + '&user.fields=public_metrics'

    res = requests.get(url = url, headers=headers)
    jdata = json.loads(res.text)

    folder = './collector/twitter/basic'
    if not os.path.isdir(folder): os.makedirs(folder)

    fname = folder + '/' + datetime.today().strftime('%Y-%m-%d-') + str(b).zfill(4) + '.json'
    with open(fname, 'w') as f: json.dump(jdata,f)

    print('Batch #{} done. The fetched data path is: {}'.format(b,fname))

print('All done! {} accounts updated, {} json files created!'.format(n, batchs))
