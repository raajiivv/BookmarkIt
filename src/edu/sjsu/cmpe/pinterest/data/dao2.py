import time
import json
import traceback

from bson.objectid import ObjectId
from pymongo import Connection
db = Connection('localhost', 27017)

class Storage(object):
 
   def __init__(self):
      # initialize our storage, data is a placeholder
      self.data = {}

      # for demo
      self.data['created'] = time.ctime()


####################### PIN #######################

   def createPin(self, user_id, pin):
	print "---> creating pin:",pin
	try:
		objId = db.pinterestDb['pin'].insert(pin, safe=True)
		return str(objId)
	except:
		return "error"

   def getPin(self, id):
	print "---> getting pin:",id
	try:
		id = ObjectId(str(id))
		pin = db.pinterestDb['pin'].find({"_id": id})
		return self.serializeObjIdInCursor(pin)
	except:
		return "error"

   def getAllPins(self):
	print "---> Listing pins:"
	try:
		pins = db.pinterestDb['pin'].find()
		return self.serializeObjIdInCursorList(pins)
	except:
		return traceback.print_exc()

   def updatePin(self, user_id, pin_id, comment):
	print "--> updating pin:", pin_id
	try:
		pin_id = ObjectId(str(pin_id))
		db.pinterestDb['pin'].update({"_id": pin_id}, { "$push": {"comments":{"user":user_id, "comment":comment["comment"]}} });
		pin = db.pinterestDb['pin'].find({"_id": pin_id})
		return self.serializeObjIdInCursor(pin)
	except:
		return "error"

####################### BOARD #######################

   def createBoard(self, user_id, board):
	print "---> creating board:",board
	try:
		objId = db.pinterestDb['board'].insert(board, safe=True)
		user_id = ObjectId(str(user_id))
		board = {"board_id":str(objId), "board_name":board["boardname"]}
		db.pinterestDb['user'].update({"_id":user_id}, { "$push": {"boards":board}})
		return str(objId)
	except:
		return "duplicate"

   def getBoard(self, id):
	print "---> getting board:",id
	try:
		id = ObjectId(str(id))
		board = db.pinterestDb['board'].find({"_id": id})
		return self.serializeObjIdInCursor(board)
	except:
		return "error"

   def getAllBoards(self):
	print "---> Listing boards:"
	try:
		boards = db.pinterestDb['board'].find()
		return self.serializeObjIdInCursorList(boards)
	except:
		return traceback.print_exc()

   def updateBoard(self, user_id, board_id, pin):
	print "--> updating board:",board_id
	try:
		board_id = ObjectId(str(board_id))
		db.pinterestDb['board'].update({"_id": board_id}, { "$push": {"pins":pin} });
		board = db.pinterestDb['board'].find({"_id": board_id})
		return self.serializeObjIdInCursor(board)
	except:
		return "error"

   def deleteBoard(self, user_id, board_id):
	print "---> deleting board:",board_id
	try:
		user_id = ObjectId(str(user_id))
		db.pinterestDb['board'].remove({"_id": board_id})
		db.pinterestDb['user'].update({"_id": user_id}, { "$pull": {"boards":{"board_id":board_id}} })
		return "success"
	except:
		return "error"

####################### USER #######################

   def register(self, user):
	print "---> registering user:",user
	existing = db.pinterestDb['user'].find({"username":user["username"]})
	if existing.hasNext():
		return "duplicate"
	try:
		user = {"username":user["username"], "password":user["password"], "name":user["name"], "boards":[]}
		objId = db.pinterestDb['user'].insert(user, safe=True)
		return str(objId)
	except:
		return "duplicate"

   def login(self, username, password):
	print "---> logging in:",username
	try:
		user = db.pinterestDb['user'].find({"username": username, "password":password}, {"_id":1})
		return self.serializeObjIdInCursor(user)
	except:
		return "error"

   def getUser(self, id):
	print "---> getting user:",id
	try:
		id = ObjectId(str(id))
		user = db.pinterestDb['user'].find({"_id": id}, {"password":0})
		return self.serializeObjIdInCursor(user)
	except:
		return "error"


################# HELPER FUNCTIONS ###################

   def serializeObjIdInCursor(self, cursor):
      serializedJson = ""
      for element in cursor:
	element["_id"] = str(element["_id"])
	serializedJson = element
      return serializedJson

   def serializeObjIdInCursorList(self, cursor):
      serializedJson = []
      for element in cursor:
	element["_id"] = str(element["_id"])
	serializedJson.append(element)
      return serializedJson
