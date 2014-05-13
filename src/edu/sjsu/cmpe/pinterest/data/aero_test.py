'''
Created on May 12, 2014

@author: rajiv
'''
import citrusleaf as cl
import python_citrusleaf as pcl
import json

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
user = cl.cl_bin_arr(4)
comment = cl.cl_bin_arr(3)
count = cl.cl_bin_arr(2)

## Provide values for those bins and then initialize them.

#User bins
u0 = user[0]
u0.bin_name = "name" 
u1 = user[1]
u1.bin_name = "user_name"
u2 = user[2]
u2.bin_name = "password"

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
count0.bin_name = "user_count";



size = cl.new_intp()
generation = cl.new_intp()
# Declare a reference pointer for cl_bin *
bins_get_all = cl.new_cl_bin_p()



class Test:

    def __init__(self):
        i = 0
        
    
    u  = {"username" : "rajiv", "name" : "Rajiv" , "password":"password"}
    
    print "---> registering user : ",user
    
    username = "rajiv"
    password = "rajiv"
    
    user_count = 2
    user = cl.cl_bin_arr(4)
    #User bins
    u0 = user[0]
    u0.bin_name = "name" 
    u1 = user[1]
    u1.bin_name = "user_name"
    u2 = user[2]
    u2.bin_name = "password"
    cl.citrusleaf_object_init_str(u0.object, str(u["name"]))
    cl.citrusleaf_object_init_str(u1.object, str(u["username"]))
    cl.citrusleaf_object_init_str(u2.object, str(u["password"]))
    print "password ", u["password"]
    # Assign the structure back to the "bins" variable
    user[0] = u0
    user[1] = u1
    user[2] = u2
    print "name ",u["name"]
    return_value = cl.citrusleaf_put(clu, "user", str(user_count), key_obj, user, 3, None);
    if return_value != cl.CITRUSLEAF_OK :
        print "1. Failure setting values ", return_value
        #sys.exit(-1);
        
    else:
        print "Success"
    
    
    '''user_count = getCount("user_count")
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
    
    
        if (uname == username & passwd == password) :
            user = {"username" : uname, "password" : password, "name" : name }
            print user
            #return user
        print "final"
    '''    
    
    
    
    '''rv = cl.citrusleaf_get_all(clu, "count", "user_count", key_obj, bins_get_all , size, 100, generation);
    # Number of bins returned
    user_count = cl.intp_value(size)
    print user_count
    ''''''print user_count
    print "rajiv"#user["username"]
    for j in xrange(user_count):
        rv = cl.citrusleaf_get_all(clu, "user", str(j), key_obj, bins_get_all , size, 100, generation);
        # Number of bins returned
        number_bins = cl.intp_value(size)
        print "check1"
        # Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
        bins = pcl.get_bins (bins_get_all, number_bins)
        for i in xrange(number_bins):
            print "check2"
            if ((bins[i].object.type)==cl.CL_STR) & (bins[i].bin_name == "user_name") & ((bins[i].object.u.str) == u["username"] ): 
                print "duplicate"        
    #Insert User into user namespace
    user_count+=1
    print "check3"
    cl.citrusleaf_object_init_str(u0.object, str(u["name"]));
    cl.citrusleaf_object_init_str(u1.object, str(u["username"]));
    cl.citrusleaf_object_init_str(u2.object, str(u["password"]));
    print "check4"
    # Assign the structure back to the "bins" variable
    user[0] = u0
    user[1] = u1
    user[2] = u2
    print str(user_count)
    return_value = cl.citrusleaf_put(clu, "user", str(user_count), key_obj, user, 3, None);
    if return_value != cl.CITRUSLEAF_OK :
        print "1. Failure setting values ", return_value
        #sys.exit(-1);
    
    else:
        print "Success"
    
    print "return value is ", return_value
    print user_count
    '''
    
    '''deletion = cl.delete_intp(size)
    cl.delete_intp(generation)
    cl.delete_cl_bin_p(bins_get_all)
    deletion = cl.delete_intp(size)
    cl.citrusleaf_delete(clu, "user", "test", key_obj, deletion )
    cl.citrusleaf_delete(clu, "user", "rajiv", key_obj, deletion )
    cl.citrusleaf_delete(clu, "user", str(1), key_obj, deletion )
    cl.citrusleaf_delete(clu, "user", "myset", key_obj, deletion )
    '''
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
    
