# Servidor para n clientes con threads
from pool import *
from thread import *
import socket
import sys
import random
import threading

import os
os.system("python pool.py")

user_id = None
id_sala = random.randint(0, 5000)
catch = False
#clients_lock = threading.Lock()
#clients = set()


def clientthread(conn):
    print ("Detectada una nueva conexion")
    buffer = ""
    while True:
        message = conn.recv(8192)
        print(message)
        vsagge = message.split(" ")
        # cR <nombreSala> . Crear sala con el nombreSala. El servidor de forma automatica ingresa a este
        # cliente a la sala que creo.
        if vsagge[0] == "#cR":
            vsagge = vsagge.pop(1)
            print(vsagge)
            message = ''.join(vsagge)

            register_sala(id_sala, message)
            register_sala_usuario(id_sala, id_usuario)

        # gR <nombreSala> Entrar a la sala nombreSala.
        elif vsagge[0] == "#gR":
            vsagge = vsagge.pop(0)
            message = ''.join(vsagge)
            register_sala_usuario(message, id_usuario)

        # eR. Salir de la sala en que se encuentra. El servidor enviara al cliente a la sala por defecto. Si el cliente
        # ingresa este comando estando en la sala por defecto, no tendra ningun efecto.
        elif vsagge[0] == "#eR":
            del_usuario_sala(id_usuario)

        # exit. Desconectara al cliente del servidor
        elif vsagge[0] == "#exit":
            del_usuario_sala(id_usuario)
            print("Conexion terminada")
            conn.close()
        # lR Lista los nombres de todas las sala disponibles y el numero de participantes de cada una.
        elif vsagge[0] == "#IR":
            vsagge = vsagge.pop(0)
            message = ''.join(vsagge)
            salas_usuarios()

        # dR <nombreSala>. Elimina la sala nombreSala. Un cliente solo puede eliminar las salas que creo.
        elif vsagge[0] == "#dR":
            delete_sala(vsagge[1])

        # show users: Muestra el listado el todos los usuarios en todo el sistema
        elif vsagge[0] == "#show":
            print(show_users())
        # \private<nombreusuario>: Envia un mensaje privado a un usuario determinado sin importar en que sala se encuentre
        elif vsagge[0] == "/private":
            message = str(id_sala[0]) + " dice: " + message
        elif vsagge[0] == "MSG:":
            id_sala = select_sala_user(user_id[0])
            if id_sala != None:
                message = str(id_sala[0]) + " dice: " + message
            else:
                message = "0 " + message
            print(message)
            conn.sendall(message)

        else:
            if message == "console":
                break
            print (conn, "user:  ", message)
            conn.send("password".encode('ascii'))
            password = conn.recv(819)
            print ("pass: ", password)
            user_id = login(str(message), str(password))
            print("USER ID: ", user_id)
            if user_id != None:
                print ("logueado con exito")
                conn.send("log-ex".encode('ascii'))
            else:
                print ("alguno de los campos es incorrecto")
                conn.send("registro".encode('ascii'))
                response = conn.recv(816)
                if(response == "y"):
                    conn.send("nombre: ")
                    nombre = conn.recv(819)
                    conn.send("apellido: ")
                    apellido = conn.recv(819)
                    conn.send("email: ")
                    email = conn.recv(819)
                    conn.send("password: ")
                    password = conn.recv(819)
                    conn.send("edad: ")
                    edad = conn.recv(819)
                    conn.send("genero(m/f): ")
                    genero = conn.recv(819)
                    print("Se registra", (nombre, apellido,
                          edad, genero, email, password))
                    register(apellido, nombre, edad, genero, email, password)

    conn.close()


def main():
    try:
        host = 'localhost'
        port = 8000
        tot_socket = 4
        list_sock = []
        for i in range(tot_socket):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port+i))
            s.listen(10)
            list_sock.append(s)
            print ("|--| Server listening on %s %d" % (host, (port+i)))
        while 1:
            for j in range(len(list_sock)):
                conn, addr = list_sock[j].accept()
                print ('|--| Connected with ' + addr[0] + ':' + str(addr[1]))
                start_new_thread(clientthread, (conn,))
        s.close()

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
