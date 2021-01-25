import pyotp
import hashlib
import base64
import CBCUtil

key = base64.b32encode('your-seed-here')

gen = pyotp.TOTP(key, digits=8, digest=hashlib.sha256)

print(gen.now())