from socket import *
import sys
import time
import _thread

proxySocket = socket(AF_INET, SOCK_STREAM)
port = 3406
proxySocket.bind(("", port))

proxySocket.listen(1)

try:
    print(f'\nProxy Server ready to serve...\n')
    while True:

        client, addr = proxySocket.accept()
        try:
            webserverSocket = socket(AF_INET, SOCK_STREAM)
            webserverSocket.connect(("", 3405))
            data = client.recv(2048).decode()
            # print(f'request:\n\t{data}')
            webserverSocket.sendall(data.encode())
            response = webserverSocket.recv(2048).decode()
            print(f'proxy-forward, server, {_thread.get_ident()}, {time.strftime("%H:%M:%S", time.localtime())}')
            # print(f'response:\n\t{response}')
            client.sendall(response.encode())
            time.sleep(3)
            print(f'proxy-forward, client, {_thread.get_ident()}, {time.strftime("%H:%M:%S", time.localtime())}\n')
            client.close()
            webserverSocket.close()
        except:
            client.close()
            webserverSocket.close()
            
except KeyboardInterrupt:
    proxySocket.close()

    sys.exit()

proxySocket.close()