import json

# bottle framework
from bottle import request, response, route, run, template, abort

# controller
from controller import App

app = None

def setup(base, conf_fn):
   print '\n**** service initialization ****\n'
   global app
   app = App(base, conf_fn)

#
# setup the configuration for our service
@route('/')
def root():
   print "--> root"
   return 'hello world'


####################### PIN #######################

#
# upload pin
#
@route('/v1/user/<user_id>/pin', method='POST')
def createPin(user_id):
    pin_name = request.forms.get('pin_name')
    print pin_name
    if not pin_name:
        abort(400, 'No data received')
    image = request.files.get('image')
    print '-> uploading pin'
    return app.createPin(user_id, pin_name,image)
#
# get pin by id from db
#
@route('/v1/pin/<id>', method='GET')
def getPin(id):
   print '-> getting pin'
   return app.getPin(id)

#
# get all pins from db
#
@route('/v1/pins', method='GET')
def getAllPins():
   print '-> getting all pins'
   return app.getAllPins()

#
# add comments to pin
#
@route('/v1/user/<user_id>/pin/<pin_id>', method='PUT')
def updatePin(user_id, pin_id):
   data = request.body.readline()
   if not data:
	abort(400, 'No data received')
   comment = json.load(request.body)

   print '-> adding comment to pin'
   return app.updatePin(user_id, pin_id, comment)

####################### BOARD #######################

#
# Create Board
#
@route('/v1/user/<user_id>/board', method='POST')
def createBoard(user_id):
   data = request.body.readline()
   if not data:
	abort(400, 'No data received')
   board = json.load(request.body)
   print '-> creating board'
   return app.createBoard(user_id, board)

#
# get board by id from db
#
@route('/v1/boards/<id>', method='GET')
def getBoard(id):
   print '-> getting board'
   return app.getBoard(id)

#
# get all boards from db
#
@route('/v1/boards', method='GET')
def getAllBoards():
   print '-> getting all boards'
   return app.getAllBoards()

#
# attach pin to board
#
@route('/v1/user/<user_id>/board/<board_id>', method='PUT')
def updateBoard(user_id, board_id):
   data = request.body.readline()
   if not data:
	abort(400, 'No data received')
   pin = json.load(request.body)

   print '-> attaching pin to board'
   return app.updateBoard(user_id, board_id, pin)

#
# delete board from db
#
@route('/v1/user/<user_id>/board/<board_id>', method='DELETE')
def deleteBoard(user_id, board_id):
   print '-> deleting board'
   return app.deleteBoard(user_id, board_id)


####################### USER #######################

#
# register
#
@route('/v1/reg', method='POST')
def register():
   data = request.body.readline()
   if not data:
	abort(400, 'No data received')
   user = json.load(request.body)
   print '-> registering user'
   response.status = 201
   return app.register(user)

#
# login
#
@route('/v1/login', method='POST')
def login():
   data = request.body.readline()
   if not data:
	abort(400, 'No data received')
   user = json.load(request.body)
   print '-> logging in'
   username = request.json["username"]
   password = request.json["password"]
   return app.login(username, password)

#
# get user by id from db
#
@route('/v1/user/<id>', method='GET')
def getUser(id):
   print '-> getting user'
   return app.getUser(id)


####################### HELPER FUNCTIONS #######################

#
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

