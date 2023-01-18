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
# PORT = 5002
# tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# orig = (HOST, PORT)
# tcp.bind(orig)
# tcp.listen(1)
# while True:
#     con, cliente = tcp.accept()
#     print ('Conectado por ', cliente)
#     t = Thread(target=conexao, args=(con,cliente,))
#     t.start()

HOST = ''
PORT = 5005

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
      elif command[0] == 'NICK':
        newNick = command[1]
        self.users[user].setNickname(newNick, user)

    print ('Finalizando conexao do cliente', cli)
    con.close() 

  def partCurrentChannel(self, user, channel):
    self.channels[user.currentChannel].removeUser(user)
    self.channels[channel].addUser(user)
    self.users[user].currentChannel = channel.name

    return "User joined your channel: " + channel

  def joinChannel(self, channel, user):
    if channel not in self.channels:
      self.channels[channel] = Channel(channel)

    if user.currentChannel != None:
      self.partCurrentChannel(user, user.currentChannel)
    
    #TODO: Não permitir dois usuários iguais no mesmo canal
    self.channels[channel].users[user] = user
    self.channels[channel].users[user].currentChannel = channel
    self.users[user] = user
    self.users[user].currentChannel = channel
    
    # self.users[user.nickname] = user.nickname
    # self.users[user.nickname].currentChannel = channel.name
    return "User" + " " + user.nickname + " " + "joined your channel: " + channel

  def listen(self):
    self.tcp.listen(1)
    # print ('Finalizando conexao do cliente', cli)
    # con.close() 
  
  def acceptConnection(self, user):
    while True:
      con, cli = self.tcp.accept()
      print ('Conectado por ', cli)
      t = Thread(target=self.connection, args=(con, cli, user))
      t.start()
  
  def listChannels(self):
    channelList = []
    for channel in self.channels:
      channelList.append(channel.name, len(channel.users))
    return channelList

server = Server(HOST, PORT)
server.listen()
user = User(HOST, PORT, "jose costa", "ze")
server.acceptConnection(user)
