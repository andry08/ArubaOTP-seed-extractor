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

def main():
	activationCode = input('Insert your activation code (the long number listed over the qr code): ').strip()
	# This check was copied from aruba's app, only basic validation here, but the code itself has a validation rule too
	if (len(activationCode) != 18 or int(activationCode[0]) not in [2, 3, 8, 9]):
		return print('The code you entered doesn\'t seem to be right, it has to be 18 digits long and start with either 2, 3, 8 or 9')

	payload = {
		'applicationcode': app_code,
		'activationcode': CBCUtil.encrypt(encryption_key, activationCode),
		'authtoken': CBCUtil.encrypt(encryption_key, str(int(time.time() * 1000)))
	}
	req1 = requests.post('https://mobile.strongauth.it/MobileLicenceServer/webresources/MobileLicenceService/SeedRequest', json=payload, headers=user_agent)
	resp1 = req1.json()

	if (resp1['returncode'] != '0000'):
		print('Seed request failed:')
		return print('[%s] %s' % (resp1['returncode'], resp1['description']))

	seed = CBCUtil.decrypt(encryption_key, resp1['seed'])
	print('Got seed!', seed)
	seed_b32 = base64.b32encode(base64.b16decode(seed)).decode('utf-8').replace('=', '')
	print('In base32:', seed_b32)

	with open(os.path.join(os.sys.path[0], 'seed'), 'w') as text_file:
		text_file.write(seed_b32)
		print('Wrote seed to file, you can now use it in any TOTP app you want, just make sure to select sha256 as algorithm and 8 digits output')

	payload = {
		'applicationcode': app_code,
		'activationcode': CBCUtil.encrypt(encryption_key, activationCode),
		'authtoken': CBCUtil.encrypt(encryption_key, str(int(time.time() * 1000))),
		'otp1': pyotp.TOTP(base64.b32encode(base64.b16decode(seed)), digits=8, digest=hashlib.sha256).now(),
		'otp2': ''
	}
	req2 = requests.post('https://mobile.strongauth.it/MobileLicenceServer/webresources/MobileLicenceService/SeedValidate', json=payload, headers=user_agent)
	resp2 = req2.json()
	
	# print(resp2)
	if (resp2['returncode'] != '0000'):
		print('Error occured in seed validation:')
		return print('[%s] %s' % (resp2['returncode'], resp2['description']))

	print('Success!')

if __name__ == '__main__':
	main()