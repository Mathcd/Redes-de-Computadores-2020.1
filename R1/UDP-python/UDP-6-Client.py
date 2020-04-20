from socket import *

serverName = '127.0.0.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)

print 'Trying to connect'
clientSocket.sendto('connect',(serverName, serverPort))
CONNECT, serverAddress = clientSocket.recvfrom(2048)

loopFlag = False

while True:
	if CONNECT == 'True':
		
		if not loopFlag:
			print 'Connection stablished'
			CITY = raw_input('Enter a City: ')
		DAYS = raw_input('Enter the number of days: ')
		city_days = CITY+','+DAYS

		clientSocket.sendto(city_days,(serverName, serverPort))
		data, serverAddress = clientSocket.recvfrom(2048)
		splitted_data = data.split(',')
		
		print 'Weather for '+CITY

		for ii in range(int(DAYS)):
			print 'Day '+str(ii+1)+':'
			print 'min: '+splitted_data[3*ii]
			print 'max: '+splitted_data[3*(ii+1)-2]
			print 'rain: '+splitted_data[3*(ii+1)-1]+'%\n'

		nextInput = raw_input('Enter City or END: ')
		loopFlag = True

		if nextInput == 'END':
			clientSocket.sendto('END',(serverName, serverPort))
			break
		CITY = nextInput

	else:
		print 'Connection refused'

clientSocket.close()
print 'Connection closed'