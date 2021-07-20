# Codigo basado de Socket Programming with Multi-threading in Python
# Import socket module
import socket
import random
import os
os.system("python pool.py")
from pool import *
id_user = 0
id_sala = random.randint(0,5000)

def Main():
	host = 'localhost'

	# Define the port on which you want to connect
	port = int(raw_input("Puerto de conexion: "))

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	# message you send to server
	while True:

		# message sent to server
		message = raw_input("email: ")
		s.send(message.encode('ascii'))

		# messaga received from server
		data = s.recv(1024)

		password = raw_input("password: ")
		s.send(password.encode('ascii'))

		id_user= login(message,password)

		data = s.recv(1024)

		# print the received message
		# here it would be a reverse of sent message
		print('Mensaje del servidor :',str(data.decode('ascii')))

		if(data.decode('ascii') == "registro"):
			response = raw_input("alguno de los campos es incorrecto o no esta registrado, desea registrarse? (y/n):  ")
			s.send(response.encode('ascii'))
			if(response == "y"):
				numregs = 6
				while numregs > 0:
					message = s.recv(1024)
					print(message)
					response = raw_input("")
					s.send(response.encode('ascii'))
					numregs -= 1
				print("Ingrese de nuevo")

			else:
				print("noup")

		elif (data.decode('ascii') == "log-ex"):
			response = raw_input("logueado con exito \n MSG:")			
			while response != "console":
				s.send(("MSG: "+response).encode('ascii'))
				response = raw_input("--> ")
				show = s.recv(1024)				
				id_sala = show.split(" ")[0]
				#print("id_sala c: ",id_sala)
				flag = user_in_sala(id_user,id_sala)
				print("InvisibleComma", show)
			
			while response != "exit":
				print("Escriba su comando")
				response = raw_input()
				s.send((response).encode('ascii'))


		# ask the client whether he wants to continue
		ans = raw_input('\n Conexion perdida, deseas intentarlo de nuevo?(y/n) :')
		if ans == 'y':
			continue
		else:
			break


	# close the connection
	s.close()

if __name__ == '__main__':
	Main()
	Main()
