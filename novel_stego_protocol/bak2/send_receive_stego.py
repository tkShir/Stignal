import sys
import socket
import select
import os
import binascii
from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto import Random

CHAT_ENTER_CODE = 1
CHAT_EXIT_CODE = 2
CHAT_MSG_CODE = 3

def chat_client():
	# if(len(sys.argv) < 3) :
	#    print('Usage : python chat_client.py hostname port')
	#    sys.exit()

	# Default Parameters:
	default = input("Use default settings for IP, port, and key settings? [y/N]: ")

	if default != 'y':
		# For sake of good UI
		host = input("Chat room IP: ")
		port = int(input("Chat room port: "))
		KEY = ''
	else:
		host = 'localhost'
		port = 8888
		KEY = 'azsxdcfvgbhnjmklazsxdcfvgbhnjmkl'

	while not (len(KEY) == 16 or len(KEY) == 24 or len(KEY) == 32):
		print('\tError: Key Length is Incorrect, enter key with length 16, 24, or 32.')
		KEY = bytes(input("Encryption key: "), encoding='ascii')
	verbose = input('Do you want to turn on verbose mode? [y/N]: ')
	if verbose == 'y':
		verbose = True
	else:
		verbose = False

	os.system('clear')
	# port = int(sys.argv[2])
	print("+-+-+-+ Welcome to SteganoChat +-+-+-+\n"
		  + "*** If you want to hide something ****\n"
		  + "*** important from the government ****\n"
		  + "*** we're here to help you.       ****\n"
		  + "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
		  + "*** Connecting to chat room...    ****\n"
		  + "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	# connect to remote host
	try:
		s.connect((host, port))
	except:
		print('Unable to connect')
		sys.exit()

	print('&&&                                &&&\n'
		  + '*** Connected to remote chatroom. ****\n'
		  + '*** Start securely messaging now! ****\n'
		  + '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
	sys.stdout.write('[Me] ');
	sys.stdout.flush()

	while 1:
		socket_list = [sys.stdin, s]

		# Get the list sockets which are readable
		ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

		for sock in ready_to_read:
			if sock == s:
				# incoming message from remote server, s
				data = sock.recv(4096)
				if not data:
					print('\nDisconnected from chat server')
					sys.exit()
				else:
					# print data
					process_packet(data, KEY, verbose)
					sys.stdout.write('[Me] ');
					sys.stdout.flush()

			else:
				# user entered a message
				msg = sys.stdin.readline().replace('\n', '')

				send_packet(msg, s, KEY, verbose)

				sys.stdout.write('[Me] ');
				sys.stdout.flush()

def apply_stego(data):
	return data.hex()
	
def reverse_stego(stego):
	#return stego
	return binascii.unhexlify(stego)

def send_packet(msg, socket, key, verbose):
	iv, ciphertext = encrypt(key, msg)
	
	msg_data = iv + b'|||' + ciphertext
	
	stego_text = apply_stego(msg_data)

	# If verbose mode turned on show all info.
	if verbose:
		print('\tSending Message: %s' % msg)
		print('\tCipherText: %s' % ciphertext)
		print('\tIV: %s' % iv)
		print('\tData to be sent: %s' % msg_data)
		print('\tStego Transformed Text: %s' % stego_text)
		print('')

	socket.send(stego_text.encode('ascii'))
	return None


def process_packet(data, key, verbose):
	data_parts = data.decode('ascii').split('$')
	
	code, client_info = int(data_parts[0]), data_parts[1].replace('\n', '').replace('\r', '')
	
	if code == CHAT_ENTER_CODE:
		print('\n[' + client_info + '] entered chat')
	elif code == CHAT_EXIT_CODE:
		print('\n[' + client_info + '] left chat')
	elif code == CHAT_MSG_CODE:
		msg_stego = data_parts[2]
		
		msg_bytes = reverse_stego(msg_stego)
		
		msg_parts = msg_bytes.split(b'|||')
		
		iv, ciphertext = msg_parts[0], msg_parts[1]
		
		msg = decrypt(key, iv, ciphertext)
		
		if verbose:
			print('\tReceived Text (from %s)' % client_info)
			print('\tStego Message: %s' % msg_stego)
			print('\tCipherText: %s' % ciphertext)
			print('\tIV: %s' % iv)
			print('\tOriginal text: %s' % msg)

		message = '\n[' + client_info + '] sent a message: ' + msg + '\n'
		print(message)


def encrypt(key, plaintext):
	iv = Random.new().read(AES.block_size)
	iv_int = int(binascii.hexlify(iv), 16) 
	ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
	aes = AES.new(key, AES.MODE_CTR, counter=ctr)
	ciphertext = aes.encrypt(plaintext)
	return (iv, ciphertext)

def decrypt(key, iv, ciphertext):
	iv_int = int.from_bytes(iv, "big", signed=False) 
	ctr = Counter.new(AES.block_size * 8, initial_value=iv_int)
	aes = AES.new(key, AES.MODE_CTR, counter=ctr)
	plaintext = aes.decrypt(ciphertext)
	return plaintext.decode('ascii')

if __name__ == "__main__":
	sys.exit(chat_client())
