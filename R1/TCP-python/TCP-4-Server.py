from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print 'The server is ready to receive'

while True:
	connectionSocket, addr = serverSocket.accept()
	weight = float(connectionSocket.recv(1024))
	height = float(connectionSocket.recv(1024))/100
	
	BMI = weight/height**2

	connectionSocket.send(str(BMI))
	connectionSocket.close()
