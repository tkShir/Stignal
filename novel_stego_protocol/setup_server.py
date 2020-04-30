import sys
import socket
import select

# from enc_and_dec import decrypt

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009
key_input = ''

CHAT_ENTER_CODE = 1
CHAT_EXIT_CODE = 2
CHAT_MSG_CODE = 3

def chat_server():
	HOST = input("Server IP: ")
	PORT = int(input("Server port: "))

	print("+-+-+-+ Welcome to SteganoChat +-+-+-+\n"
		  + "*** If you want to hide something ****\n"
		  + "*** important from the government ****\n"
		  + "*** we're here to help you.       ****\n"
		  + "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
		  + "*** Starting your server...       ****\n"
		  + "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)

	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)
	print('&&&                                &&&\n'
		  + '*** Server started successfully.  ****\n'
		  + '*** Start securely messaging now! ****\n'
		  + '-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
	print("Chat server started on port " + str(PORT))

	while 1:

		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)

		for sock in ready_to_read:
			# a new connection request recieved
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				
				clientinfo = "(%s, %s)" % addr
				print("Client (%s, %s) connected" % addr)

				broadcast(server_socket, sockfd, ("%i$%s\n" % (CHAT_ENTER_CODE, clientinfo)).encode('ascii'))

			# a message from a client, not a new connection
			else:
				# process data recieved from client,
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER)
					if data:
						# there is something in the socket
						
						print("Got data:", data, str(sock.getpeername()))

						output_data = ("%i$%s$%s" % (CHAT_MSG_CODE, str(sock.getpeername()), data.decode('ascii'))).encode('ascii')
						broadcast(server_socket, sock, output_data)
					else:
						# remove the socket that's broken
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)

						clientinfo = "(%s, %s)" % addr
			
						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, ("%i$%s\n" % (CHAT_EXIT_CODE, clientinfo)).encode('ascii'))

					# exception
				except ZeroDivisionError:
					clientinfo = "(%s, %s)" % addr
					broadcast(server_socket, sock, ("%i$%s\n" % (CHAT_EXIT_CODE, clientinfo)).encode('ascii'))
					continue

	server_socket.close()


# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
	for socket in SOCKET_LIST:
		# send the message only to peer
		if socket != server_socket and socket != sock:
			socket.send(message)
			'''try:
				socket.send(message)
			except:
				print("\nRemoving broken socket")
				# broken socket connection
				socket.close()
				# broken socket, remove it
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)'''


if __name__ == "__main__":
	sys.exit(chat_server())
