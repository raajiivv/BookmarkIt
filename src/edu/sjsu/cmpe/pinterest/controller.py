import sys
import os
import socket
import StringIO
import json

# dao 
from data.dao import Storage

class App(object):
   json, xml, html, text = range(1,5)
   
   #
   # setup the configuration for our service
   #
   def __init__(self,base,conf_fn):
      self.host = socket.gethostname()
      self.base = base
      self.conf = {}
      
      # should emit a failure (file not found) message
      if os.path.exists(conf_fn):
         with open(conf_fn) as cf:
            for line in cf:
               name, var = line.partition("=")[::2]
               self.conf[name.strip()] = var.strip()
      else:
         raise Exception("configuration file not found.")

      # create storage
      self.__store = Storage()
   

####################### PIN #######################

   #
   # function to create pin
   # 
   def createPin(self, user_id, pin, image):
      print '--> creating pin'

      try:
        pin_id = self.__store.createPin(user_id, pin, image)
        return {"success" : True, "pin_id": pin_id}
      except:
        return {"success" : False}

   #
   # function to get pin by id
   # 
   def getPin(self, id):
      print '--> getting pin'

      try:
        pin = self.__store.getPin(id)
        return {"success" : True, "pin": pin}
      except:
        return {"success" : False}

   #
   # function to get all pins
   # 
   def getAllPins(self):
      print '--> Listing pins'

      try:
        pins = self.__store.getAllPins()
	print pins		
        return {"success" : True, "pins": pins}

      except:
        return {"success" : False}

   #
   # function to update pin
   # 
   def updatePin(self, user_id, pin_id, comment):
      print '---> updating pin'

      try:
        pin = self.__store.updatePin(user_id, pin_id, comment)
        return {"success" : True, "pin": pin}
      except:
        return {"success" : False}

####################### BOARD #######################

   #
   # function to create board
   # 
   def createBoard(self, user_id, board):
      print '--> creating board'

      try:
        board_id = self.__store.createBoard(user_id, board)
        return {"success" : True, "token": board_id}
      except:
        return {"success" : False}

   #
   # function to get board by id
   # 
   def getBoard(self, id):
      print '--> getting board'

      try:
        board = self.__store.getBoard(id)
        return {"success" : True, "board": board}
      except:
        return {"success" : False}

   #
   # function to get all boards
   # 
   def getAllBoards(self):
      print '--> Listing boards'

      try:
        boards = self.__store.getAllBoards()
	print boards		
        return {"success" : True, "board": boards}

      except:
        return {"success" : False}

   #
   # function to update board
   # 
   def updateBoard(self, user_id, board_id, pin):
      print '---> updating board'

      try:
        board = self.__store.updateBoard(user_id, board_id, pin)
        return {"success" : True, "board": board}
      except:
        return {"success" : False}

   #
   # function to delete board
   # 
   def deleteBoard(self, user_id, board_id):
      print '--> deleting board'

      try:
        self.__store.deleteBoard(user_id, board_id)
        return {"success" : True}
      except:
        return {"success" : False}


####################### USER #######################

   #
   # function to register user
   # 
   def register(self, user):
      print '--> register'

      try:
        objId = self.__store.register(user)
        return {"success" : True, "id": objId}
      except:
        return {"success" : False}

   #
   # function to login
   # 
   def login(self, username, password):
      print '--> login'

      try:
        objId = self.__store.login(username, password)
        return {"success" : True, "token": objId["_id"]}
      except:
        return {"success" : False}

   #
   # function to get user by id
   # 
   def getUser(self, id):
      print '--> getting user'

      try:
        user = self.__store.getUser(id)
        #return {"success" : True, "username": user["username"], "name":user["name"]}
	return {"success" : True, "user":user}
      except:
	return {"success" : False}



########################################################################

#
# test and demonstrate the setup
#
if __name__ == "__main__":
  if len(sys.argv) > 2:
     base = sys.argv[1]
     conf_fn = sys.argv[2]
     svc = Room(base,conf_fn)
     svc.dump_conf()
  else:
     print "usage:", sys.argv[0],"[base_dir] [conf file]"


