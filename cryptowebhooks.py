import urllib, json, pickle, time, requests

#init this for the first time the script runs
#it will save some data to a file for permanent storage
permdata_filename = "bitcointrackerdata"
#permdata = [100]
#permdata[0] is the previous total number of btc txs
#fileObject = open(permdata_filename,'wb') 
#pickle.dump(permdata,fileObject)   
#fileObject.close()

#use blockchain.info API for bitcoin transaction history
#bitcoin_url = "https://blockchain.info/rawaddr/1HB5XMLmzFVj8ALj6mfBsbifRoD4miY36v"
#wikileaks donation address for testing

#add actual bitcoin wallet address for incoming donations here
bitcoin_url = "https://blockchain.info/rawaddr/YOURADDRESSHERE"
response = urllib.urlopen(bitcoin_url)
data = json.loads(response.read())

fileObject = open(permdata_filename,'r')  
permdata = pickle.load(fileObject)
fileObject.close()

#get number of total transactions
curtxs=data["n_tx"]
#see if there is a difference between total transactions since the last time we checked
txdiff=curtxs-permdata[0]
permdata[0]=curtxs

listtest = data["txs"]

output=""
#get the n latest transactions, where n the latest transactions since we last checked
#this will work for up to 50 new txs due to API limitations
for n in range(0,txdiff):
	i=listtest[n]
	timestamp=i["time"]
	
	#unix epoch timestamp
	datetime=str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp)))
	amount=0
	for out in i["out"]:
		#only account for incoming txs to this address
		#so dont show spending as donations
		if out["addr"]==data["address"]:
			amount+=out["value"]
			
	if amount>0:
		output+="@adrian New bitcoin donation on " + datetime+"\nAmount: " + str(amount*0.00001) + "mBTC. Thanks!\n\n"

#incoming webhooks for mattermost
chaturl = 'https://chat.lambdaspace.gr/hooks/ADDWEBHOOKURL'
#add the correct url here
payload = {"channel": "bot-testing","username": "cryptocoinbot", "text": output}
r = requests.post(chaturl, data=json.dumps(payload))

#save current total transactions to file
fileObject = open(permdata_filename,'wb') 
pickle.dump(permdata,fileObject)   
fileObject.close()
