import sqlite3
import Users

class Database:
   
   def __init__(self, name):
      
      self.dbConn = sqlite3.connect(name)
      self.dbCur = self.dbConn.cursor()

      self.dbCur.execute('CREATE TABLE IF NOT EXISTS users (type TEXT, name TEXT, id INT, team TEXT, gender TEXT)')
      self.dbCur.execute('CREATE TABLE IF NOT EXISTS events (name TEXT, id INT, startTime TEXT)')
      self.dbCur.execute('CREATE TABLE IF NOT EXISTS entry (eventID INT, athleteName TEXT, athleteID INT, status TEXT)')
      self.dbCur.execute('CREATE TABLE IF NOT EXISTS results (event INT, athleteName TEXT, athleteID INT, athleteTeam TEXT, attempt INT, value REAL)')
      
   def __del__(self):
      self.dbConn.close()
      
   def GetAdmin(self, name, id):
      
      self.dbCur.execute('SELECT * FROM users WHERE type = ? AND name = ? AND id = ?', ("admin", name, id))
      
      Match = self.dbCur.fetchone()
      
      if Match != None:
         return Users.Admin(name, id)
         
      else:
         return None
         
   def GetUser(self, name, id):
      
      self.dbCur.execute('SELECT * FROM users WHERE name = ? AND id = ?', (name, id))
      
      Match = self.dbCur.fetchone()
      
      if Match != None:
         return Match
         
      else:
         return None
         
   def GetUserType(self, name, id):
      
      self.dbCur.execute('SELECT type FROM users WHERE name = ? AND id = ?', (name, id))
      
      Match = self.dbCur.fetchone()
      
      if Match != None:
         return Match
         
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
      
      
   def AddUser(self, userType, name, id, team, gender):
      
      self.dbCur.execute('INSERT INTO users(type, name, id, team, gender) VALUES (?, ?, ?, ?, ?)', (userType, name, id, team, gender))
      self.dbConn.commit()
        
      return True
        
   def RemoveUser(self, userType, name, id):
      
      self.dbCur.execute('DELETE FROM users WHERE type = ? AND name = ? AND id = ?', (userType, name, id))
      self.dbConn.commit()
      
      return True
      
   def ModifyUser(self, inName, inID, outType, outName, outID, outTeam, outGender):
      
      self.dbCur.execute('UPDATE users SET type = ?, name = ?, id = ?, team = ?, gender = ? WHERE name = ? AND id = ?', \
         (outType, outName, outID, outTeam, outGender, inName, inID))
      
      self.dbConn.commit()
         
   def AddResults(self, eventID, athleteName, athleteID, athleteTeam, attempt, value ):
   
      self.dbCur.execute('INSERT INTO results(event, athleteName, athleteID, athleteTeam, attempt, value) \
         VALUES (?, ?, ?, ?, ?, ?)', (eventID, athleteName, athleteID, athleteTeam, attempt, value))
         
      self.dbConn.commit()
      

   def ModifyStatus(self, EID, AID, Status):
      self.dbCur.execute('UPDATE entry SET status = ? WHERE eventID = ? AND athleteID = ?', \
         (Status, EID, AID))
      
      self.dbConn.commit()