import json
import os
import time
import base64
import CBCUtil
import requests
import pyotp
import hashlib

encryption_key = bytes.fromhex('118285f9e6856e1b87806e239bafdcfee7155933adfc7662dae9fe2e7c6a4a73') # extracted from app version 2.5.0
app_code = 'ec46d084-41b7-11e6-99c7-005056a0a452'
req_headers = {
	'User-Agent': 'okhttp/4.8.1'
}

def request_otp(activation_code):
	# extract seed
	payload = {
		'applicationcode': app_code,
		'activationcode': CBCUtil.encrypt(encryption_key, activation_code),
		'authtoken': CBCUtil.encrypt(encryption_key, str(int(time.time() * 1000)))
	}
	req1 = requests.post('https://mobile.strongauth.it/MobileLicenceServer/webresources/MobileLicenceService/SeedRequest', json=payload, headers=req_headers)
	resp1 = req1.json()

	if (resp1['returncode'] != '0000'):
		raise Exception('Seed request failed: [{}] {}'.format(resp1['returncode'], resp1['description']))

	seed = CBCUtil.decrypt(encryption_key, resp1['seed'])
	seed_b32 = base64.b32encode(base64.b16decode(seed)).decode('utf-8').replace('=', '')

	otp_type = resp1['tokentype']
	digits = resp1['digit']
	period = resp1['stepsize']
	counter = int(CBCUtil.decrypt(encryption_key, resp1['counter']))
	algo = ''

	# validate seed
	payload = {
		'applicationcode': app_code,
		'activationcode': CBCUtil.encrypt(encryption_key, activation_code),
		'authtoken': CBCUtil.encrypt(encryption_key, str(int(time.time() * 1000))),
		'otp1': '',
		'otp2': ''
	}
	if (otp_type == 'TOTP'):
		algo = 'SHA256'
		payload['otp1'] = pyotp.TOTP(seed_b32, digits=digits, digest=hashlib.sha256, interval=period/1000).now()
	elif (otp_type == 'HOTP'):
		algo = 'SHA1'
		payload['otp1'] = pyotp.HOTP(seed_b32, digits=digits, digest=hashlib.sha1, initial_count=counter).at(0)
		payload['otp2'] = pyotp.HOTP(seed_b32, digits=digits, digest=hashlib.sha1, initial_count=counter).at(1)
		counter = counter + 2
	else:
		raise Exception('Unknown tokentype: "{}"'.format(otp_type))
	req2 = requests.post('https://mobile.strongauth.it/MobileLicenceServer/webresources/MobileLicenceService/SeedValidate', json=payload, headers=req_headers)
	resp2 = req2.json()
	
	if (resp2['returncode'] != '0000'):
		raise Exception('Error occured in seed validation: [{}] {}'.format(resp2['returncode'], resp2['description']))
	
	return [seed_b32, otp_type, digits, period, counter, algo]

def write_seed_file(seed, otp_type, digits, period, counter, algo):
	with open(os.path.join(os.sys.path[0], 'seed.json'), 'w') as text_file:
		text_file.write(json.dumps([seed, otp_type, digits, period, counter, algo]))
		