import os
import base64
import qrcode

def generate_and_print(seed=None):
	if seed is None:
		try:
			with open(os.path.join(os.sys.path[0], 'seed.txt'), 'r') as f:
				seed = f.readline()
		except Exception as e:
			raise Exception('Error while reading seed file, make sure to execute the request.py script before this') from e
	
	uri = 'otpauth://totp/%(issuer)s:%(user)s?secret=%(secret)s&issuer=%(issuer)s&algorithm=%(algo)s&digits=%(digits)d' % {
		'issuer': 'Aruba',
		'user': 'userID',
		'secret': seed,
		'algo': 'SHA256',
		'digits': 6
	}

	print('In case the qr code won\'t show up, use a qr generator to convert this uri:')
	print(uri)
	
	qr = qrcode.QRCode()
	qr.add_data(uri)
	
	qr.print_ascii()
	# qr.print_tty()  # nicer, but glitches out pretty bad
