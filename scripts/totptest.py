import pyotp
import hashlib
import base64
import CBCUtil
import os

def generate(seed=None, time=None):
    if seed is None:
        try:
            with open(os.path.join(os.sys.path[0], 'seed.txt'), 'r') as f:
                seed = f.readline()
        except Exception as e:
            raise Exception('Error while reading seed file, make sure to execute the request.py script before this') from e

    gen = pyotp.TOTP(seed, digits=8, digest=hashlib.sha256, interval=30)
    code = 0
    if time is None:
        code = gen.now()
    else:
        code = gen.at(time)

    return code
