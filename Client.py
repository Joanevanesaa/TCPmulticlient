import threading
import socket
alias = input('What is your name?')
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 8888

ClientSocket.connect((host, port))

def clientReceive():
    while True:
        try:
            message = ClientSocket.recv(5024).decode('utf-8')
            if message == 'alias?':
                ClientSocket.send(alias.encode('utf-8'))
            else:
                print(message)
        except:
            print('error')
            ClientSocket.close()
            break

    while True:
        message = '{}: {}'.format(alias, input(""))
        ClientSocket.send(message.encode('utf-8'))


receive_Thread = threading.Thread(target = clientReceive)
receive_Thread.start()

send_Thread = threading.Thread(target=clientSend)
send_Thread.start()

