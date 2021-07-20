
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager


import psycopg2
from psycopg2 import pool


postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="fxjzjfkzoyuffb",
                                                    password="6a54799b50cb8f80b9b2940a5753bca332d3c9c74bb1993f187ecb1cd0082f0e",
                                                    host="ec2-35-173-114-25.compute-1.amazonaws.com",
                                                    port="5432",
                                                    database="d2f7enckmqnqc")
ps_connection = 0



def contextmanager():
    try:
        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
    

def prueba():
    try:
        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        
    if (ps_connection):
        print("successfully recived connection from connection pool ")
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("select * from usuario")
        mobile_records = ps_cursor.fetchall()

        print("Displaying rows from mobile table")
        for row in mobile_records:
            print(row)

        ps_cursor.close()

        postgreSQL_pool.putconn(ps_connection)
        print("Put away a PostgreSQL connection")
        try:
            if (postgreSQL_pool):
                print("BD Connect")
            ps_connection = postgreSQL_pool.getconn()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)
        



def login(email,password):
    try:
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
          
    if (ps_connection):
        ps_cursor = ps_connection.cursor()
        data = [email,password]
        ps_cursor.execute("SELECT (user_id) from usuario where email = %s and password = %s; ",data)
        mobile_records = ps_cursor.fetchone()       

        ps_cursor.close()
        postgreSQL_pool.putconn(ps_connection)
        print("id_usuario: ",mobile_records)
        return(mobile_records)


def register(nombre,apellido,edad,genero,email,password):
    try:

        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
          
    if (ps_connection):
        ps_cursor = ps_connection.cursor()
        data = [nombre,apellido,email,password,email,edad,genero]
        ps_cursor.execute("INSERT INTO usuario values(nextval('sec_users'),%s,%s,%s,%s,%s,%s,%s) returning email; ",data)
        mobile_records = ps_cursor.fetchone()
        ps_connection.commit()

        ps_cursor.close()
        postgreSQL_pool.putconn(ps_connection)

    return mobile_records

def getnumsalas():
    try:

        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        
    if (ps_connection):
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("SELECT MAX(id) from salas")
        mobile_records = ps_cursor.fetchone()

        ps_cursor.close()
        postgreSQL_pool.putconn(ps_connection)
        return (mobile_records + 1)

def register_sala(id,nombre):
    try:

        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

            
        if (ps_connection):
            ps_cursor = ps_connection.cursor()
            data = [id,nombre]
            ps_cursor.execute("INSERT INTO salas values(%s,%s) returning id",data)
            mobile_records = ps_cursor.fetchone()
            ps_connection.commit()
            ps_cursor.close()
            return mobile_records
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)


def register_sala_usuario(id_sala,id_usuario):
    try:

        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        
    if (ps_connection):
        ps_cursor = ps_connection.cursor()
        data = [id_sala,id_usuario]
        ps_cursor.execute("INSERT INTO usuario_salas values(%s,%s) returning id; ",data)
        mobile_records = ps_cursor.fetchone()
        ps_connection.commit()
        ps_cursor.close()
        postgreSQL_pool.putconn(ps_connection)

def del_usuario_sala(id_usuario):
    try:

        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        
    if (ps_connection):
        ps_cursor = ps_connection.cursor()
        data = [id_usuario]
        ps_cursor.execute("DELETE * FROM usuario_salas WHERE id_usuario = (%s); ",data)
        mobile_records = ps_cursor.fetchone()

        ps_cursor.close()
        postgreSQL_pool.putconn(ps_connection)

def salas_usuarios():
    try:
        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        
    if (ps_connection):
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("SELECT salas.nombre, count(usuario_salas.id_usuario) FROM usuario_salas INNER JOIN salas ON salas.id = usuario_salas.id_sala GROUP BY nombre")
        mobile_records = ps_cursor.fetchone()
        ps_cursor.close()
        postgreSQL_pool.putconn(ps_connection)
        return mobile_records

def select_sala_user(id_usuario):
    try:
        if (postgreSQL_pool):
            print("BD Connect")
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        
    if (ps_connection):
        ps_cursor = ps_connection.cursor()
        data = [id_usuario]
        ps_cursor.execute("SELECT id_sala from usuario_salas where id_usuario = (%s)", data)
        mobile_records = ps_cursor.fetchone()
        ps_cursor.close()
        postgreSQL_pool.putconn(ps_connection)
        return mobile_records

def user_in_sala(id_usuario,id_sala):
    try:
        ps_connection = postgreSQL_pool.getconn()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error while connecting to PostgreSQL", error)
        
    if (ps_connection):
        ps_cursor = ps_connection.cursor()
        data = [id_usuario,id_sala]
        ps_cursor.execute("SELECT id from usuario_salas where (id_usuario = (%s) and id_sala = (%s))", data)
        mobile_records = ps_cursor.fetchone()
        ps_cursor.close()
        postgreSQL_pool.putconn(ps_connection)
        return mobile_records





