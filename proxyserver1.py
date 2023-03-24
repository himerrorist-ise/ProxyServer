from socket import *
import sys


if "__main__" == __name__:
    port = 3406

    proxySocket = socket(AF_INET, SOCK_STREAM)
    proxySocket.bind(("", port))

    proxySocketServer = socket(AF_INET, SOCK_STREAM)
    proxySocketServer.connect(("", 3405))
    
    try:
        proxySocket.listen(1)
        print(f'\nServer has been started. Now listening...')

        while True:
            client, address = proxySocket.accept()
            print(f'\nConnected to the client {address}\n')
            data = client.recv(2048).decode()
            proxySocketServer.send(data.encode())
            response = proxySocketServer.recv(2048).decode()
            print(response)
            client.send(response.encode())


    except KeyboardInterrupt:
        print(f'\nConnection closed with the server {proxySocketServer.getsockname()}')
        proxySocket.close()
        proxySocketServer.close()
        sys.exit()

    proxySocket.close()
    proxySocketServer.close()