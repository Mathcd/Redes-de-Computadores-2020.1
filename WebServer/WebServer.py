# Import socket module
from socket import *    

# Create a TCP server socket
#(AF_INET is used for IPv4 protocols)
#(SOCK_STREAM is used for TCP)

#=============================================
### PRECISA COLOCAR O favicon.ico !!!!!!!!
#=============================================

serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)


# Open and read the requestedFile, send the socket headline
# according to the http code and send the file through socket
def read_send(requestedFile, httpCode, connectionSocket):
	f = open(requestedFile)
	requestedData = f.read()

	# headline response for socket according to http code
	if httpCode == 200:
		responseHeader = "HTTP/1.1 200 OK\r\n\r\n"
	
	elif httpCode == 404:
		responseHeader = "HTTP/1.1 404 Not Found\r\n\r\n"
	
	elif httpCode == 500:
		responseHeader = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
		
	connectionSocket.send(responseHeader)


	for ii in range(len(requestedData)):  
		connectionSocket.send(requestedData[ii])
	connectionSocket.send("\r\n")

	connectionSocket.close()

	

# Server should be up and running and listening to the incoming connections
while True:
	print 'Ready to serve...'
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	

	# Dealing with exceptions
	try:
		# Receives the request message from the client
		message =  connectionSocket.recv(1024)
		print message
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filePath = message.split()[1]

		# ===========================================
		# KILL SERVER (for development only)
		if filePath == '/kill':
			print "The server will shutdown now"
			break
		# ===========================================
		
		print filePath
		print "Tamanho do filePath:", len(filePath)

		# If no path is specified redirects to default page 
		if filePath == '/':
			requestedFile = 'index.htm'

		else:
			requestedFile = filePath[1:]

		# Read and send the file
		read_send(requestedFile, 200, connectionSocket)

	# Exception for file not found
	except IOError:
		requestedFile = "error404.htm"
		read_send(requestedFile, 404, connectionSocket)

		connectionSocket.close()

	# ============================================
	# PROVISORY! BROKEN PIPE BUG HAS TO BE CORRECTED!!!
	except IndexError:
		print "Houve algum erro de indice\n\n"
		connectionSocket.send("HTTP/1.1 500 Internal Server Error\r\n\r\n")
		# connectionSocket.send("<html><head></head><body><h1>500 Internal Server Error</h1></body></html>\r\n")
	# ============================================


serverSocket.close()  

