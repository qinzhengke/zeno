import * as fs from 'fs'
import * as reader from 'read-last-lines'
import sscanf from 'sscanf'

function dumpDiffs(total_diffs){

  var date = new Date()
  var str_month = '' + (date.getUTCMonth()+1)
  if(str_month.length ==1) str_month = '0' + str_month
  var str_day = '' + date.getUTCDate()
  if(str_day.length ==1) str_day = '0' + str_day
  var date_str = date.getUTCFullYear() + str_month + str_day

  var fpath = 'twitter_follows_count_trend-' + date_str + '.csv'
  var head = 'account'
  total_diffs.values().next().value.forEach(function(v,k){
    head += ',df'+k+',rdf'+k+',ddf'+k
  })
  fs.appendFile(fpath, head, function(err){ if(err) throw err })

  total_diffs.forEach(function(value,key){

  	var line = '\n'+ key
	value.forEach(function(v,k){
	    line += ',' + v.df + ',' + v.rdf.toFixed(4) + ',' + v.ddf
	})
	  console.log(line)
        fs.appendFile(fpath, line, function(err){ if(err) throw err })
  })

  fs.copyFileSync(fpath, '/root/gdrive/'+fpath)
}

export async function analyze(folder){
    var fpaths = fs.readdirSync(folder)
    var accounts = []
    fpaths.forEach(function(f,i){accounts.push(f.split('.')[0])})
    fpaths.forEach(function(f,i){ fpaths[i] = folder + '/' + f})

    console.log(fpaths)

    var steps = [1,3,7,15]
    var n = Math.max(...steps) + 2
    let total_diffs = new Map()
    for(var i=0; i<fpaths.length; i++){
        var str = await reader.read(fpaths[i],n+1)
        var lines = str.split('\n')
        lines.shift()
        lines.reverse();
        var cnts = new Array(n)
        console.log(lines)
        var pad = 0
        for(var j=0; j<n; j++){
            if(j<lines.length){
                cnts[j] = sscanf(lines[j], '%s,%d')[1]
                pad = cnts[j]
            }
            else{
                cnts[j] = pad
            }
        }

        let diffs = new Map()
        for(var d of steps) diffs.set(d,{df:NaN,rdf:NaN,ddf:NaN})

        var y = cnts[0]
        diffs.forEach(function(diff, step){
            var yd = cnts[step]
            diff.df = y - yd
            diff.rdf = diff.df / yd
            var y1 = cnts[1]
            var yd1 = cnts[step+1]
            diff.ddf = y - yd - (y1 - yd1)
        })

        total_diffs.set(accounts[i], diffs)

    }
    console.log(total_diffs)

    dumpDiffs(total_diffs)

}
