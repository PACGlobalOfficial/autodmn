#!/usr/bin/python3
from __future__ import print_function
import os, time, requests, json, sys

# autodmn (for pac)
# barrystyle

collateral = 500000

# test for argv
try:
   hostipaddr = sys.argv[1]
except:
   print ('autodmn usage:\n\nautodmn.py3 host-ip-addr:port')
   sys.exit()

class RPCHost(object):
    def __init__(self, url):
        self._session = requests.Session()
        self._url = url
        self._headers = {'content-type': 'application/json'}
    def call(self, rpcMethod, params):
        payload = json.dumps({"method": rpcMethod, "params": params, "jsonrpc": "2.0"})
        try:
           response = self._session.post(self._url, headers=self._headers, data=payload)
           responseJSON = response.json()
           print (str(responseJSON) + '\n')
           return responseJSON['result']
        except:
           return False

def senddaemoncmd(payload,params):
    rpchandler = RPCHost("http://testuser:testpass@127.0.0.1:9998")
    return rpchandler.call(payload,params)

def locatecollateral():
    return senddaemoncmd('masternode',['outputs'])

def getblskey():
    response = senddaemoncmd('bls',['generate'])
    secret = response['secret']
    public = response['public']
    return secret, public

def generateaddresses():
    ownerkeyaddr = senddaemoncmd('getnewaddress',['"ownerkeyaddr"'])
    return ownerkeyaddr

def findfundaddress():
    return senddaemoncmd('listaddressgroupings',[''])

def buildprotx(mnnumber):
    try:
        collat = str(locatecollateral()).split(',')[mnnumber]
        collat_txid = str(collat).split(':')[0].replace('{','').replace('\'','').strip()
        collat_outn = str(collat).split(':')[1].replace('}','').replace('\'','').strip()
    except:
        print ('error finding collateral')
        sys.exit()

    # just go for first input that isnt the collat (for funding)
    fundingaddress = findfundaddress()
    iteminput = ''
    itemamt = ''
    for item in fundingaddress:
        iteminput = (str(item) + '\n').replace('[','').replace(']','').split(',')[0]
        itemamt   = (str(item) + '\n').replace('[','').replace(']','').split(',')[1]
        testamt = int(itemamt.split('.')[0])
        if testamt != collateral:
           break

    fundaddress = iteminput.replace('\'','')
    owneraddr = generateaddresses()
    secret, public = getblskey()
    print ('your BLS private key is '+str(secret))
    params = [
        "register_prepare",
        collat_txid,
        int(collat_outn),
        hostipaddr,
        owneraddr,
        public,
        owneraddr,
        0,
        fundaddress
    ]
    return params

# main func
print ('')

print ('Setting up DIP0003 masternode at '+hostipaddr)

protx_params = buildprotx(0)
protx_response = senddaemoncmd('protx', (protx_params))
protx_message = protx_response['tx']
collateral_addr = protx_response['collateralAddress']
sign_message = protx_response['signMessage']
signed_message = senddaemoncmd('signmessage', [collateral_addr, sign_message])
protx_submit = senddaemoncmd('protx', ['register_submit', protx_message, signed_message])

print (protx_submit)
