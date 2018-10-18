import socket, json, sys
from threading import Thread

def receive():
    while(active):
        data_received = sock.recv(4096)
        if(sys.getsizeof(data_received) != 33):
            data_received = json.loads(data_received.decode())
            message_received = data_received.get('mensaje_cliente')
            print('')
            print(message_received)

def send():
    global active
    while(active):
        string = input()
        data = json.dumps({'mensaje_cliente': string})
        sock.send(data.encode())
        if(string==close_word):
            active = False

#HOST AND PORT INFO
host = '127.0.0.1'
port = 8888

#VARIABLES
close_word = 'exit'
active = True

#tu nombre
print('Antes de comenzar, escribe tu nombre... ')
name = input()

sock = socket.socket()
sock.connect((host, port))
#envia el nombre
data = json.dumps({'name': name})
sock.send(data.encode())

#crea los hilos manejados por el cliente
receive_thread = Thread(target=receive)
receive_thread.start()
send_thread = Thread(target=send)
send_thread.start()

receive_thread.join()
send_thread.join()
sock.close()
