from socket import *
import sys
from _thread import *
import base64

port = 3405

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", port))

flag = False

def threadedClient(conn):
  global flag
  
  try:
      
    data = conn.recv(2048).decode()

    filename = data.split()[1]
    filetype = filename.split(".")[1]

    # print(data)
    if (filetype != "html"):
      conn.close()
      return
    with open(filename[1:], 'r') as f:

      lines = f.readlines()
      
      conn.send("HTTP/1.1 200 OK\r\n".encode())
      conn.send("Content-Type: text/html\r\n".encode())

      for i in range(0, len(lines)):
        conn.send(lines[i].encode())
      conn.send("\r\n".encode())

  except KeyboardInterrupt:
      flag = True

  conn.close()
  # print("Connection closed!\n\nNow Listening...")
  return

try:
  serverSocket.listen()
  print("\nServer has been started. Now listening...")
  while not flag:
    client, address = serverSocket.accept()

    # print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threadedClient, (client,))
    
    
except KeyboardInterrupt:
    serverSocket.close()
    sys.exit()

serverSocket.close()