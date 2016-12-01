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

########## SQL DB #######################
#dbConn = sqlite3.connect('tfms.db')
#dbCur = dbConn.cursor()
#tfmsDB = Database.Database('tfms.db')

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
   
def Get_Input(message):
   print(message)
   input = ""
   char = ""
   
   while char != "\n":
      print("Getting input...\n")
      char = sys.stdin.read()
      
      if char != "":
         input = input + char
   
   return input.rstrip()

def Login():
   global currentUser
   tfmsDB = Database.Database('tfms.db')

   if currentUser == "":
      print('Logging in....')
      name = Get_Input("Enter name: ")
      ID = Get_Input("Enter ID: ")
      
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
      name = Get_Input("Enter User Name: ")
      id = Get_Input("Enter User ID or type ? to autogenerate: ")
      type = Get_Input("Enter User type\n"+
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
         
      addAnother = Get_Input("Add another user (y/n)? ")
      
      if addAnother != 'y':
         addingUsers = False
         
def RemoveUser(name):
   dbCur.execute('SELECT * FROM users WHERE name = ?', (name,))
   
   user = dbCur.fetchone()
   
   if user != None:
      #accept = Get_Input('Sure you want to remove' + user[0] + user[1] + user[2] + ' (y/n)? ')
      #accept = Get_Input('Sure you want to remove' + str(user) + ' (y/n)? ')
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
      
   name = Get_Input('Enter name of user to be removed: ')
   Success = RemoveUser(name)
   
   
def ModifyUser():
   PrintUsers()
   
   name = Get_Input('Enter name of user to be modified: ')
   
   dbCur.execute('SELECT * FROM users WHERE name = ?', (name,))
   
   user = dbCur.fetchone()
   
   if user != None:
      modifiedUser = {}
      modifiedUser['type'] = user[0]
      modifiedUser['name'] = user[1]
      modifiedUser['id']   = user[2]
      
      field = Get_Input('Enter the field you want to modify: ')
      value = Get_Input('Enter the new value: ')
      modifiedUser[field] = value
      
      dbCur.execute('UPDATE users SET type = ?, name = ?, id = ? WHERE type = ? AND name = ? AND id = ?', \
         (modifiedUser['type'], modifiedUser['name'], modifiedUser['id'], user[0], user[1], user[2]))
      
      dbConn.commit()
      
   else:
      print("User doesn't exist...")

   
def UserOptions():
   print("Please select one of the following user options...")
   command = Get_Input("1  - Add User\n" +
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
   tfmsDB = Database.Database('tfms.db')
   allAdmin = tfmsDB.GetAllAdmin()
   print(allAdmin)
   if len(allAdmin) != 0:
      print("Admin exists currently...")
      return True
      
   else:
      print("Must create an admin account....")
      name = Get_Input("Please enter admin name: ")
      ID = Get_Input("Please enter admin ID: ")
      
      print("Creating admin....")
      
      tfmsDB.AddUser('admin', name, ID)
      
      return True
 

def acceptCommands():
   if currentUser == "":
      print("Please select one of the following commands...")
      command = Get_Input("1  - Login\n" +
                          "0  - Shutdown\n")
        
      if int(command) >= 0 and int(command) <= 1: 
         commandCallback[command]()
      else:
         print("Invalid command....")
                        
   else:
      print("Please select one of the following commands...")
      command = Get_Input("1  - Logout\n" +
                          "2  - User Options\n" +
                          "3  - Meet Setup\n"
                          "4  - Meet Mangement\n"
                          "0  - Shutdown\n")
                          
      if int(command) >= 0 and int(command) <= 4: 
         commandCallback[command]()
      else:
         print("Invalid command....")
 
 
class ThreadedTCPRequestHandler(StreamRequestHandler):
   
   def handle(self):
      
      data = self.connection.recv(4096)
      data = pickle.loads(data)
      
      # data = self.request.recv(10240)
        
      Authenticator = DataManager.Authenticator(data)
        
      if Authenticator.Authenticated():
         print("Data authenticated...")
         
         #Decryptor = DataManager.Decryptor(data)
         
         print(data[0])
         
         dispatch = DataManager.Dispatcher(data, Database.Database('tfms.db'))
         dispatch.ExecuteCommand()
         
      else:
         print("Data NOT authenticated...")
        
        
      cur_thread = threading.current_thread()
      print (cur_thread)
      print("data received: " + ' '.join(data))
      response = "{}: {}".format(cur_thread.name, ' '.join(data))
      self.wfile.write(response)
      #self.request.sendall(response)


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
    

def main():
   global Running
   global usersLoaded
   
   print('Track & Field Meet Server Starting....')

   while (Running == True):
      if not usersLoaded:
         usersLoaded = LoadAdmin()
         RegisterCallbacks()

      else:
         acceptCommands()
         
   server.shutdown()
   server.server_close()
   
HOST, PORT = "192.168.0.162", 50021

server = SSL_ThreadingTCPServer((HOST,PORT),ThreadedTCPRequestHandler,"TFMS.crt","TFMS.key")


ip, port = server.server_address

# Start a thread with the server -- that thread will then start one
# more thread for each request
server_thread = threading.Thread(target=server.serve_forever)
# Exit the server thread when the main thread terminates
server_thread.daemon = True
server_thread.start()
print("Server loop running in thread:", server_thread.name)   
 
# io_thread = threading.Thread(target=main) 
# io_thread.daemon = True
# io_thread.start()

#server.shutdown()
#server.server_close()
