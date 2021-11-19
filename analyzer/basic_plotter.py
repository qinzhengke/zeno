from typing import Collection
from matplotlib import pyplot as plt
from os.path import expanduser
import os,sys
import datetime as dt
import matplotlib.dates as mdates
sys.path.append('.')
from twitter_loader import load_twitter_data

def plot(tdata,incs):
    output_dir = os.environ['ZENO_OUTPUT_DIR']+'/analyzer/basic_plotter'
    if not os.path.isdir(output_dir): os.makedirs(output_dir)
    for key,val in tdata.items():
        print('Ploting ' + key)
        dates = [ a[0] for a in val ]
        x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
        y = [a[1]['public_metrics']['followers_count'] for a in val]
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('time')
        ax1.set_ylabel('tfc')
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        line, = ax1.plot(x,y,color='cyan',marker='.')
        line.set_label('twitter followers count')
        ax1.legend()

        ax2 = ax1.twinx()
        ax2.set_ylabel('inc(%)')
        assert(key in incs)
        x = incs[key]['dates']
        for i in incs[key]['dfs']:
            y = i['rdy']
            assert(len(x)==len(y))
            line, = ax2.plot(x,y,marker='x')
            line.set_label('%d day inc'%i['df'])
        ax2.legend()
        plt.gcf().autofmt_xdate()
        plt.title('Twitter Followers of ' + key)
        fig.savefig(output_dir+'/'+key+'.png')

tdata,_ = load_twitter_data()

dfs = [1, 3, 7, 15]
incs = {}
for key,val in tdata.items():
    dates = [ dt.datetime.strptime(a[0],'%Y-%m-%d') for a in val ]
    item = {}
    y = [a[1]['public_metrics']['followers_count'] for a in val]
    item['dates'] = dates
    N = len(y)
    ldfs = []
    for d in dfs:
        dy = []
        rdy = []
        for K in range(N):
            v = y[K] - y[K-d] if K-d >= 0  else 0
            rv = 100.0 * v / y[K-d] if K-d >=0 else 0
            dy.append(v)
            rdy.append(rv)
        ldfs.append({'df':d,'dy':dy, 'rdy':rdy})
    item['dfs'] = ldfs

    incs[key] = item

plot(tdata,incs)