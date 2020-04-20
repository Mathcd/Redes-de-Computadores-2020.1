from socket import *
serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# get and send users weight
weight = raw_input('Enter your weight (kg): ')
clientSocket.send(weight)

# get and send user's height
height = raw_input('Enter your height (cm): ')
clientSocket.send(height)

# receive BMI and print
BMI = clientSocket.recv(1024)
print 'Your BMI is', BMI

clientSocket.close()
