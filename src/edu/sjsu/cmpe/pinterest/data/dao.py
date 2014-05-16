import time
'''import json
import traceback
import zlib'''
import datetime
import os

import citrusleaf as cl
import python_citrusleaf as pcl

'''from bson.objectid import ObjectId
from pymongo import Connection
db = Connection('localhost', 27017)'''
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

comment = cl.cl_bin_arr(4)
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
p3 = pin[3]
p3.bin_name = "image"

#Comment bins
c0 = comment[0]
c0.bin_name = "comment"
c1 = comment[1]
c1.bin_name = "pin_id"
c2 = comment[2]
c2.bin_name = "user_id"

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

    def createPin(self, user_id, pname, img):
        print "---> creating pin:",pname
        pin_count = self.getCount("pin_count")
        pin_count +=1
        print "1"
        pin_name = pname
        pin_path = str(img.filename)
        print pin_name, pin_path
        user_id = int(user_id)
        print "2"

        dir = '/home/rajiv/workspace/python/cmpe273-project2/'+str(user_id)
        print dir

        if not os.path.exists(dir):
            os.mkdir(dir)
        fname = str(datetime.datetime.now())+'_'+str(img.filename)
        filepath = dir + '/'+fname
        imageUrl = 'http://localhost:8080'+str(user_id)+fname
        
        img.save(filepath)
        print(imageUrl)
        
        cl.citrusleaf_object_init_str(p0.object, pin_name)#str(u["name"]));
        cl.citrusleaf_object_init_str(p1.object, filepath)
        cl.citrusleaf_object_init_int(p2.object, user_id)
        #img = zlib.compress(img)
        print "here"
        #cl.citrusleaf_object_init_blob(p3.object, img, "102400")
        print "here too"
        

        print "user id : ", user_id
        # Assign the structure back to the "bins" variable
        pin[0] = p0
        pin[1] = p1
        pin[2] = p2
        #pin[3] = p3
                
        print "name ",pin_name
        print "reading from object " , pin[0].object.u.str
        return_value = cl.citrusleaf_put(clu, "pin", str(pin_count), key_obj, pin, 3, None);
        self.setCount("pin_count", pin_count)
        return pin_count

    def getPin(self, id):
        print "---> getting pin:",id
        rv = cl.citrusleaf_get_all(clu, "pin", str(id), key_obj, bins_get_all , size, 100, generation);
        number_bins = cl.intp_value(size)
        # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
        if number_bins > 0 : 
            bins = pcl.get_bins (bins_get_all, number_bins)
            for i in xrange(number_bins):
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "pin_name"):
                    pname = bins[i].object.u.str
    
                '''if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "password"):
                    passwd = bins[i].object.u.str'''
    
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "pin_path"):
                    ppath = bins[i].object.u.str
                    
            print "User values : ", pname, ppath
            comments = self.getComments(id)
            user = {"_id": id, "pin_name" : pname, "pin_path" : ppath, "comments" : comments }
            print user
            return user
        else:
           return "error"

    def getAllPins(self):
        print "---> Listing pins:"
        pin_count = self.getCount("pin_count")
        pins = []
        for i in range(pin_count):
            pin = self.getPin(i+1)
            pins.append(pin)
        return pins

####################### BOARD #######################

    def createBoard(self,user_id,b, pin_list=""):
        print "---> creating board:",b
        
        board_count = self.getCount("board_count")
        board_count +=1
        print "1"
        board_name = str(b["boardname"])
        
        user_id = int(user_id)
        print "2"
        cl.citrusleaf_object_init_str(b0.object, board_name)#str(u["name"]));
        cl.citrusleaf_object_init_str(b1.object, pin_list)
        cl.citrusleaf_object_init_int(b2.object, user_id)

        print "user id : ", user_id
        # Assign the structure back to the "bins" variable
        board[0] = b0
        board[1] = b1
        board[2] = b2
                
        print "name ",b["boardname"]
        print "reading from object " , board[0].object.u.str
        return_value = cl.citrusleaf_put(clu, "board", str(board_count), key_obj, board, 3, None);
        self.setCount("board_count", board_count)
        return board_count

    def getBoard(self, id):
        print "---> getting board:",id
        rv = cl.citrusleaf_get_all(clu, "board", str(id), key_obj, bins_get_all , size, 100, generation);
        number_bins = cl.intp_value(size)
        # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
        if number_bins > 0 : 
            bins = pcl.get_bins (bins_get_all, number_bins)
            for i in xrange(number_bins):
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "pin_list"):
                    pin_list = bins[i].object.u.str
                    
            print "Pin List : ", pin_list
            pin_list = pin_list.split(",")
            pins=[]
            for pin in pin_list:
                pins.append(self.getPin(pin))

            print pins
            return pins
        else:
            return "error"
        


    def getAllBoards(self):
        print "---> Listing boards:"
        board_count = self.getCount("board_count")
        print board_count
        boards = []
        for j in xrange(board_count):
            rv = cl.citrusleaf_get_all(clu, "board", str(j+1), key_obj, bins_get_all , size, 100, generation);
            number_bins = cl.intp_value(size)
            # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
            if number_bins>0:
                print "j : ", j
                bins = pcl.get_bins (bins_get_all, number_bins)
                for i in xrange(number_bins):
                    if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "board_name"):
                        bname = bins[i].object.u.str
                
                bId = j+1
                b = {"board_id" : bId, "board_name" : bname}
                boards.append(b)
        return boards
            
    def updateBoard(self, user_id, board_id, pin):
        print "--> updating board:",board_id
        rv = cl.citrusleaf_get_all(clu, "board", str(board_id), key_obj, bins_get_all , size, 100, generation);
        number_bins = cl.intp_value(size)
        # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
        if number_bins > 0 : 
            bins = pcl.get_bins (bins_get_all, number_bins)
            for i in xrange(number_bins):
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "pin_list"):
                    pin_list = bins[i].object.u.str
    
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "board_name"):
                    board_name = bins[i].object.u.str
                
            print pin_list,board_name        
            print "Pin List : ", pin_list
            if (pin_list == "") :
                pin_list = pin["pin_id"]
            else :
                pin_list = str(pin_list)+","+str(pin["pin_id"]) 
            print "Updated pin list : ", pin_list
            b = {"boardname": board_name}
            print b
            #self.createBoard(user_id, b, pin_list)
            user_id = int(user_id)
            pin_list = str(pin_list)
            cl.citrusleaf_object_init_str(b1.object, pin_list)
            cl.citrusleaf_object_init_str(b0.object, board_name)#str(u["name"]));
            cl.citrusleaf_object_init_int(b2.object, user_id)
            # Assign the structure back to the "bins" variable
            board[0] = b0
            board[1] = b1
            board[2] = b2
            
            return_value = cl.citrusleaf_put(clu, "board", str(board_id), key_obj, board, 3, None);
            print "here"
            return b
        return "error"

    def deleteBoard(self, user_id, board_id):
        print "---> deleting board:", board_id
        cl.delete_intp(generation)
        cl.delete_cl_bin_p(bins_get_all)
        deletion = cl.delete_intp(size)
        cl.citrusleaf_delete(clu, "board", str(board_id), key_obj, deletion ) 


