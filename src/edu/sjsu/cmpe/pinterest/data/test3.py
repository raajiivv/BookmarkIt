'''
Created on May 13, 2014

@author: rajiv
'''

import citrusleaf as cl
import python_citrusleaf as pcl
import json
import zlib

# Initialize citrusleaf once
cl.citrusleaf_init()
# Create a cluster with a particular starting host
clu = cl.citrusleaf_cluster_create()
# Add host to the cluster
return_value = cl.citrusleaf_cluster_add_host(clu, "127.0.0.1", 3000, 1000)

# set up the key. Create a stack object, set its value to a string
key_obj = cl.cl_object()
cl.citrusleaf_object_init_str(key_obj, "rajiv")

u  = {"username" : "rajiv", "name" : "Rajiv" , "password":"password"}
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
    
size = cl.new_intp()
generation = cl.new_intp()
# Declare a reference pointer for cl_bin *
bins_get_all = cl.new_cl_bin_p()
rv = cl.citrusleaf_get_all(clu, "user", "rajiv", key_obj, bins_get_all , size, 100, generation);
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
