'''
Created on May 12, 2014

@author: rajiv
'''
x = "1,2,3,4"
y = x.split(",")
y.append("5")
print y
x  = str(y)
print x

user = {"u":1, "y":"d"}

x = user ["u"]

if user.has_key("k"):
    