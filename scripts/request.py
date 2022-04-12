import os
import time
import base64
import CBCUtil
import requests
import pyotp
import hashlib

encryption_key = bytes.fromhex('118285f9e6856e1b87806e239bafdcfee7155933adfc7662dae9fe2e7c6a4a73') # extracted from app version 2.5.0
app_code = 'ec46d084-41b7-11e6-99c7-005056a0a452'
user_agent = {
	'User-Agent': 'okhttp/4.8.1'
}

def extract_otp(activation_code):
	# extract seed
	payload = {
		'applicationcode': app_code,
		'activationcode': CBCUtil.encrypt(encryption_key, activation_code),
		'authtoken': CBCUtil.encrypt(encryption_key, str(int(time.time() * 1000)))
	}
	req1 = requests.post('https://mobile.strongauth.it/MobileLicenceServer/webresources/MobileLicenceService/SeedRequest', json=payload, headers=user_agent)
	resp1 = req1.json()

	if (resp1['returncode'] != '0000'):
		raise Exception('Seed request failed: [{}] {}'.format(resp1['returncode'], resp1['description']))

	seed = CBCUtil.decrypt(encryption_key, resp1['seed'])
	seed_b32 = base64.b32encode(base64.b16decode(seed)).decode('utf-8').replace('=', '')

	# validate seed
	payload = {
		'applicationcode': app_code,
		'activationcode': CBCUtil.encrypt(encryption_key, activation_code),
		'authtoken': CBCUtil.encrypt(encryption_key, str(int(time.time() * 1000))),
		'otp1': pyotp.TOTP(base64.b32encode(base64.b16decode(seed)), digits=8, digest=hashlib.sha256, interval=30).now(),
		'otp2': ''
	}
	req2 = requests.post('https://mobile.strongauth.it/MobileLicenceServer/webresources/MobileLicenceService/SeedValidate', json=payload, headers=user_agent)
	resp2 = req2.json()
	
	# print(resp2)
	if (resp2['returncode'] != '0000'):
		raise Exception('Error occured in seed validation: [{}] {}'.format(resp2['returncode'], resp2['description']))
	
	return seed_b32

def write_seed_file(seed):
	with open(os.path.join(os.sys.path[0], 'seed.txt'), 'w') as text_file:
		text_file.write(seed)
		