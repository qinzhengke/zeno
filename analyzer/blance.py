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

def print_summary(data):

    profit = total_token_val_cny + data['CNY']['count']
    relative_profit = profit / (-data['CNY']['count']) * 100
    s = '<table border=1px>'
    s += '<tr><td align="right">Date</td><td>%s</td></tr>'%ticker.get_datestr()
    s += '<tr><td align="right">Total CNY devote (CNY)</td>'
    s += '<td align="right">%.1f</td></tr>'%data['CNY']['count']
    s += '<tr><td align="right">Total token values (CNY)</td>'
    s += '<td align="right">%.1f</td></tr>'%total_token_val_cny
    s += '<tr><td align="right">Total profit (CNY)</td>'
    s += '<td align="right">%.1f</td></tr>'%profit
    s += '<tr><td align="right">Total relative profit</td>'
    s += '<td align="right">%.1f%%</td></tr>'%relative_profit

    s += '</table>'
    return s

def print_token_summary(data):

    s = '<table border=1px>'

    numlen = 14

    s += '<tr><td>'
    for token in data: s += '<td align="center" style="width:80px">%s</td>'%token
    s += '</tr>'

    s += '<tr><td>Count</td>'
    for _,token in data.items(): s += '<td align="right">%.2f</td>'%token['count']
    s += '</tr><tr>'

    s += '<tr><td>Price(USD)</td>'
    for _,token in data.items(): s += '<td align="right">%.2f</td>'%token['price_usd']
    s += '</tr><tr>'

    s += '<tr><td>Value(USD)</td>'
    for _,token in data.items(): s += '<td align="right">%.2f</td>'%token['val_usd']
    s += '</tr><tr>'

    s += '<tr><td>Value(CNY)</td>'
    for _,token in data.items(): s += '<td align="right">%.2f</td>'%token['val_cny']
    s += '</tr><tr>'

    s += '<tr><td>Relative Value</td>'
    for _,token in data.items(): s += '<td align="right">%.2f%%</td>'%(token['rel_val']*100.0)
    s += '</tr><tr>'

    s += '</table>'
    return s

def print_trade_history(raw,data):

    s = '<table border=1px>'
    s += '<tr><td>No.</td><td style="width:100px">Date</td><td>Exchange</td><td>Price</td>'
    for token in data: s += '<td style="width:80px">%s</td>'%token
    s += '</tr>'

    for i,item in enumerate(reversed(raw)):
        s += '<tr><td align="right">%d</td>'%(len(raw)-i)
        s += '<td>%s</td>'%item['date']
        s += '<td>%s</td>'%item['exchange']
        s += '<td align="right">%.2f</td>'%(item['sell_count']/item['buy_count'])
        for token in data:
            if item['buy_token']==token: s += '<td align="right">%.2f</td>'%item['buy_count']
            elif item['sell_token']==token: s += '<td align="right">%.2f</td>'%(-item['sell_count'])
            else: s += '<td></td>'
        s += '</tr>'
    s += '</table>'
    return s

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
for key,value in data.items():
    value['val_usd'] = ticker.get_price(key) * value['count']
    value['val_cny'] = ticker.get_price(key) * 6.4 * value['count']
    value['price_usd'] = ticker.get_price(key)

total_token_val_cny = 0
for key,value in data.items(): total_token_val_cny += value['val_cny'] if key != 'CNY' else 0
for key,value in data.items(): value['rel_val'] = value['val_cny'] / total_token_val_cny
for key,value in data.items():
    if key == 'CNY': value['sort_key'] = 1e9-1
    elif key == 'USDT': value['sort_key'] = 1e9-2
    else: value['sort_key'] = value['rel_val']

data = {k: v for k, v in sorted(data.items(), key=lambda x:x[1]['sort_key'], reverse=True)}

s = '<html><body>'

s += '<p align="center">Tab 1. Total summary %s</p>'%print_summary(data)

s += '<p align="center">Tab 2. Token summary %s</p>'%print_token_summary(data)

s += '<p align="center">Tab 3. Trading history %s</p>'%print_trade_history(jdata,data)

s += '</body></html>'

folder = os.environ['ZENO_OUTPUT_DIR']+'/analyzer/blance'
if not os.path.isdir(folder): os.makedirs(folder)
fpath = folder + '/' + ticker.get_datestr() + '.html'
fp = open(fpath,'w')
fp.write(s)

 
    