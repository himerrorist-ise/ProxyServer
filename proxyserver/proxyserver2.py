from socket import *
import sys
import _thread
import time

port = 3406
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind(("", port))

flag = False
threadId = 0

def threadFunc(conn):
    global flag
    global threadId
    threadId += 1

    try:
        webserverSocket = socket(AF_INET, SOCK_STREAM)
        webserverSocket.connect(("", 3405))
        data = conn.recv(2048).decode()
        # print(f'request:\n\t{data}')
        print(f'\nproxy-forward, server, {_thread.get_ident()}, {time.strftime("%H:%M:%S", time.localtime())}')
        webserverSocket.sendall(data.encode())
        response = webserverSocket.recv(2048).decode()
        # print(f'response:\n\t{response}')
        print(f'proxy-forward, client, {_thread.get_ident()}, {time.strftime("%H:%M:%S", time.localtime())}\n')
        conn.sendall(response.encode())
        time.sleep(0.5)
        conn.close()
        webserverSocket.close()
    except KeyboardInterrupt:
        conn.close()
        webserverSocket.close()
        flag = True
    except:
        conn.close()
        webserverSocket.close()

    return

try:
    proxySocket.listen(10)
    print(f'\nProxy Server Started...\n')

    while not flag:
        client, addr = proxySocket.accept()
        print(f'\r\nCurrent number of threads { _thread._count()}\r\n')
        _thread.start_new_thread(threadFunc, (client, ))

except KeyboardInterrupt:
    proxySocket.close()
    sys.exit()

proxySocket.close()