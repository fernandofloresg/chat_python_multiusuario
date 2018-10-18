import socket, json, sys
from threading import Thread
host = '127.0.0.1'
port = 8888
connections = [] #lista de conexiones

def accept_connections():
    while 1:
        conn, addr = sock.accept()
        print('%s se ha conectado', addr)
        connections.append(conn)
        Thread(target=handle_client, args=(conn,)).start()

def handle_client(conn):
    data = conn.recv(4096)
    name = json.loads(data.decode()).get('name')
    message = 'Bienvenido, si quieres salir escribe exit'
    data = json.dumps({'mensaje_cliente' : message})
    conn.send(data.encode())
    while 1:
        data = conn.recv(4096)
        if(sys.getsizeof(data) != 33):
            data = json.loads(data.decode())
            message = name + ':' + data.get('mensaje_cliente')
            if(message != 'exit'):
                broadcast(message, conn)
            else:
                conn.close()
                connections.remove(conn)
                broadcast('Se ha salido ' + name, conn)
                break


def broadcast(message, connection): #manda mensajes a todas las conexones
    data = json.dumps({'mensaje_cliente' : message}).encode()
    for conn in connections:
        if(conn != connection):
            try:
                conn.send(data)
            except BrokenPipeError:
                connections.remove(conn)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket creado')
    sock.bind((host, port))
    sock.listen(4)
    print('Esperando conecciones ... ')
    accept_thread = Thread(target = accept_connections)
    accept_thread.start()
    accept_thread.join()
    sock.close()
