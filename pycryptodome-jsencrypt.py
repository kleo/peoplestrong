import base64
from base64 import b64decode, b64encode
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import requests
import urllib

pubkey = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfcPXpvCFtEplCT5g/DasjabZ3
hGqszcgJU4fuBX7e7ci6t4oQqDUbIJTqODx0HUNTiRqMo61BarLRwZQ9ROiFAmkI
3TM1zVlAwb27afL2y6axK1NhzbvT9zCdLhTFRlBXHEBTdJHver/T1yFAsT9Vxrzk
p1mayP8GAvzUZIDd/QIDAQAB
-----END PUBLIC KEY-----'''

privkey = '''-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCfcPXpvCFtEplCT5g/DasjabZ3hGqszcgJU4fuBX7e7ci6t4oQ
qDUbIJTqODx0HUNTiRqMo61BarLRwZQ9ROiFAmkI3TM1zVlAwb27afL2y6axK1Nh
zbvT9zCdLhTFRlBXHEBTdJHver/T1yFAsT9Vxrzkp1mayP8GAvzUZIDd/QIDAQAB
AoGAMXgs9J6IiH0SzD5B8J5fERfFo4OUTZVzkWE3daSC3sxMUZKM5eoqwAX17k4Q
g75om0yYzjYilX9ziB1Vz0TIF67V4pH2/kD8sAeVX3TkEAsHLOPp7zn+Xbt54LcP
0NHdVQMK/19Ut3x59pYUMrHSd4crPTg240u8YcqsTeXBDokCQQDewmhYQNWEOE7w
W4UmeCbqaXtRAhvfpoO/Xb0hqqs/APw7Psii9me9Y2rT7TsYKDJQrXB+X2oetsde
RaWtnzIXAkEAtzu/Xbj9QULF5sTAXq39fco3c1kdZFTRyzRK0qvSWLahWgTCj+NO
hE+n74DCXlT80LJpHPcf1mAlYAZQgSlhCwJBANAKstcRnhgBWsAiSWWXO4kcAH60
wIGNC2hzTIsf0RVjfy55wXppNJPtQL0yx0kVaYBtqy1rQTn0LJi/5S8VCfsCQFBU
xWUVgRJnb9PoVl4r8YKAcScE3rnp5cAswNDzu1hhWQPaKmJiyT2AnqOF07D/mYb1
cNfeD/swU7JxkkHOHlkCQHCcnkZEzIWlSNc1Z7btFWDlb3jJH2IcYv/LWfxAWFgu
YUDHIrzFkxvwsC3GBznUAewhCNPGeQ+p6xfb4vrvAj4=
-----END RSA PRIVATE KEY-----'''

rsa_key = RSA.importKey(pubkey)

cipher = PKCS1_v1_5.new(rsa_key)

rsa_key2 = RSA.importKey(privkey)

decipher = PKCS1_v1_5.new(rsa_key2)

username_encrypted = base64.b64encode(cipher.encrypt(b"username")).decode('utf-8')
password_encrypted = base64.b64encode(cipher.encrypt(b"password")).decode('utf-8')      

print(username_encrypted)

username_decrypted = decipher.decrypt(b64decode(username_encrypted), 'error').decode('utf-8')

print(username_decrypted)

username_url_encoded = urllib.parse.quote(username_encrypted, safe='')

print(username_url_encoded)

