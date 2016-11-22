

class User:

   PublicKey = ""
   userType = ""

   def __init__(self, name):
      self.name = name
      


class Official(User):

   def __init__(self, name, ID):
      User.__init__(self, name)
      self.ID = ID
      self.userType = "official"
      
 
 
class Admin(Official):
 
   def __init__(self, name, ID):
      Official.__init__(self, name, ID)
      self.userType = "admin"
      
class Participant(User):

   def __init__(self, name, ID):
      User.__init__(self, name)
      self.ID = ID
      self.userType = "participant"

class Athlete(Participant):

   def __init__(self, name, ID, Gender):
      Participant.__init__(self, name, ID)
      self.Gender = Gender
      self.userType = "athlete"
      
    
class Coach(Participant):
   
   def __init__(self, name, ID):
      Participant.__init__(self, name, ID)
      self.userType = "coach"
      
      
class Spectator(User):
   
   def __init__(self, name):
      User.__init__(self, name)
      self.userType = "spectator"
      
      