import Database

permissions = {}
permissions['admin'] = ['adduser', 'removeuser', 'getallusers', 'modifyuser', 'addresults', 'updatestatus', 'getresults']
permissions['official'] = ['addresults', 'updatestatus', 'getresults']
permissions['coach'] = ['getresults', 'updatestatus']
permissions['athlete'] = ['getresults', 'updatestatus']
permissions['spectator'] = ['getresults']

class Authenticator:
   


   def __init__(self, data, db):
      self.recv = data
      self.db = db
   
   def Authenticated(self):
      if self.db.GetUser(self.recv[1],self.recv[2]) != None:
         return True
      else:
         return False
         
   def Permitted(self):
      
      print("user type: ")
      print( ''.join(self.db.GetUserType(self.recv[1],self.recv[2])))
      if self.recv[0] in permissions[''.join(self.db.GetUserType(self.recv[1],self.recv[2]))]:
         return True
      else:
         return False
      
      

class Dispatcher:
   
   response = ""

   def __init__(self, data, db):
      self.command = data[0]
      self.user = data[1:3]
      self.params = data[3:]
      self.db = db
 
   def ExecuteCommand(self):
      
      if self.command == 'adduser':
         self.db.AddUser(self.params[0], self.params[1], self.params[2], self.params[3], self.params[4])
         return "AddSuccess"
         
      elif self.command == 'getuser':
         response = self.db.GetUser(self.params[0], self.params[1])
         if response != None:
            return ' '.join(response)
         else:
            return "NoneFound"
            
      elif self.command == 'modifyuser':
         if self.db.GetUser(self.params[0], self.params[1]) != None:
            self.db.ModifyUser(self.params[0], self.params[1], self.params[2], self.params[3], self.params[4], self.params[5], self.params[6])
            return "ModifySuccess"
         else:
            return "ModifyFail"
            
      elif self.command == 'addresults':
         self.db.AddResults(self.params[0], self.params[1], self.params[2], self.params[3], self.params[4], self.params[5])
         return "AddSuccess"
      
      elif self.command == 'updatestatus':
         if ''.join(self.db.GetUserType(self.user[0], self.user[1])) == 'athlete':
            self.db.ModifyStatus(self.params[0], self.user[1], self.params[3])
            
         elif ''.join(self.db.GetUserType(self.user[0], self.user[1])) == 'coach' and \
            self.db.GetUser(self.user[0], self.user[1])[3] == self.db.GetUser(self.params[1], self.params[2])[3]:
            self.db.ModifyStatus(self.params[0], self.params[2], self.params[3])
            
         elif ''.join(self.db.GetUserType(self.user[0], self.user[1])) == 'admin' or \
              ''.join(self.db.GetUserType(self.user[0], self.user[1])) == 'official':
            self.db.ModifyStatus(self.params[0], self.params[2], self.params[3])
            
         else:
         
            return "StatusUpdateFail"
            
         return "StatusUpdateSuccess"
      
      else:
         return "CommandUnknown"
