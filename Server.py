import socket
import threading

host = socket.gethostname()
port = 8888

# membuat socket
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ServerSocket.bind((host, port)) #binding socket
ServerSocket.listen()
clients = [] #empty list for client
aliases = [] #list for nickname


def Broadcast(message, currentClient):
    file = open("chatHistory.txt", "a")
    file.write(str(message) + "\n")
    for client in clients:
       if(client != currentClient):
           client.send(message)


def handleClient(client):
    while True:
        try:
            #membaca input
            message = client.recv(5024)
            Broadcast(message, client)
            print(message)

        except:
            #remove client that is not related anymore
            index = clients.index(client)
            clients.remove(client)
            client.close()

            alias = aliases[index]
            leftMessage = (f'{alias} has left the chat room'.encode('utf-8'))
            Broadcast(leftMessage, 0)
            aliases.remove(alias)
            break

def receive():
    while True:
        print('Server is running')
        client, address = ServerSocket.accept()
        print('Connected with: '+str(address))
        client.send('alias?'.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)

        index = clients.index(client)
        connectedMessage = (f'{alias} is connected'.encode('utf-8'))
        print(connectedMessage)
        Broadcast(f'{alias} has connected to the chat room'.encode('utf-8'), 0)
        client.send('you are now connected'.encode('utf-8'))
        thread = threading.Thread(target = handleClient, args=(client, ))
        thread.start()


if __name__ == "__main__":
    receive()