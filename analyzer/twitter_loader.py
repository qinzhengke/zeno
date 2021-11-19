import os,re,json,collections

def load_twitter_data():
    root  = os.environ['ZENO_OUTPUT_DIR']+'/collector/twitter/basic'
    raw = []
    for (dir,_,fnames) in os.walk(root):
        p = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{4}\.json')
        fnames = [s for s in fnames if p.match(s)]
        for fn in fnames:
            date = fn[0:10]
            data = json.loads( open(os.path.join(dir,fn)).read() )
            for item in data['data']:
                raw.append([date, item['username'], item])

    out = collections.defaultdict(list)
    for item in raw: out[item[1]].append([item[0],item[2]])
    for _,item in out.items(): item.sort(key = lambda x:x[0])
    return out,item[-1][0]