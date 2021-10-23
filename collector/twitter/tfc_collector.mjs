import { getWatchAccounts } from './account_manager.mjs'
import fetch from 'node-fetch'
import * as fs from 'fs'

async function getFollowersCnt(accounts){
  var url = 'https://api.twitter.com/2/users/by?usernames='
  // console.log(accounts.length)
  for(var i=0; i<accounts.length; i++){
    url += accounts[i]
    if(i != accounts.length-1) url += ','
  }
  url += '&user.fields=public_metrics'

  console.log(url)

  // var options = {};
  // options.headers = {
  // };

  var cnts = []
  const response = await fetch(url, {
        // method: 'POST',
        method: 'GET',
        headers: {
            "Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAAGu6UgEAAAAA03qrh%2FrpV7EXMm%2BRAJY6c8%2BdDBU%3DoCF477cyj6U1SSbXW2ROrNIbCCEYmYXzS5sBsuoMidkBJcDK2t"
        }
    })

  const jdata = await response.json()
  console.log(jdata)
  for(var i=0; i<accounts.length; i++) cnts.push(jdata['data'][i]['public_metrics']['followers_count'])

  return cnts
}

export async function fetchFollowersData(){
  console.log('fetchFollowersData()')
    // var now = Utilities.formatDate(new Date(), "GMT+1", "yyyy/MM/dd")

  var date = new Date()
  var date_str = date.getUTCFullYear() + '/' + (date.getUTCMonth()+1) + '/' + date.getUTCDate() 

  var accounts = getWatchAccounts()

  // console.log(accounts)

  var batch = 10
  var cnts = []
  for(var beg=0; beg<accounts.length; beg+=batch){
    var end = beg + batch
    if(end > accounts.length) end = accounts.length

    var sub_accounts = []
    for(var i=beg; i<end; i++) sub_accounts.push(accounts[i])

    var sub_cnts = await getFollowersCnt(sub_accounts)
    // Utilities.sleep(500)

    for(var i=0; i<sub_cnts.length; i++) cnts.push(sub_cnts[i])

  }
  console.log(accounts)
  console.log(cnts)

  var folder = 'twitter_follower_count'
  if(!fs.existsSync(folder)) fs.mkdirSync(folder)

  var new_file_cnt = 0
  for(var i=0; i<accounts.length; i++){
    var fpath = folder + '/' + accounts[i] + '.csv'
    if(!fs.existsSync(fpath)){
      console.log('TFC file not exist, create now: ' + fpath)
      fs.appendFile(fpath, 'date,count', function(err){ if(err) throw err })
      new_file_cnt ++
    }
    fs.appendFile(fpath, '\n' + date_str+','+cnts[i], function(err){ if(err) throw err })
  }

  console.log('TFC updated! ' + accounts.length + ' accounts updated, ' + new_file_cnt + ' new accounts created! }')
}