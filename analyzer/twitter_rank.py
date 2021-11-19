import os,sys
sys.path.append('.')
from twitter_loader import load_twitter_data

def print_rank(data):
    s = ''
    s += 'rank  account             '
    for d in data[0]['dfs']: s += ('df' + str(d['df'])).ljust(20)
    s += '\n' + '-'*100 + '\n'
    for r,val in enumerate(data):
        s += (str(r+1)+'.').ljust(6) + val['account'].ljust(20)
        for d in val['dfs']:
            num = '%.2fk'%(float(d['val'])/1000.0)
            s += (num.ljust(7) + '(%.2f%%)'%(d['rval']*100)).ljust(20)
        s += '\n'

    return s

src,date = load_twitter_data()

dfs = [1, 3, 7, 15]
dst = []
for key,val in src.items():
    item = {}
    y = [a[1]['public_metrics']['followers_count'] for a in val]
    item['account'] = key
    N = len(y)
    ldfs = []
    for d in dfs:
        v = y[N-1] - y[N-1-d] if N-1-d >= 0  else 0
        rv = v / y[N-1-d] if N-1-d >=0 else 0
        ldfs.append({'df':d,'val':v, 'rval':rv})
    item['dfs'] = ldfs

    dst.append(item)

s = ''
s += 'This is daily twitter info report about crypto.\n'
s +=  'Date: %s\n'%date
for i,d in enumerate(dfs):
    dst.sort(key=lambda x:x['dfs'][i]['rval'], reverse=True)
    s += '='*100 + '\n'
    s += 'Sorted by relative increasement of %d days. \n'%d
    s += print_rank(dst[0:20])
    s += '\n'

for i,d in enumerate(dfs):
    dst.sort(key=lambda x:x['dfs'][i]['val'], reverse=True)
    s += '='*100 + '\n'
    s += 'Sorted by absolute increasement of %d days. \n'%d
    s += print_rank(dst[0:20])
    s += '\n'

folder = os.environ['ZENO_OUTPUT_DIR']+'/analyzer/twitter'
if not os.path.isdir(folder): os.makedirs(folder)
fpath = folder + '/' + date + '.txt'
fp = open(fpath,'w')
fp.write(s)

print('All done! The result file is %s'%fpath)
