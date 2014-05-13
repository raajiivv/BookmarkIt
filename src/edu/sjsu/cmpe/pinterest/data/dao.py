import time
import json
import traceback
import zlib

import citrusleaf as cl
import python_citrusleaf as pcl

from bson.objectid import ObjectId
from pymongo import Connection
db = Connection('localhost', 27017)
# Initialize citrusleaf once
cl.citrusleaf_init()
# Create a cluster with a particular starting host
clu = cl.citrusleaf_cluster_create()
# Add host to the cluster
return_value = cl.citrusleaf_cluster_add_host(clu, "127.0.0.1", 3000, 1000)

# set up the key. Create a stack object, set its value to a string
key_obj = cl.cl_object()
cl.citrusleaf_object_init_str(key_obj, "rajiv")

# Declaring an array in this interface
pin = cl.cl_bin_arr(4)
board = cl.cl_bin_arr(4)

comment = cl.cl_bin_arr(3)
count = cl.cl_bin_arr(2)

user = cl.cl_bin_arr(4)
#User bins
u0 = user[0]
u0.bin_name = "name" 
u1 = user[1]
u1.bin_name = "user_name"
u2 = user[2]
u2.bin_name = "password"


## Provide values for those bins and then initialize them.


#Board bins
b0 = board[0]
b0.bin_name = "board_name"
b1 = board[1]
b1.bin_name = "pin_list"
b2 = board[2]
b2.bin_name = "user_id"

#Pin bins
p0 = pin[0]
p0.bin_name = "pin_name"
p1 = pin[1]
p1.bin_name = "pin_path"
p2 = pin[2]
p2.bin_name = "user_id"

#Comment bins
c0 = comment[0]
c0.bin_name = "comment"
c1 = comment[1]
c1.bin_name = "pin_id"

#Count bins
count0 = count[0]
count0.bin_name = "count";



size = cl.new_intp()
generation = cl.new_intp()
# Declare a reference pointer for cl_bin *
bins_get_all = cl.new_cl_bin_p()


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

   '''def register(self, user):
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
    '''    
        
   def register(self,u):
        print "---> registering user : ",u
        # Number of bins returned
        user_count = self.getCount("user_count")
        for j in xrange(user_count):
            rv = cl.citrusleaf_get_all(clu, "user", str(j+1), key_obj, bins_get_all , size, 100, generation);
            number_bins = cl.intp_value(size)
            # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
            bins = pcl.get_bins (bins_get_all, number_bins)
            for i in xrange(number_bins):
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "user_name"):
                    #print "comparing ", u["username"], " with database object ", bins[i].object.u.str 
                    if (bins[i].object.u.str) == u["username"] :
                        return "duplicate"        
        #Insert User into user namespace
        user_count+=1
        #self.setUser(u,user_count)
        cl.citrusleaf_object_init_str(u0.object, str(u["name"]))
        cl.citrusleaf_object_init_str(u1.object, str(u["username"]))
        cl.citrusleaf_object_init_str(u2.object, str(u["password"]))
        print "password ", str(u["password"])
        # Assign the structure back to the "bins" variable
        user[0] = u0
        user[1] = u1
        user[2] = u2
        print "name ",u["name"]
        print "reading from object " , user[0].object.u.str
        return_value = cl.citrusleaf_put(clu, "user", str(user_count), key_obj, user, 3, None);
        
        self.setCount("user_count", user_count)
        return user_count
        
   '''def login(self, username, password):
	print "---> logging in:",username
	try:
		user = db.pinterestDb['user'].find({"username": username, "password":password}, {"_id":1})
		return self.serializeObjIdInCursor(user)
	except:
		return "error"'''
   
   def login (self, username, password):
        print "---> logging in:",username
        user_count = self.getCount("user_count")
        print user_count
        for j in xrange(user_count):
            rv = cl.citrusleaf_get_all(clu, "user", str(j+1), key_obj, bins_get_all , size, 100, generation);
            number_bins = cl.intp_value(size)
            # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
            print "j : ", j
            bins = pcl.get_bins (bins_get_all, number_bins)
            for i in xrange(number_bins):
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "user_name"):
                    uname = bins[i].object.u.str

                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "password"):
                    passwd = bins[i].object.u.str

                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "name"):
                    name = bins[i].object.u.str
                    
            print "User values : ", uname, passwd, name
            print username, password


            if (uname == username) & (passwd == password) :
                user = {"_id": j+1, "username" : uname, "password" : password, "name" : name }
                print user
                return user
            print "final"
        return "error"
        
   
   '''def getUser(self, id):
	print "---> getting user:",id
	try:
		id = ObjectId(str(id))
		user = db.pinterestDb['user'].find({"_id": id}, {"password":0})
		return self.serializeObjIdInCursor(user)
	except:
		return "error"'''
       
   def getUser(self, id):
        print "---> getting user:",id
        '''user_count = self.getCount("user_count")
        print user_count
        for j in xrange(user_count):'''
        rv = cl.citrusleaf_get_all(clu, "user", str(id), key_obj, bins_get_all , size, 100, generation);
        number_bins = cl.intp_value(size)
        # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
        if number_bins > 0 : 
            bins = pcl.get_bins (bins_get_all, number_bins)
            for i in xrange(number_bins):
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "user_name"):
                    uname = bins[i].object.u.str
    
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "password"):
                    passwd = bins[i].object.u.str
    
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "name"):
                    name = bins[i].object.u.str
                    
            print "User values : ", uname, passwd, name
            user = {"_id": id, "username" : uname, "name" : name }
            print user
            return user
        else:
           return "error"
 


