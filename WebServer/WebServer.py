# Importing modules
from socket import *    
import thread
import time


# Keep the server running and listening to the incoming connections
def setup_connections(serverSocket, serverFlag):
	while True:
		print 'Ready to serve...\n'

		# Set up a new connection from the client
		connectionSocket, addr = serverSocket.accept()
		print "Connection stablished"

		# Show client info
		print "Client Address: "+str(addr[0])+":"+str(addr[1])+"\n"

		# Start a new threat to each client connected
		thread.start_new_thread(sockets_for_clients, (connectionSocket, addr))


# Open and read the requestedFile, send the socket headline
# according to the http code and send the file through socket
def read_send(requestedFile, httpCode, connectionSocket, addr):
	
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
	print "Sending '"+requestedFile+"' to "+str(addr[0])+":"+str(addr[1])+"\n"

	# Close the connection socket
	connectionSocket.close()
	

# Get the client request, process it and return a file
# depending on the request
def sockets_for_clients(connectionSocket, addr):
	
	# flag for server status
	global serverFlag

	# Dealing with exceptions
	try:
		# Receives the request message from the client
		message =  connectionSocket.recv(1024)
		print "Request:\n"+message
		
		# Extract the path of the requested object from the message
		# The path is the second part of HTTP header, identified by [1]
		filePath = message.split()[1]


		# Server shutdown command
		if filePath == '/kill':
			requestedFile = 'serverkilled.html'
			#connectionSocket.close()
			print "The server has been shutdown by kill command\n"
			serverFlag = False


		# Testing error 500 response with intentional invalid command
		elif filePath == '/teste500':
			requestedFile = 'noFile.html'


		# If no path is specified redirects to default page 
		elif filePath == '/':
			requestedFile = 'index.html'

		# Otherwise redirects to the requested file
		else:
			requestedFile = filePath[1:]

		# Read and send the file
		read_send(requestedFile, 200, connectionSocket, addr)


	# Exception for file not found
	except IOError:
		requestedFile = "error404.html"
		read_send(requestedFile, 404, connectionSocket, addr)


	# For unexpected errors
	except:

		# Try to notify the client with error 500
		try:
			requestedFile = "error500.html"
			read_send(requestedFile, 500, connectionSocket, addr)
			print "Internal server error\n"

		# If it is not possible to notify the client
		# just print the error on server's terminal
		except:
			print "Internal server error\n"



# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# Listen to at most 5 connections at a time
serverSocket.listen(5)

#global Flag for server status (up/down)
serverFlag = True

# Start the server
thread.start_new_thread(setup_connections, (serverSocket, serverFlag))

# Check server status, if False, close the server socket and ends the program
while serverFlag:
	time.sleep(1)

serverSocket.close()  

