import socket
#import rsa
import os.path
import Users
import pickle
import xml.etree.ElementTree as ET
import sqlite3
import random
import threading
from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler, BaseRequestHandler
import ssl
import DataManager
import Database


######### Global Variables ##########
Running = True
usersLoaded = False
userList = []
userRoot = ET.Element("users")
currentUser = ""
commandCallback = {}
userOptionCallback = {}


########## SQL DB #######################
#dbConn = sqlite3.connect('tfms.db')
#dbCur = dbConn.cursor()
tfmsDB = Database.Database('tfms.db')

#####################################
def getRandomID():
   range_start = 10**(5)
   range_end = (10**6)-1
   return random.randint(range_start, range_end)

#def SetupDB():
   #global dbCur
   #global dbConn
   
   #dbCur.execute('CREATE TABLE IF NOT EXISTS users (type TEXT, name TEXT, id INT)')
   #dbCur.execute('CREATE TABLE IF NOT EXISTS events (name TEXT)')

def Login():
   global currentUser
   
   if currentUser == "":
      print('Logging in....')
      name = raw_input("Enter name: ")
      ID = raw_input("Enter ID: ")
      
      Match = tfmsDB.GetAdmin(name, ID)
      
      if Match != None:
          
         print("Welcome back " + name + "!!!!!!!")
         currentUser = Match
               
      else :
         print("Unknown user....")
         
   else:
      print('Logging out....')
      currentUser = ""
 
 
def Shutdown():
   print('Shutting down...')
   global Running
   Running = False

def typeLookup(type):
   if type == 'ad':
      return "admin"
   elif type == 'o':
      return "official"
   elif type == 'c':
      return "coach"
   elif type == 'at':
      return "athlete"
   else:
      return None
   
def PrintUsers():
   dbCur.execute('SELECT * FROM users ORDER BY name ASC')
   
   while True:
      row = dbCur.fetchone()
      if row == None:
         break
      print(row)

def AddUser():
   
   addingUsers = True
   
   while(addingUsers):
      name = raw_input("Enter User Name: ")
      id = raw_input("Enter User ID or type ? to autogenerate: ")
      type = raw_input("Enter User type\n"+
                       "ad - admin\n" +
                       "o  - oficial\n" +
                       "c  - coach\n" +
                       "at - athlete\n")
                       
      userType = typeLookup(type)
      
      if id == '?':
         id = getRandomID()
      
      if userType != None:
         dbCur.execute('INSERT INTO users(type, name, id) VALUES (?, ?, ?)', (userType, name, id))
         dbConn.commit()
      else:
         print("Failed to add user...")
         
      addAnother = raw_input("Add another user (y/n)? ")
      
      if addAnother != 'y':
         addingUsers = False
         
def RemoveUser(name):
   dbCur.execute('SELECT * FROM users WHERE name = ?', (name,))
   
   user = dbCur.fetchone()
   
   if user != None:
      #accept = raw_input('Sure you want to remove' + user[0] + user[1] + user[2] + ' (y/n)? ')
      #accept = raw_input('Sure you want to remove' + str(user) + ' (y/n)? ')
      #if accept == 'y':
      dbCur.execute('DELETE FROM users WHERE type = ? AND name = ? AND id = ?', (user[0], user[1], user[2]))
      dbConn.commit()
      return True
      #else:
         #print('Cancelling removal....')
   else:
      #print("User doesn't exist...")
      return False
   
def RemoveUserOption():
   PrintUsers()
      
   name = raw_input('Enter name of user to be removed: ')
   Success = RemoveUser(name)
   
   
def ModifyUser():
   PrintUsers()
   
   name = raw_input('Enter name of user to be modified: ')
   
   dbCur.execute('SELECT * FROM users WHERE name = ?', (name,))
   
   user = dbCur.fetchone()
   
   if user != None:
      modifiedUser = {}
      modifiedUser['type'] = user[0]
      modifiedUser['name'] = user[1]
      modifiedUser['id']   = user[2]
      
      field = raw_input('Enter the field you want to modify: ')
      value = raw_input('Enter the new value: ')
      modifiedUser[field] = value
      
      dbCur.execute('UPDATE users SET type = ?, name = ?, id = ? WHERE type = ? AND name = ? AND id = ?', \
         (modifiedUser['type'], modifiedUser['name'], modifiedUser['id'], user[0], user[1], user[2]))
      
      dbConn.commit()
      
   else:
      print("User doesn't exist...")

   
