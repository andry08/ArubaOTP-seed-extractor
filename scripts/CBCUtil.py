import base64
from Crypto.Cipher import AES
from Crypto import Random

def encrypt(key, raw):
	raw += (AES.block_size - len(raw) % AES.block_size) * chr(AES.block_size - len(raw) % AES.block_size)
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode('utf-8')

def decrypt(key, enc):
	enc = base64.b64decode(enc)
	iv = enc[:AES.block_size]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	dec = cipher.decrypt(enc[AES.block_size:])
	return (dec[:-dec[-1]]).decode('utf-8')
