import sqlite3
import Users

class Database:
   
   def __init__(self, name):
      
      self.dbConn = sqlite3.connect(name)
      self.dbCur = self.dbConn.cursor()

      self.dbCur.execute('CREATE TABLE IF NOT EXISTS users (type TEXT, name TEXT, id INT, team TEXT, gender TEXT)')
      self.dbCur.execute('CREATE TABLE IF NOT EXISTS events (name TEXT)')
      
   def GetAdmin(self, name, id):
      
      self.dbCur.execute('SELECT * FROM users WHERE type = ? AND name = ? AND id = ?', ("admin", name, id))
      
      Match = self.dbCur.fetchone()
      
      if Match != None:
         return Users.Admin(name, id)
         
      else:
         return None
         
   def GetAllAdmin(self):
      admin = []
      self.dbCur.execute('SELECT * FROM users WHERE type = "admin"')
      print("getting all admin...")
      admin = self.dbCur.fetchall()
      print(admin)
      return admin
         
         
   def GetAllUsers(self):
      users = []
      self.dbCur.execute('SELECT * FROM users ORDER BY name ASC')
      
      while True:
         row = self.dbCur.fetchone()
         if row == None:
            break
          
         users.append(row)
          
      return users
      
      
   def AddUser(self, userType, name, id):
      
      self.dbCur.execute('INSERT INTO users(type, name, id) VALUES (?, ?, ?)', (userType, name, id))
      self.dbConn.commit()
        
      return True
        
   def RemoveUser(self, userType, name, id):
      
      self.dbCur.execute('DELETE FROM users WHERE type = ? AND name = ? AND id = ?', (userType, name, id))
      self.dbConn.commit()
      
      return True
      
   def ModifyAmin(self, originalUser, modifiedUser):
      
      self.dbCur.execute('UPDATE users SET type = ?, name = ?, id = ? WHERE type = ? AND name = ? AND id = ?', \
         ('admin', modifiedUser.name, modifiedUser.ID, 'admin', originalUser.name, originalUser.ID))
      
      self.dbConn.commit()
         
