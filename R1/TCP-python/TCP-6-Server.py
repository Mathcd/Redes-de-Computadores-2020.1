from socket import *
import thread

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print 'The server is ready to receive'

def sockets_for_clients(connectionSocket, addr):
	sentence = connectionSocket.recv(1024)
	
	while(sentence != 'encerrar'):
		capitalizedSentence = sentence.upper()
		connectionSocket.send(capitalizedSentence)
		sentence = connectionSocket.recv(1024)
		
	connectionSocket.close()
	print 'Connection to client '+addr[0]+':'+str(addr[1])+' closed'

while True:
	connectionSocket, addr = serverSocket.accept()
	print 'Connection to client '+addr[0]+':'+str(addr[1])+' stablished'

	thread.start_new_thread(sockets_for_clients, (connectionSocket, addr))