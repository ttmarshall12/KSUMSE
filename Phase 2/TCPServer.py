import socket
#import rsa
import os.path
import Users
import pickle
import xml.etree.ElementTree as ET
import sqlite3
import random

def oldStuff():
   SEND_PORT = 50021

   # if not os.path.isfile('public.key') or not os.path.isfile('private.key'):
      
      # print("Gnerating RSA keys...")
      # (pubkey, privkey) = rsa.newkeys(512)
      
      # f = open('public.key', 'w')
      # f.write(pubkey.save_pkcs1('PEM'))
      # f.close()
      
      # f = open('private.key', 'w')
      # f.write(privkey.save_pkcs1('PEM'))
      # f.close()
      
   # else:
      
      # print("loading public key...")
      # f = open('public.key', 'r')
      # keyfile = f.read()
      # pubkey = rsa.PublicKey.load_pkcs1(keyfile, 'PEM')
      # f.close()
      # #f.open('public.key','r')
      # #pubkey = f.read()
      # #f.close()
      
      # print("loading private key...")
      # f = open('private.key', 'r')
      # keyfile = f.read()
      # privkey = rsa.PrivateKey.load_pkcs1(keyfile,'PEM')
      # f.close()
      # #f.open('private.key', 'r')
      # #privkey = f.read()
      # #f.close()
      

   # print("loading client public key...")
   # f = open('clientpublic.key', 'r')
   # keyfile = f.read()
   # clientpubkey = rsa.PublicKey.load_pkcs1(keyfile, 'PEM')
   # f.close()

   # message = 'hello mate!'
   # cryptmessage = rsa.encrypt(message,pubkey)

   # print("Encrypted message: " + cryptmessage)
   # print("Decrypted message: " + rsa.decrypt(cryptmessage, privkey))

   # print("Signing message...")
   # signature = rsa.sign(message, privkey, 'SHA-1')

   # print("verifying message...")
   # print("Message verrified = " + str(rsa.verify(message, signature, pubkey)))

   # print("Creating socket...")
   # s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

   # print("Binding socket...")
   # s.bind(('',SEND_PORT))

   # #s.settimeout(0.1)

   # print("Port listening...")
   # s.listen(5)

   # while 1:
       # print("Socket accepting...")
       # client, addr = s.accept()
       # print ('connected with ' + addr[0] + ':' + str(addr[1]))

       # print("Recieving data...")
       # data = client.recv(1024)
      
       # print("Enrypted data: " + str(data))
       # decryptedData = rsa.decrypt(data,privkey)
       # print("Decrypted data: " + str(decryptedData))
       
       # MESSAGE = "I received your data"
       
       # encryptedData = rsa.encrypt(MESSAGE.encode(), clientpubkey)

       # client.send(encryptedData)

       # client.close()


   # print("Clsoing socket...")
   # s.close()

   def printName(instance):
      print(instance.name)

   test = Users.Official("Jim", 123456)

   # print("Writing user to disk...")

   # with open('test.pkl', 'wb') as output:
      # pickle.dump(test, output, pickle.HIGHEST_PROTOCOL)

   # del test

   # with open('test.pkl', 'rb') as input:
      # test = pickle.load(input)
     
   # x = printName
   # x(test)
   #print("Test user's name is " + test.name)

   print(isinstance(test, Users.User))
   print(isinstance(test, Users.Official))

######### Global Variables ##########
Running = True
usersLoaded = False
userList = []
userRoot = ET.Element("users")
currentUser = ""
commandCallback = {}
userOptionCallback = {}


########## SQL DB #######################
dbConn = sqlite3.connect('tfms.db')
dbCur = dbConn.cursor()
######### XML Schema ###############
#userElement = ET.SubElement(userRoot, "user")
# userTypeElement = ET.subElement(userElement,"userType")
# userNameElement = ET.subElement(userElement, "userName")
# userIDElement = ET.subElement(userElement, "userID")

#####################################
def getRandomID():
   range_start = 10**(5)
   range_end = (10**6)-1
   return random.randint(range_start, range_end)

def SetupDB():
   global dbCur
   global dbConn
   
   dbCur.execute('CREATE TABLE IF NOT EXISTS users (type TEXT, name TEXT, id INT)')
   dbCur.execute('CREATE TABLE IF NOT EXISTS events (name TEXT)')

def Login():
   global currentUser
   
   if currentUser == "":
      print('Logging in....')
      name = raw_input("Enter name: ")
      ID = raw_input("Enter ID: ")
      
      dbCur.execute('SELECT * FROM users WHERE type = ? AND name = ? AND id = ?', ("admin", name, ID))
      
      Match = dbCur.fetchone()
      
      if Match != None:
      
         print(Match[1])
         
         print("Welcome back " + name + "!!!!!!!")
         currentUser = Users.Admin(name,ID)
               
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
   
def RemoveUser():
   PrintUsers()
      
   name = raw_input('Enter name of user to be removed: ')
   
   dbCur.execute('SELECT * FROM users WHERE name = ?', (name,))
   
   user = dbCur.fetchone()
   
   if user != None:
      #accept = raw_input('Sure you want to remove' + user[0] + user[1] + user[2] + ' (y/n)? ')
      accept = raw_input('Sure you want to remove' + str(user) + ' (y/n)? ')
      if accept == 'y':
         dbCur.execute('DELETE FROM users WHERE type = ? AND name = ? AND id = ?', (user[0], user[1], user[2]))
         dbConn.commit()
      else:
         print('Cancelling removal....')
   else:
      print("User doesn't exist...")
   
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
   userOptionCallback['2'] = RemoveUser
   userOptionCallback['3'] = ModifyUser
   

def LoadAdmin():
   global dbCur
   dbCur.execute('SELECT * FROM users WHERE type = "admin"')
   allAdmin = dbCur.fetchall()
   
   if len(allAdmin) != 0:
      print("Loading admin file...")
      return True
      
   else:
      print("Must create an admin account....")
      name = raw_input("Please enter admin name: ")
      ID = raw_input("Please enter admin ID: ")
      
      print("Creating admin....")
      admin = Users.Admin(name, ID)
      userList.append(admin)
      dbCur.execute('INSERT INTO users(type, name, id) VALUES (?, ?, ?)', ("admin", admin.name, admin.ID))
      dbConn.commit()
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
      

def main():
   global Running
   global usersLoaded
   
   print('Track & Field Meet Server Starting....')
   print('Setting up DB...')
   
   SetupDB()
   
   while (Running == True):
      
      if not usersLoaded:
         usersLoaded = LoadAdmin()
         RegisterCallbacks()

      else:
         acceptCommands()
         
      #print("Run status is " + str(Running))
      
      
main()
