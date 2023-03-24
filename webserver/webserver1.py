# import socket module
from socket import *

# In order to terminate the program
import sys

# Prepare a sever socket
serverSocket = socket(AF_INET, SOCK_STREAM)
### YOUR CODE HERE ###
portNum = 3405

serverSocket.bind(("", portNum))

serverSocket.listen(1)

try:

  while True:
      # Establish the connection
      print('Ready to serve...')

      ### YOUR CODE HERE ###
      connectionSocket, addr = serverSocket.accept()

      try:
          ### YOUR CODE HERE ###
          message = connectionSocket.recv(2048).decode()
          # print(message)
          filename = message.split()[1]
          with open(filename[1:], 'r') as f:
            ### YOUR CODE HERE ###
            outputdata = f.readlines()

          # Send one HTTP header line into socket
          ### YOUR CODE HERE ###
          connectionSocket.send(("HTTP/1.1 200 OK\r\n").encode())
          connectionSocket.send("Content-Type: text\html\r\n".encode())
          # connectionSocket.send("\r\n".encode())

          # Send the content of the requested file into socket
          for i in range(0, len(outputdata)):
              connectionSocket.send(outputdata[i].encode())
          connectionSocket.send("\r\n".encode())

          # Close client socket
          connectionSocket.close()
      except IOError:
          # Send response message for file not found
          ### YOUR CODE HERE ###
          connectionSocket.send(("HTTP/1.1 404 Not Found\r\n").encode())

          # Close client socket
          ### YOUR CODE HERE ###
          connectionSocket.close()
      except:
         connectionSocket.close()
          
except KeyboardInterrupt:
  
  # Close server socket
  serverSocket.close()

  # Terminate the program after sending the corresponding data
  sys.exit()

serverSocket.close()