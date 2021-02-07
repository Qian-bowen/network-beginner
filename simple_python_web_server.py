#import socket module
import socket
import re
from threading import Thread

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#Prepare a sever socket 
port=10000
serverSocket.bind(('',port))
serverSocket.listen(10)
threads=[]

def file_type(filename):
    print(filename[1:])
    if re.match('.*html',filename):
        ctype='text/html'
    elif re.match('.*PNG',filename):
        ctype='image/png'
    elif re.match('.*xml',filename):
        ctype='text/xml'
    elif re.match('.*jpg',filename):
        ctype='image/jpeg'
    print(ctype)
    return ctype


def newRequest(connectionSocket):
    print ('Ready to serve...')     
    try:         
        message = connectionSocket.recv(1024)
        filename = message.split()[1] 
        #注意python split函数的特性 分割后第二行第一个字符是\n  
        ctype=file_type(filename[1:].decode('utf-8'))
        
        

        f=open(filename[1:],'rb')
        outputdata = f.read()
       
        #Send one HTTP header line into socket 
        header= 'HTTP/1.1 200 OK\nConnection:close\nContent-Length:%d\nContent-Type:%s\n\n'%(len(outputdata),ctype)
        connectionSocket.send(header.encode())


        #Send the content of the requested file to the client
        connectionSocket.send(outputdata)
        connectionSocket.close()
    except IOError:
        #Send response message for file not found
        header=' HTTP/1.1 404 Not Found'
        connectionSocket.send(header.encode())

        #Close client socket
        connectionSocket.close()  
    

while True:
    #establish the connection
    connectionSocket, addr =  serverSocket.accept()
    #create a new thread
    newThread=Thread(target=newRequest,args=(connectionSocket,))
    newThread.start()
    threads.append(newThread)
    

serverSocket.close()