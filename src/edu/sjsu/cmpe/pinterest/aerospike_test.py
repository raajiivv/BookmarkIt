'''
Created on May 4, 2014

@author: rajiv
'''
import citrusleaf as cl
import python_citrusleaf as pcl
import sys
import zlib
from citrusleaf import cl_write_parameters


# Initialize citrusleaf once
cl.citrusleaf_init()
# Create a cluster with a particular starting host
asc = cl.citrusleaf_cluster_create()
# Add host to the cluster
return_value = cl.citrusleaf_cluster_add_host(asc, "127.0.0.1", 3000, 1000)



# set up the key. Create a stack object, set its value to a string
key_obj = cl.cl_object()
#key_obj2 = cl.cl_object()
cl.citrusleaf_object_init_str(key_obj, "rajiv")
#cl.citrusleaf_object_init_str(key_obj2, "newKeyObject")


# Declaring an array in this interface
bins = cl.cl_bin_arr(3)
cans = cl.cl_bin_arr(4)
tins = cl.cl_bin_arr(4)

# Provide values for those bins and then initialize them.
# Initializing bin of type string
b0 = bins[0]
b0.bin_name = "email"
cl.citrusleaf_object_init_str(b0.object, "support@citrusleaf.com");

# Initializing bin of type int
b1 = bins[1]
b1.bin_name = "hits"
cl.citrusleaf_object_init_int(b1.object, 314);


c0 = cans[0]
c0.bin_name = "name"
cl.citrusleaf_object_init_str(c0.object, "Rajiv");

c1 = cans[1]
c1.bin_name = "username"
cl.citrusleaf_object_init_str(c1.object, "rajiv");

c2 = cans[2]
c2.bin_name = "password"
cl.citrusleaf_object_init_str(c2.object, "password");

pin_id=1

t0 = tins[0]
t0.bin_name = "board_id"
cl.citrusleaf_object_init_int(t0.object,pin_id)

t1 = tins[1]
t1.bin_name = "board_name"
cl.citrusleaf_object_init_str(t1.object, "Some name");

t2 = tins[2]
t2.bin_name = "pins"
cl.citrusleaf_object_init_str(t2.object, "1,2,3,4,5");



# Assign the structure back to the "bins" variable
bins[0] = b0
bins[1] = b1


cans[0] = c0
cans[1] = c1
cans[2] = c2

tins[0] = t0
tins[1] = t1
tins[2] = t2



'''return_value2 = cl.citrusleaf_put(asc, "user", "rajiv", key_obj, bins, 2, None);
if return_value != cl.CITRUSLEAF_OK :
    print "1. Failure setting values ", return_value
    #sys.exit(-1);
    
else:
    print "Success"


return_value2 = cl.citrusleaf_put(asc, "user", "rajiv", key_obj, cans, 3, None )
if return_value2 !=cl.CITRUSLEAF_OK :
    print "2. Falied to set values %d", return_value2
    #sys.exit(-1)
else :
    print "Success"

return_value2 = cl.citrusleaf_put(asc, "user", "rajiv", key_obj, tins, 3, None )
if return_value2 !=cl.CITRUSLEAF_OK :
    print "3. Falied to set values %d", return_value2
    #sys.exit(-1)
else :
    print "Success"'''



size = cl.new_intp()
generation = cl.new_intp()
# Declare a reference pointer for cl_bin *
bins_get_all = cl.new_cl_bin_p()
rv = cl.citrusleaf_get_all(asc, "user", "rajiv", key_obj, bins_get_all , size, 100, generation);
# Number of bins returned
number_bins = cl.intp_value(size)
# Use helper function get_bins to get the bins from pointer bins_get_all and the number of bins
bins = pcl.get_bins (bins_get_all, number_bins)

if number_bins>0:
    print "something", number_bins
else:
    print "nothing", number_bins
    

# Printing value received
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




# Delete
cl.citrusleaf_free_bins(bins, number_bins, bins_get_all)
deletion = cl.delete_intp(size)
cl.delete_intp(generation)
cl.delete_cl_bin_p(bins_get_all)
deletion = cl.delete_intp(size)
cl.citrusleaf_delete(asc, "user", "test", key_obj, deletion )
cl.citrusleaf_delete(asc, "user", "rajiv", key_obj, deletion )
cl.citrusleaf_delete(asc, "user", str(1), key_obj, deletion )
cl.citrusleaf_delete(asc, "user", "myset", key_obj, deletion )