import sys
import socket
import select
import os

# Baseline code was taken from the following website tutorials:
# * https://www.bogotobogo.com/python/python_network_programming_tcp_server_client_chat_server_chat_client_select.php
# * https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
# and repurposed to fit our needs

SOCKET_LIST = []

def chat_server():
    # Get server input details
    HOST = raw_input("Server IP: ")
    PORT = int(raw_input("Server port: "))
    RECV_BUFFER = 4096

    os.system('clear')

    print("+-+-+-+ Welcome to SteganoChat +-+-+-+\n" 
        + "*** If you want to hide something ****\n"
        + "*** important from the government ****\n"
        + "*** we're here to help you.       ****\n"
        + "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
        + "*** Starting your server...       ****\n"
        + "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")

    # Set up server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    SOCKET_LIST.append(server_socket)
    print('&&&                                &&&\n'
        + '*** Server started successfully.  ****\n'
        + '*** Start securely messaging now! ****\n'
        + '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
    print("Chat server started on port " + str(PORT))
 
    while 1:
        # Get sockets which are ready
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
      
        for sock in ready_to_read:
            # This means a new client has connected
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print("User (%s, %s) has connected to the server." % addr)
                 
                broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)
             
            # This means a new message has been received
            else:


                try:
                    # Socket has data to be transferred.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # Data to be transferred
                        output_data = data
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + output_data)  
                    else:
                        # Remove broken sockets
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # Connection broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()

# Placeholder method
def do_something_with_incoming_data(data):
    pass
    
# Broadcast a message to all connected clients
def broadcast(server_socket, sock, message):
    for socket in SOCKET_LIST:

        # Send a message to the given socket
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                # Close the socket
                socket.close()
                # Remove socket from list
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":
    sys.exit(chat_server()) 