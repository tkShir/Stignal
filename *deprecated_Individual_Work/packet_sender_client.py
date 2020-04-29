import sys
import socket
import select
import os
import random
from Crypto.Cipher import AES

# Baseline code was taken from the following website tutorials:
# * https://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
# * https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
# and repurposed to fit our needs

def chat_client():
    default = raw_input("Use default settings for IP and port settings? [y/N]: ")

    if default != 'y':
        # For the sake of good UI, get user input details
        HOST = raw_input("Chat room IP: ")
        PORT = int(raw_input("Chat room port: "))
    else:
        HOST = 'localhost'
        PORT = 9009

    KEY = b''
    while not (len(KEY) == 16 or len(KEY) == 24 or len(KEY) == 32):
        KEY = bytes(raw_input("Encryption key: "))
    
    # Verbose mode is used to display message interior logs
    verbose = raw_input('Do you want to turn on verbose mode? [y/N]: ')
    if verbose == 'y':
        verbose = True
    else:
        verbose = False

    os.system('clear')
    
    print("+-+-+-+ Welcome to SteganoChat +-+-+-+\n" 
        + "*** If you want to hide something ****\n"
        + "*** important from the government ****\n"
        + "*** we're here to help you.       ****\n"
        + "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
        + "*** Connecting to chat room...    ****\n"
        + "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    
    # Connect to the server
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print("Unable to connect to server. Exiting.")
        print(e)
        exit(0)
     
    print('&&&                                &&&\n'
        + '*** Connected to remote chatroom. ****\n'
        + '*** Start securely messaging now! ****\n'
        + '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
    sys.stdout.write("*** Me: ")
    sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get all possible ready to read/write sockets
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
        
        for sock in ready_to_read:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    # This means the server died
                    print("\nDisconnected from server.")
                    exit(0)
                else :
                    # Print the data
                    process_packet(data, KEY, verbose)
                    sys.stdout.write("*** Me: ")
                    sys.stdout.flush()
            
            # aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
            else :
                # User sends a message
                msg = sys.stdin.readline().replace('\n', '')

                file_contents = ""
                if msg == "/quit":
                    exit(0)
                if msg[0:6] == "/file ":
                    file_extp = msg[6:].strip()
                    try:
                        f = open(file_extp, "rb")
                        content = f.read()
                        msg = "/file " + content
                        f.close()
                        
                    except Exception as e:
                        sys.stdout.write("Error in file path. Code broke.")
                        exit(0)

                send_packet(msg, s, KEY, verbose)
                sys.stdout.write('*** Me: ')
                sys.stdout.flush()


def send_packet(msg, socket, key, verbose):
    ctxt, nonce = encrypt(msg, key)

    # Extract the nonce from text
    nonce_and_ctxt = nonce + bytes('|||') + ctxt

    # Do stego magic on the nonce_and_ctxt variable
    stego_text = nonce_and_ctxt

    # If verbose mode turned on show all info.
    if verbose:
        print("\tSending Message: %s" % msg)
        print("\tCipherText: %s" % ctxt)
        print("\tNonce: %s" % nonce)
        print("\tData to be sent: %s" % nonce_and_ctxt)
        print("\tStego Transformed Text: %s" % stego_text)
        print("")

    socket.send(stego_text)
    return None

def process_packet(stego_data, key, verbose):
    # Reverse stego magic
    orig_data = stego_data


    try:
        # Get the nonce
        split_intro_nonce_and_ctxt = orig_data.split(b'|||')
        if len(split_intro_nonce_and_ctxt) < 2:
            sys.stdout.write(orig_data)
            return None

        ctxt = split_intro_nonce_and_ctxt[1]

        # Sorry for weird implementation, it's because of the packets being sent sends a IP/Port header which makes it messy
        intro_end_idx = split_intro_nonce_and_ctxt[0].index(']')
        intro, nonce = split_intro_nonce_and_ctxt[0][:intro_end_idx+2], split_intro_nonce_and_ctxt[0][intro_end_idx+2:]
    except:
        sys.stdout.write("Packet Error: Data received was not valid\n")
        return None


    if verbose:
        print("Received Text:")
        print(stego_data)
        print("Stego-text transformed back to original data:")
        print("%s" % orig_data)
        print("Ciphertext: %s" % ctxt)
        print(nonce)

    dec = decrypt(ctxt, key, nonce)

    if dec[0:6] == "/file ":
        file_cal = dec[6:].strip()
        f = open('msg' + str(random.randint(0, 99999)) + '.txt', 'wb')
        f.write(file_cal)
        f.close()

    message = str(intro).strip() + ": " + dec + "\n"
    sys.stdout.write(message)
    return None


def encrypt(message, key):
    """
    Input:
        message: string
        key: bytes/bytearray/memoryview (Must be 16, 24, or 32 bytes long)
    Output:
        ciphertext: bytes
        tag:
    """

    # Make sure that the key is the correct size
    if not (len(key) == 16 or len(key) == 24 or len(key) == 32):
        print('Key Length Incorrect (length: %s)' %len(key))
        print('Exiting encryption method...')
        return None

    # Encrypt the data
    data = bytes(message)
    cipher = AES.new(key, AES.MODE_CTR)
    ct_bytes = cipher.encrypt(data)
    nonce = cipher.nonce

    return (ct_bytes, nonce)

def decrypt(ciphertext, key, nonce):
    # Decrypt the data
    try:
        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        plaintext_bytes = cipher.decrypt(ciphertext)
        plaintext = plaintext_bytes.decode('utf-8')
        return plaintext
    except Exception:
        print("Incorrect decryption")
        return None

if __name__ == "__main__":
    sys.exit(chat_client())