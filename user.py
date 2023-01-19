class User:
  # def __init__(self, host, port, connection, username, nickname):
  def __init__(self, host, port, username, nickname):
    self.host = host
    self.port = port
    # self.connection = connection
    self.username = username
    self.nickname = nickname        
    self.currentChannel = None
  
  def setNickname(self, nickname, nicknameList):
    if nickname in nicknameList:
      print ("Nickname already in use. Please choose another one")
      return False
    
    self.nickname = nickname
    print (self.username + " changed nickname to " + self.nickname)
    return True
  
  def getUser(self):
    return self.nickname + " " + self.host + "" + self.username
