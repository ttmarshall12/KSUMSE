import socket
import os.path
import Users
import sqlite3
import random
import threading
from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler, BaseRequestHandler
import ssl
import DataManager
import Database
import time
import sys
import pickle


######### Global Variables ##########
Running = True
usersLoaded = False
userList = []
currentUser = ""
commandCallback = {}
userOptionCallback = {}
server = ""

def getRandomID():
   range_start = 10**(5)
   range_end = (10**6)-1
   return random.randint(range_start, range_end)
 
class ThreadedTCPRequestHandler(StreamRequestHandler):
   
   def handle(self):
      
      data = self.connection.recv(4096)
      data = pickle.loads(data)
       
      Authenticator = DataManager.Authenticator(data, Database.Database('tfms.db'))
        
      if Authenticator.Authenticated() and Authenticator.Permitted():
         print("Data authenticated...")
         
         print(data[0])
         
         dispatch = DataManager.Dispatcher(data, Database.Database('tfms.db'))
         response = dispatch.ExecuteCommand()
         
      else:
      
         if not Authenticator.Authenticated():
            print("Data NOT authenticated...")
            response = "AuthenticationFail"
         elif not Authenticator.Permitted():
            print ("Incorrect permissions...")
            response = "PermissionFail"
         else:
            print ("Unknown fail...")
            response = "UnknownFail"
        
        
      cur_thread = threading.current_thread()
      print (cur_thread)
      print("data received: " + ' '.join(data))

      self.wfile.write(response)


class SSL_TCPServer(TCPServer):
   def __init__(self,
                server_address,
                RequestHandlerClass,
                certfile,
                keyfile,
                ssl_version=ssl.PROTOCOL_TLSv1,
                bind_and_activate=True):
        TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version

   def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                 server_side=True,
                                 certfile = self.certfile,
                                 keyfile = self.keyfile,
                                 ssl_version = self.ssl_version)
        return connstream, fromaddr

        
class SSL_ThreadingTCPServer(ThreadingMixIn, SSL_TCPServer): pass    
    


   
HOST, PORT = "192.168.0.162", 50021
print('Track & Field Meet Server Starting....')

server = SSL_ThreadingTCPServer((HOST,PORT),ThreadedTCPRequestHandler,"TFMS.crt","TFMS.key")


ip, port = server.server_address

# Start a thread with the server -- that thread will then start one
# more thread for each request
server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print("Server loop running in thread:", server_thread.name)   
 
