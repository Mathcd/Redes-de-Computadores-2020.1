# Import socket module
from socket import *    

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# Listen to at most 4 connections at a time
serverSocket.listen(4)


# Open and read the requestedFile, send the socket headline
# according to the http code and send the file through socket
def read_send(requestedFile, httpCode, connectionSocket):
	
	# open the requested data as binary and read it
	f = open(requestedFile, 'rb')
	requestedData = f.read()

	# headline response for socket according to http code
	if httpCode == 200:
		responseHeader = "HTTP/1.1 200 OK\r\n\r\n"
	
	elif httpCode == 404:
		responseHeader = "HTTP/1.1 404 Not Found\r\n\r\n"
	
	elif httpCode == 500:
		responseHeader = "HTTP/1.1 500 Internal Server Error\r\n\r\n"

	# Send response header and the requested data		
	connectionSocket.send(responseHeader)
	connectionSocket.send(requestedData)
	connectionSocket.send("\r\n")

	# Close the connection socket
	connectionSocket.close()
	

# Server should be up and running and listening to the incoming connections
while True:
	print ('Ready to serve...')
	
	# Set up a new connection from the client
	connectionSocket, addr = serverSocket.accept()
	

	# Dealing with exceptions
	try:
		# Receives the request message from the client
		message =  connectionSocket.recv(1024)
		print (message)
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filePath = message.split()[1]


		# Server shutdown command
		if filePath == '/kill':
			read_send('serverkilled.html', 200, connectionSocket)
			connectionSocket.close()
			print ("The server has been shutdown")
			break
		

		# If no path is specified redirects to default page 
		if filePath == '/':
			requestedFile = 'index.html'

		# Otherwise redirects to the requested file
		else:
			requestedFile = filePath[1:]

		# Read and send the file
		read_send(requestedFile, 200, connectionSocket)


	# Exception for file not found
	except IOError:
		requestedFile = "error404.html"
		read_send(requestedFile, 404, connectionSocket)


	# Dealing with broken pipe exception bug
	except IndexError:
		requestedFile = "error500.html"
		read_send(requestedFile, 500, connectionSocket)
		print ("Internal server error\n\n")


	# For unexpected errors
	except:

		# Try to notify the client with error 500
		try:
			requestedFile = "error500.html"
			read_send(requestedFile, 500, connectionSocket)
			print ("Internal server error\n\n")

		# If it is not possible to notify the client
		# just print the error on server's terminal
		except:
			print ("Internal server error\n\n")


# Close the server socket
serverSocket.close()  

