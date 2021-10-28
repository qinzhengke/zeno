import * as fs from 'fs'
import * as reader from 'read-last-lines'
import sscanf from 'sscanf'

function getDateStr(){
  var date = new Date()
  var str_month = '' + (date.getUTCMonth()+1)
  if(str_month.length ==1) str_month = '0' + str_month
  var str_day = '' + date.getUTCDate()
  if(str_day.length ==1) str_day = '0' + str_day
  return date.getUTCFullYear() + str_month + str_day
}

function getNumStr(num){
  if(num > 1000000){
    return (num/1000000).toFixed(2) + 'M'
  }
  else if(num > 1000){
    return (num/1000).toFixed(2) + 'K'
  }
  else return '' + num
}

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
  fs.writeFile(fpath, head, function(err){ if(err) throw err })

  total_diffs.forEach(function(value,key){

  	var line = '\n'+ key
	value.forEach(function(v,k){
	    line += ',' + v.df + ',' + v.rdf.toFixed(4) + ',' + v.ddf
	})
	  console.log(line)
        fs.appendFile(fpath, line, function(err){ if(err) throw err })
  })
}

function sortDiffs(diffs,step,type){

  if(type == 'rdf'){
    return new Map([...diffs.entries()].sort((a, b) => b[1].get(step).rdf - a[1].get(step).rdf));
  }
  else if(type == 'ddf'){
    return new Map([...diffs.entries()].sort((a, b) => b[1].get(step).ddf - a[1].get(step).ddf));
  }
  else{	// 'df' and all others.
    return new Map([...diffs.entries()].sort((a, b) => b[1].get(step).df - a[1].get(step).df));
  }
}

function dumpDiffsForShare(fpath, total_diffs, title){

  var line = 'Date: ' + getDateStr()
  fs.writeFileSync(fpath, line, function(err){ if(err) throw err })
  line = '\n\n' + title
  fs.appendFileSync(fpath, line, function(err){ if(err) throw err })
  var head = '\n\n' + 'rank ' + 'account'.padEnd(20)
  total_diffs.values().next().value.forEach(function(v,k){
    if([1,3].includes(k)){
      head += (k + ' day inc').padEnd(14) + (k + ' day rel inc').padEnd(16)
    }
  })
  console.log(head)
  fs.appendFileSync(fpath, head+'\n', function(err){ if(err) throw err })

  var i = 0
  total_diffs.forEach(function(value,key){
    if(i < 20){
      line = '\n' + (''+(i+1)+'.').padEnd(5) + key.padEnd(20)
      value.forEach(function(v,k){
          if([1,3].includes(k)){
            line += (''+v.df).padEnd(14) + (''+(v.rdf*100).toFixed(2)+'%').padEnd(16)
          }
      })
      console.log(line)
      fs.appendFileSync(fpath, line, function(err){ if(err) throw err })
      i++
    }
  })
}

export async function analyze(folder){
    var fpaths = fs.readdirSync(folder)
    var accounts = []
    fpaths.forEach(function(f,i){ accounts.push(f.split('.')[0])})
    fpaths.forEach(function(f,i){ fpaths[i] = folder + '/' + f})

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

    var date_str = getDateStr()

    var df1_diffs = sortDiffs(total_diffs, 1, 'df')
    var fpath = date_str + '-tfc_trend_share-df1.txt'
    var title = 'Twitter followers increasement, sorted by 1 day inc.'
    dumpDiffsForShare(fpath, df1_diffs, title)

    var rdf1_diffs = sortDiffs(total_diffs, 1, 'rdf')
    fpath = date_str + '-tfc_trend_share-rdf1.txt'
    title = 'Twitter followers increasement, sorted by 1 day relative inc.'
    dumpDiffsForShare(fpath, rdf1_diffs, title)

}
