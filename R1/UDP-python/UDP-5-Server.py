from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

allowedClients = ['127.0.0.1', '192.168.0.34']

print "The server is ready to receive"

while True:
	message, clientAddress = serverSocket.recvfrom(2048)

	if(clientAddress[0] in allowedClients):
		modifiedMessage = message.upper()
		serverSocket.sendto(modifiedMessage, clientAddress)

	else:
		serverSocket.sendto('Error 403: forbidden', clientAddress)