from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

database = [['Sao Paulo','Santo Andre'], # 'City'
			['17.5','18.3'],			 # 'min day 1'
			['29.1','29.4'],			 # 'max day 1'
			['0.45','0.34'],			 # 'rain day 1'
			['19.2','19.7'],			 # 'min day 2'
			['31.4','27.7'],			 # 'max day 2'
			['0.22','0.14'],			 # 'rain day 2'
			['15.0','16.1'],			 # 'min day 3'
			['34.1','26.2'],			 # 'max day 3'
			['0.87','0.68'],			 # 'rain day 3'
		   ]

print "The server is ready to receive"

while True:
	request, clientAddress = serverSocket.recvfrom(2048)

	if request == 'connect':
		serverSocket.sendto('True', clientAddress)

	city_days, __ = serverSocket.recvfrom(2048)

	while city_days != 'END':
		CITY, DAYS = city_days.split(',')
		index = database[0].index(CITY)
		data = ''

		for ii in range(int(DAYS)*3):
			data += (database[ii+1][index]+',')

		serverSocket.sendto(data, clientAddress)
		city_days, __ = serverSocket.recvfrom(2048)
