#import socket module
from socket import *

# create an IPv4 TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a sever socket
serverSocket.bind(("localhost", 6789))

# Listen for connections from client
serverSocket.listen(1)

while True:
    # Establish the connection
    print ("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024)
        message_split = message.split()
        if len(message_split) <= 1:
            # Small connection from browser - ignore
            connectionSocket.close()
            continue
            
        filename = message_split[1]
        f = open(filename[1:], "rb")
        outputdata = f.read()
        
        # Send the first HTTP header line into socket
        connectionSocket.send(b'HTTP/1.1 200 OK \r\n\r\n')
        
        # Send the content of the requested file to the client
        connectionSocket.send(outputdata)
        
        # Close client socket
        connectionSocket.close()      
    except IOError:
        # Send response message for file not found
        connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n\r\n')
        connectionSocket.send(b'<html><head></head><body><h1>404 Not Found</h1></body></html>')
                
        # Close client socket
        connectionSocket.close()
    except KeyboardInterrupt:
        # User pressed Ctrl+C, exit gracefully
        break
        
# Close server connection
serverSocket.close()
