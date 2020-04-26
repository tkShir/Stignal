"""
for 4 and 5. Our choice for the encryption scheme is AES-CTR, python implementation is found here:
    https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
We will apply AES-CTR on the message before it is transformed.
So we need to encrypt the message and store it.
This library is trusted.
"""

from Crypto.Cipher import AES

def encrypt(message, key):
	"""
	Input:
	    message: string
	    key: bytes/bytearray/memoryview (Must be 16, 24, or 32 bytes long)
	Output:
		ciphertext: bytes
		tag:
	"""

	if not (len(key) == 16 or len(key) == 24 or len(key) == 32):
		print(f'Key Length Incorrect (length: {len(key)})')
		print('Exiting Encryption Method...')
		return None

	data = bytes(message, 'utf-8')
	cipher = AES.new(key, AES.MODE_CTR)
	ct_bytes = cipher.encrypt(data)
	nonce = cipher.nonce

	return (ct_bytes, nonce)

def decrypt(ciphertext, key, nonce):
	try:
		cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
		plaintext_bytes = cipher.decrypt(ciphertext)
		plaintext = plaintext_bytes.decode('utf-8')
		return plaintext
	except Exception:
		print("Incorrect decryption")
		return None

if __name__ == '__main__':
	message = 'Is there life on mars'
	key = b'Sixteen byte key'
	key2 = b'twenty-four byte key    '
	key3 = b'thirty-two byte key thirty-two  '

	ctxt, nonce = encrypt(message, key)
	ctxt2, nonce2 = encrypt(message, key2)
	ctxt3, nonce3 = encrypt(message, key3)

	print(decrypt(ctxt, key, nonce))
	print(decrypt(ctxt2, key2, nonce2))
	print(decrypt(ctxt3, key3, nonce3))