####################### USER #######################

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
        self.createUser(u,user_count)
        self.setCount("user_count", user_count)
        return user_count
        
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
    
                '''if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "password"):
                    passwd = bins[i].object.u.str'''
    
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "name"):
                    name = bins[i].object.u.str
                    
            print "User values : ", uname, name
            user = {"_id": id, "username" : uname, "name" : name }
            print user
            return user
        else:
           return "error"
       
##################### COMMENTS ####################

    def getComments(self, pId):
        comment_count = self.getCount("comment_count")
        pId = int(pId)
        comments = []
        for j in xrange(comment_count):
            rv = cl.citrusleaf_get_all(clu, "comment", str(j+1), key_obj, bins_get_all , size, 100, generation);
            number_bins = cl.intp_value(size)
            # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
            bins = pcl.get_bins (bins_get_all, number_bins)
            for i in xrange(number_bins):
                if ((bins[i].object.type)==cl.CL_INT): 
                    #print "comparing ", u["username"], " with database object ", bins[i].object.u.str
                    if (bins[i].bin_name == "pin_id"): 
                        pin_id = bins[i].object.u.i64
                    if (bins[i].bin_name == "user_id"):
                        user_id = bins[i].object.u.i64
                if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "comment"):
                    comment_string = bins[i].object.u.str
            if(pId == pin_id):
                c = {"user_id" : user_id, "comments":comment_string }
                comments.append(c)
        return comments
        
   
    def setComment(self, uId, pId, c):
        print "----> User ", uId," commenting ", c["comment"], " on pin ", pId
        comment_count = self.getCount("comment_count")
        comment_count +=1
        print "1"
        comment_string = str(c["comment"])
        
        user_id = int(uId)
        pin_id = int(pId)
        print "2"
        
        cl.citrusleaf_object_init_str(c0.object, comment_string)#str(u["name"]));
        cl.citrusleaf_object_init_int(c1.object, pin_id)
        cl.citrusleaf_object_init_int(c2.object, user_id)

        print "user id : ", user_id
        # Assign the structure back to the "bins" variable
        comment[0] = c0
        comment[1] = c1
        comment[2] = c2
                
        print "name ",c["comment"]
        print "reading from object " , comment[0].object.u.str
        return_value = cl.citrusleaf_put(clu, "comment", str(comment_count), key_obj, comment, 3, None);
        self.setCount("comment_count", comment_count)
        
        return self.getPin(pin_id)
         


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
        print name,value
        return_value = cl.citrusleaf_put(clu, "count", name, key_obj, count, 1, None);
    
    
    def createUser(self, u, user_count):
        name = str(u["name"])
        uname = str(u["username"])
        passwd = str (u["password"])
        print
        cl.citrusleaf_object_init_str(u0.object, name)#str(u["name"]));
        cl.citrusleaf_object_init_str(u1.object, uname)#str(u["username"]));
        cl.citrusleaf_object_init_str(u2.object, passwd)#str(u["password"]));
        print uname, name, passwd
        # Assign the structure back to the "bins" variable
        user[0] = u0
        user[1] = u1
        user[2] = u2
        print "name ",u["name"]
        print "reading from object " , user[0].object.u.str
        return_value = cl.citrusleaf_put(clu, "user", str(user_count), key_obj, user, 3, None);

        
