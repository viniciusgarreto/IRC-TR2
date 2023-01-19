#Servidor TCP
import socket
from threading import Thread
from channel import Channel
from user import User

# def conexao(con,cli):
#     while True:
#         msg = con.recv(1024)
#         if not msg: break
#         print (msg)
#     print ('Finalizando conexao do cliente', cli)
#     con.close() 

# # Endereco IP do Servidor
# HOST = ''
# # Porta que o Servidor vai escutar
# PORT = 5007
# tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# orig = (HOST, PORT)
# tcp.bind(orig)
# tcp.listen(1)
# while True:
#     con, cliente = tcp.accept()
#     print ('Conectado por ', cliente)
#     t = Thread(target=conexao, args=(con,cliente,))
#     t.start()

HOST = 'localhost'
PORT = 5007

class Server:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.channels = {}
    self.users = {}
    self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (host, port)
    self.tcp.bind(orig)
  
  def connection(self, con, cli, user):
    while True:
      msg = con.recv(1024)
      if not msg: break
      
      command = msg.decode().split(' ')
      if command[0] == 'JOIN':
        channel = command[1]
        response = self.joinChannel(channel, user)
        print (response)
      elif command[0] == 'LIST':
        response = self.listChannels()
        print(response)
      elif command[0] == 'NICK':
        newNick = command[1]
        self.users[user].setNickname(newNick, [user.nickname for user in self.users])
      elif command[0] == 'USER':
        print("Nickname: " + user.nickname + " Host: " + user.host + " Username: " + user.username)
      elif command[0] == 'QUIT':
        response = self.quitChannel(user)
        print (response)
      else:
        print ("ERR	UNKNOWNCOMMAND")

    print ('Finalizando conexao do cliente', cli)
    con.close() 

  def partCurrentChannel(self, user, channel):
    self.channels[user.currentChannel].removeUser(user)

  def addChannel(self, channel):
    self.channels[channel.name] = channel
  
  def joinChannel(self, channel, user):
    if channel not in self.channels:
      canal = Channel(channel)
      self.addChannel(canal)

    if user.currentChannel != None:
      self.partCurrentChannel(user, user.currentChannel)
    
    self.channels[channel].users[user] = user
    self.users[user] = user
    self.users[user].currentChannel = channel
    
    return "User" + " " + user.nickname + " " + "joined your channel: " + channel

  def quitChannel(self, user):    
    self.channels[user.currentChannel].removeUser(user)    
    return "User " + user.nickname + " quit the channel"

  def listen(self):
    self.tcp.listen(1)
  
  def acceptConnection(self, user):
    while True:
      con, cli = self.tcp.accept()
      print ('Conectado por ', cli)
      t = Thread(target=self.connection, args=(con, cli, user))
      t.start()
  
  def listChannels(self):
    channelList = []
    for channel in self.channels:
      channelList.append(self.channels[channel].name + " " + str(len(self.channels[channel].users)))
    return channelList

server = Server(HOST, PORT)
server.listen()
user2 = User(HOST, PORT, "alice costa", "alce")
server.acceptConnection(user2)
