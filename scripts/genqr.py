import json
import os
import qrcode

def generate_and_print(seed=None, otp_type='TOTP', digits=8, period=60, counter=0, algo='SHA256'):
	if seed is None:
		try:
			with open(os.path.join(os.sys.path[0], 'seed.json'), 'r') as f:
				seed, otp_type, digits, period, counter = json.loads(f.read())
		except Exception as e:
			raise Exception('Error while reading seed file, make sure to execute the request.py script before this') from e
	
	period = int(period/1000)
	
	uri = ''

	if (otp_type == 'TOTP'):
		uri = 'otpauth://%(type)s/%(issuer)s:%(user)s?secret=%(secret)s&issuer=%(issuer)s&algorithm=%(algo)s&digits=%(digits)d&period=%(period)d' % {
			'type': otp_type.lower(),
			'issuer': 'Aruba',
			'user': 'userID',
			'secret': seed,
			'algo': algo,
			'digits': digits,
			'period': period
		}
	elif (otp_type == 'HOTP'):
		uri = 'otpauth://%(type)s/%(issuer)s:%(user)s?secret=%(secret)s&issuer=%(issuer)s&algorithm=%(algo)s&digits=%(digits)d&counter=%(counter)d' % {
			'type': otp_type.lower(),
			'issuer': 'Aruba',
			'user': 'userID',
			'secret': seed,
			'algo': algo,
			'digits': digits,
			'counter': counter
		}
	else:
		raise Exception('Unknown tokentype: "{}"'.format(otp_type))

	print('In case the qr code won\'t show up, use a qr generator to convert this uri:')
	print(uri)
	
	qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
	qr.add_data(uri)
	
	qr.print_ascii(invert=True)
	# qr.print_tty()  # nicer, but glitches out pretty bad