################# HELPER FUNCTIONS ###################

   def getCount(self, name):
    rv = cl.citrusleaf_get_all(clu, "count", name, key_obj, bins_get_all , size, 100, generation);
    # Number of bins returned
    number_bins = cl.intp_value(size)
    # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
    bins = pcl.get_bins (bins_get_all, number_bins)
    for i in xrange(number_bins):
        if ((bins[i].object.type)==cl.CL_INT) & (bins[i].bin_name == "count") :
            return bins[i].object.u.i64
    return 0

   def setCount(self,name,value):
    cl.citrusleaf_object_init_int(count0.object, value);
    count[0] = count0
    return_value = cl.citrusleaf_put(clu, "count", name, key_obj, count, 1, None);
    
    
   def setUser(self, u, user_count):

    cl.citrusleaf_object_init_str(u0.object, str(u["name"]))
    cl.citrusleaf_object_init_str(u1.object, str(u["username"]))
    cl.citrusleaf_object_init_str(u2.object, str(u["password"]))
    print "password ", str(u["password"])
    # Assign the structure back to the "bins" variable
    user[0] = u0
    user[1] = u1
    user[2] = u2
    print "name ",u["name"]
    print "reading from object " , user[0].object.u.str
    return_value = cl.citrusleaf_put(clu, "user", str(user_count), key_obj, user, 3, None);
    if return_value != cl.CITRUSLEAF_OK :
        print "1. Failure setting values ", return_value
        #sys.exit(-1);
        
    else:
        print "Success"
        
    size = cl.new_intp()
    generation = cl.new_intp()
    # Declare a reference pointer for cl_bin *
    bins_get_all = cl.new_cl_bin_p()
    rv = cl.citrusleaf_get_all(clu, "user", str(user_count), key_obj, bins_get_all , size, 100, generation);
    # Number of bins returned
    number_bins = cl.intp_value(size)
    # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
    bins = pcl.get_bins (bins_get_all, number_bins)

        
    for i in xrange(number_bins):
        if(bins[i].object.type)==cl.CL_STR:
            print "Bin name: ",bins[i].bin_name,"Resulting string: ",bins[i].object.u.str
        elif(bins[i].object.type)==cl.CL_INT:
            print "Bin name: ",bins[i].bin_name,"Resulting int: ",bins[i].object.u.i64
        elif bins[i].object.type == cl.CL_BLOB:
            binary_data = cl.cdata(bins[i].object.u.blob, bins[i].object.sz)
            print "Bin name: ",bins[i].bin_name,"Resulting decompressed blob: ",zlib.decompress(binary_data)
        else:
            print "Bin name: ",bins[i].bin_name,"Unknown bin type: ",bins[i].object.type




        
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