def UserOptions():
   print("Please select one of the following user options...")
   command = raw_input("1  - Add User\n" +
                       "2  - Remove User\n" +
                       "3  - Modify User\n")
   
   if int(command) >= 1 and int(command) <= 3: 
      userOptionCallback[command]()
   else:
      print("Invalid command....")
   
def MeetSetup():
   print('Meet setup...')
   
   
def MeetManagement():
   print('Meet management...')
 
 
def RegisterCallbacks():
   commandCallback['1'] = Login
   commandCallback['2'] = UserOptions
   commandCallback['3'] = MeetSetup
   commandCallback['4'] = MeetManagement
   commandCallback['0'] = Shutdown
   
   userOptionCallback['1'] = AddUser
   userOptionCallback['2'] = RemoveUserOption
   userOptionCallback['3'] = ModifyUser
   

def LoadAdmin():
   global tfmsDB
   allAdmin = tfmsDB.GetAllAdmin()
   print(allAdmin)
   if len(allAdmin) != 0:
      print("Admin exists currently...")
      return True
      
   else:
      print("Must create an admin account....")
      name = raw_input("Please enter admin name: ")
      ID = raw_input("Please enter admin ID: ")
      
      print("Creating admin....")
      
      tfmsDB.AddUser('admin', name, ID)
      
      return True
 

def acceptCommands():
   if currentUser == "":
      print("Please select one of the following commands...")
      command = raw_input("1  - Login\n" +
                          "0  - Shutdown\n")
        
      if int(command) >= 0 and int(command) <= 1: 
         commandCallback[command]()
      else:
         print("Invalid command....")
                        
   else:
      print("Please select one of the following commands...")
      command = raw_input("1  - Logout\n" +
                          "2  - User Options\n" +
                          "3  - Meet Setup\n"
                          "4  - Meet Mangement\n"
                          "0  - Shutdown\n")
                          
      if int(command) >= 0 and int(command) <= 4: 
         commandCallback[command]()
      else:
         print("Invalid command....")
 
# class testHandler(StreamRequestHandler):
    # def handle(self):
       # data = self.connection.recv(4096)
        # self.wfile.write(data)
 
 
class ThreadedTCPRequestHandler(BaseRequestHandler):
   
   def handle(self):
      data = self.request.recv(10240)
        
      Authenticator = DataManager.Authenticator(data)
        
      # if Authenticator.Authenticated():
         # print("Data authenticated...")
         
         # Decryptor = DataManager.Decryptor(data)
         
         # dispatch = DataManager.Dispatcher(Decryptor.Decrypt("tempkey"))
         
      # else:
         # print("Data NOT authenticated...")
        
        
      
      cur_thread = threading.current_thread()
      response = "{}: {}".format(cur_thread.name, data)
      self.request.sendall(response)


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
    
    
# class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    # pass    
    
# def client(ip, port, message):
    # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.connect((ip, port))
    # try:
        # sock.sendall(message)
        # response = sock.recv(10240)
        # print "Received: {}".format(response)
    # finally:
        # sock.close()
        
def client(ip, port, message):
   s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
   ssl_sock = ssl.wrap_socket(s,
                              ca_certs="TFMS.crt",
                              cert_reqs=ssl.CERT_REQUIRED,
                              ssl_version=ssl.PROTOCOL_TLSv1)
   ssl_sock.connect((ip,port))
   try:
      ssl_sock.send(message)
      response = ssl_sock.recv(4096)
      print "Received: {}".format(response)
   finally:
      ssl_sock.close()
      
 
def main():
   global Running
   global usersLoaded
   
   print('Track & Field Meet Server Starting....')
   #print('Setting up DB...')
   
   #SetupDB()
   
   while (Running == True):
      
      if not usersLoaded:
         usersLoaded = LoadAdmin()
         RegisterCallbacks()

      else:
         acceptCommands()
         
      #print("Run status is " + str(Running))
  
  
# Port 0 means to select an arbitrary unused port
HOST, PORT = "192.168.0.162", 50021

#MySSL_ThreadingTCPServer(('127.0.0.1',5151),testHandler,"cert.pem","key.pem").serve_forever()
server = SSL_ThreadingTCPServer((HOST,PORT),ThreadedTCPRequestHandler,"TFMS.crt","TFMS.key")


#server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
ip, port = server.server_address

# Start a thread with the server -- that thread will then start one
# more thread for each request
server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print("Server loop running in thread:", server_thread.name)   
 
 
main()


client(ip, port, "Hello World 1")
client(ip, port, "Hello World 2")
client(ip, port, "Hello World 3")

server.shutdown()
server.server_close()   
