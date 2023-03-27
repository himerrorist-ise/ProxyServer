from socket import *
import sys
import _thread
import time

port = 3406
proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.bind(("", port))

flag = False
threadId = 0

cacheData = dict()

def threadFunc(conn):
    global flag
    global threadId
    threadId += 1
    global cacheData

    try:
        webserverSocket = socket(AF_INET, SOCK_STREAM)
        data = conn.recv(2048).decode()
        filename = data.split()[1][1:]
        if cacheData.keys().__contains__(filename) and (time.time() - cacheData[filename][1] < 10 ):
            # conn.send("HTTP/1.1 200 OK\r\n".encode())
            # conn.send("Content-Type: text/html\r\n".encode())
            conn.sendall(cacheData[filename][0].encode())
            # time.sleep(4)
            print(f'proxy-cache, client, {_thread.get_ident()}, {time.strftime("%H:%M:%S", time.localtime())}\n')
        else:
            webserverSocket.connect(("", 3405))
            webserverSocket.sendall(data.encode())
            response = webserverSocket.recv(2048).decode()
            # time.sleep(5)
            print(f'\nproxy-forward, server, {_thread.get_ident()}, {time.strftime("%H:%M:%S", time.localtime())}')
            cacheData[filename] = [response, time.time()]
            conn.sendall(response.encode())
            time.sleep(4)
            print(f'proxy-forward, client, {_thread.get_ident()}, {time.strftime("%H:%M:%S", time.localtime())}\n')
        conn.close()
        webserverSocket.close()
    except KeyboardInterrupt:
        conn.close()
        webserverSocket.close()
        flag = True
    except:
        conn.close()
        webserverSocket.close()

    _thread.exit()

try:
    proxySocket.listen(10)
    print(f'\nProxy Server Started...\n')

    while not flag:
        client, addr = proxySocket.accept()
        # print(f'\r\nCurrent number of threads { _thread._count()}\r\n')
        _thread.start_new_thread(threadFunc, (client, ))
        time.sleep(0.5)
        # print(f'\n\n{cacheData}\n\n')

except KeyboardInterrupt:
    proxySocket.close()
    sys.exit()

proxySocket.close()