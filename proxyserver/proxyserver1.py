from socket import *
import sys
import time

proxySocket = socket(AF_INET, SOCK_STREAM)
port = 3406
proxySocket.bind(("", port))

proxySocket.listen(1)

try:
    while True:

        print(f'Proxy Server ready to serve...')
        client, addr = proxySocket.accept()
        try:
            webserverSocket = socket(AF_INET, SOCK_STREAM)
            webserverSocket.connect(("", 3405))
            data = client.recv(2048).decode()
            # print(f'request:\n\t{data}')
            print(f'proxy-forward, server, 1, {time.strftime("%H:%M:%S", time.localtime())}')
            webserverSocket.sendall(data.encode())
            response = webserverSocket.recv(2048).decode()
            # print(f'response:\n\t{response}')
            print(f'proxy-forward, client, 1, {time.strftime("%H:%M:%S", time.localtime())}')
            client.sendall(response.encode())
            client.close()
            webserverSocket.close()
        except:
            client.close()
            webserverSocket.close()
            
except KeyboardInterrupt:
    proxySocket.close()

    sys.exit()

proxySocket.close()