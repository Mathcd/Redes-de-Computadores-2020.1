from socket import *
serverName = '127.0.0.1'
#serverName = '172.17.85.233'
serverPort = 12000
clientSocket = socket(AF_INET,SOCK_DGRAM)

message = raw_input('Input lowercase sentence:')

while(message != 'sair'):
	clientSocket.sendto(message,(serverName, serverPort))
	modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
	print modifiedMessage
	message = raw_input('Input lowercase sentence:')

clientSocket.close()
