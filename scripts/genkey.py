import os
from Crypto.Cipher import AES
from Crypto.Hash import SHA1
from Crypto.Protocol.KDF import PBKDF2

kdf_key = 'ec46d084-41b7-11e6-99c7-005056a0a452' # application key
kdf_salt = 'ArubaPEC'

keyout = PBKDF2(kdf_key, kdf_salt, 32, 1024, hmac_hash_module=SHA1)
# print(keyout.hex())

encrypted_key = 0
with open(os.path.join(os.sys.path[0], 'appkey.sec'), 'rb') as f: # file extracted from app raw resources
	encrypted_key = bytearray(f.read())

cipher = AES.new(keyout, AES.MODE_ECB)

decrypted_key = cipher.decrypt(encrypted_key)
decrypted_key = decrypted_key[:-decrypted_key[-1]] # remove padding

print(decrypted_key.hex())