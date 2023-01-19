from user import User

class Channel:
  def __init__(self, name):
    # Impossibilitar usuários com o mesmo nickname
    self.users = {}
    self.name = name
  
  def addUser(self, user):
    self.users[user] = user
    user.currentChannel = self.name

  def removeUser(self, user):
    del self.users[user]
    user.currentChannel = None