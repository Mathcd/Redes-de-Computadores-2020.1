from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print 'The server is ready to receive'

while True:
	connectionSocket, addr = serverSocket.accept()
	sentence = connectionSocket.recv(1024)

	print 'Connection to client stablished'

	while(sentence != 'encerrar'):
		capitalizedSentence = sentence.upper()
		connectionSocket.send(capitalizedSentence)
		sentence = connectionSocket.recv(1024)

	connectionSocket.close()
	print 'Connection to client closed\n'
	print 'The server is ready to receive'