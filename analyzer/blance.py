import sys
import json
import collections
import os
import datetime

class AlterTicker:
    def __init__(self,folder):
        self.data = {}
        newest_date = datetime.date(2000,1,1)
        newest_ticker_file = ''
        for (dir,_,fnames) in os.walk(folder):
            for f in fnames:
                f = f[0:len(f)-5]
                d = datetime.datetime.strptime(f,'%Y-%m-%d').date()
                if d > newest_date:
                    newest_date = d
                    newest_ticker_file = dir + '/' + f + '.json'

        jdata = json.loads(open(newest_ticker_file).read())
        for item in jdata['data'] : self.data[item['symbol']] = item

    def get_price(self, token, year=-1, month=-1, day=-1):
        if token == 'CNY'       : return 1.0/6.4
        elif token in self.data : return self.data[token]['quotes']['USD']['price']
        else                    : return 0

class CryptoRankTicker:
    def __init__(self,folder):
        self.data = {}
        self.newest_date = datetime.date(2000,1,1)
        newest_ticker_file = ''
        for (dir,_,fnames) in os.walk(folder):
            for f in fnames:
                f = f[0:len(f)-5]
                d = datetime.datetime.strptime(f,'%Y-%m-%d').date()
                if d > self.newest_date:
                    self.newest_date = d
                    newest_ticker_file = dir + '/' + f + '.json'

        jdata = json.loads(open(newest_ticker_file).read())
        for item in jdata['data']: self.data[item['symbol']] = item

    def get_price(self, token):
        if   token == 'CNY'     : return 1.0/6.4
        elif token == 'USDT'    : return 1.0
        elif token in self.data : return self.data[token]['values']['USD']['price']
        else                    : return 0

    def get_datestr(self):
        return self.newest_date.strftime('%Y-%m-%d')

def load_ledger(folder):
    data = []
    for dir,_,fnames in os.walk(folder+'/trades'):
        for f in fnames:
            jdata = json.loads(open(os.path.join(dir,f)).read())
            data += jdata
    data.sort(key=lambda x:x['date'])
    return data


jdata = load_ledger(sys.argv[1])

data = collections.defaultdict(dict)
data['CNY']['count'] = 0
data['CNY']['fmt'] = ''
data['USDT']['count'] = 0
for item in jdata:
    token = item['buy_token']
    if token in data    : data[token]['count'] += item['buy_count']
    else                : data[token]['count'] = item['buy_count']

    token = item['sell_token']
    if token in data    : data[token]['count'] -= item['sell_count']
    else                : data[token]['count'] = item['sell_count']

ticker_folder = os.environ['ZENO_OUTPUT_DIR']+'/collector/cryptorank/basic'
ticker = CryptoRankTicker(ticker_folder)
for token in data:
    data[token]['val_usd'] = ticker.get_price(token) * data[token]['count']
    data[token]['val_cny'] = ticker.get_price(token) * 6.4 * data[token]['count']
    data[token]['price_usd'] = ticker.get_price(token)

total_token_val_cny = 0
for token in data: total_token_val_cny += data[token]['val_cny'] if token != 'CNY' else 0
for token in data: data[token]['rel_val'] = data[token]['val_cny'] / total_token_val_cny

s = ''

s += 'Date: ' + ticker.get_datestr() + '\n'

profit = total_token_val_cny + data['CNY']['count']
relative_profit = profit / (-data['CNY']['count'])
s += ('Total CNY devote:').ljust(25) + '%.1f'%-data['CNY']['count'] + ' CNY\n'
s += ('Total token values:').ljust(25) + '%.1f'%total_token_val_cny + ' CNY\n'
s += ('Total profit:').ljust(25) + '%.1f'%profit + ' CNY\n'
s += ('Total relative profit:').ljust(25) + '%.1f'%(relative_profit*100.0) + '%\n'

s += '='*200 + '\n'

numlen = 14

# Print token names
s +=  ''.rjust(16)
for token in data: s += token.rjust(numlen)
s += '\n'
s += '-'*200 + '\n'

# Print token counts
s += 'Count'.rjust(16)
for _,token in data.items(): s += ('%.2f'%token['count']).rjust(14)
s += '\n' + '-'*200 + '\n'

# Print real time price
s += 'Price(USDT)'.rjust(16)
for _,token in data.items(): s += ('%.2f'%token['price_usd']).rjust(14)
s += '\n' + '-'*200 + '\n'

# Print token value in USDT
s += 'Value(USDT)'.rjust(16)
for _,token in data.items(): s += ('%.2f'%token['val_usd']).rjust(14)
s += '\n' + '-'*200 + '\n'

# Print token value in CNY
s += 'Value(CNY)'.rjust(16)
for _,token in data.items(): s += ('%.2f'%token['val_cny']).rjust(14)
s += '\n' + '-'*200 + '\n'

# Print token value in CNY
s += 'Relative Value'.rjust(16)
for _,token in data.items(): s += ('%.2f'%(token['rel_val']*100.0)+'%').rjust(14)
s += '\n' + '='*200 + '\n'

for i,item in enumerate(reversed(jdata)):
    s += (str(len(jdata)-i) + '.').ljust(6) + item['date'].rjust(10)
    for token in data:
        if item['buy_token']==token: s += str(item['buy_count']).rjust(numlen)
        elif item['sell_token']==token: s += str(-item['sell_count']).rjust(numlen)
        else: s += ''.rjust(numlen)
    s += '\n'


folder = os.environ['ZENO_OUTPUT_DIR']+'/analyzer/blance'
if not os.path.isdir(folder): os.makedirs(folder)
fpath = folder + '/' + ticker.get_datestr() + '.txt'
fp = open(fpath,'w')
fp.write(s)

 
    