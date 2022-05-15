import json
import pyotp
import hashlib
import os

def generate_totp(seed, digits, interval, time):
	if seed is None:
		try:
			with open(os.path.join(os.sys.path[0], 'seed.json'), 'r') as f:
				seed, otp_type, digits, period, _ = json.loads(f.read())
				if (otp_type != 'TOTP'):
					raise Exception('The token type is not time-based!')
				interval = period/1000
		except Exception as e:
			raise Exception('Error while reading seed file, make sure to execute the request.py script before this') from e

	gen = pyotp.TOTP(seed, digits=digits, digest=hashlib.sha256, interval=interval)

	return gen.now() if time is None else gen.at(time)
