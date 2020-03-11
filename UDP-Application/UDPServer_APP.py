from socket import *

allowed_list = ['127.0.0.1','172.17.85.233', '172.17.85.235']

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

print "The server is ready to receive\n"
while 1:
	message, clientAddress = serverSocket.recvfrom(2048)

	if(clientAddress[0] in allowed_list):	
		modifiedMessage = message.upper()
		serverSocket.sendto(modifiedMessage, clientAddress)
		print 'Message <', modifiedMessage, '> sent to Client in', clientAddress
	else:
		print('Message ignored from Client in', clientAddress)

	print "\nThe server is ready to receive\n"
