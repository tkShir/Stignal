import sys
import socket
import select



def chat_client():
    #if(len(sys.argv) < 3) :
    #    print('Usage : python chat_client.py hostname port')
    #    sys.exit()

    # For sake of good UI
    host = raw_input("Chat room IP: ")
    # host = sys.argv[1]
    port = int(raw_input("Chat room port: "))
    KEY = raw_input("Encryption key: ")
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
    try :
        s.connect((host, port))
    except :
        print('Unable to connect')
        sys.exit()
     
    print('&&&                                &&&\n'
        + '*** Connected to remote chatroom. ****\n'
        + '*** Start securely messaging now! ****\n'
        + '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
    sys.stdout.write('[Me] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
         
        for sock in ready_to_read:             
            if sock == s:
                # incoming message from remote server, s
                data = sock.recv(4096)
                if not data :
                    print('\nDisconnected from chat server')
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data)
                    sys.stdout.write('[Me] '); sys.stdout.flush()     
            
            else :
                # user entered a message
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Me] '); sys.stdout.flush()

if __name__ == "__main__":
    sys.exit(chat_client())