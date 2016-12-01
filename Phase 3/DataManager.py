import Database

class Decryptor:
   
   def __init__(self, data):
      self.encrypted = data
      
      
   def Decrypt(self, key):
      return None


class Authenticator:

   def __init__(self, data):
      self.recv = data
      
   
   def Authenticated(self):
      return True
      
      

class Dispatcher:
   
   response = ""

   def __init__(self, data, db):
      self.recv = data
      self.db = db
 
   def ExecuteCommand(self):
      
      if self.recv[0] == 'adduser':
        self.db.AddUser(self.recv[1], self.recv[2], self.recv[3])
      else:
         print("Command not recognized...")
