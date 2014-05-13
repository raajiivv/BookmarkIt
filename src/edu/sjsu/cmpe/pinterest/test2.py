'''
Created on May 5, 2014

@author: rajiv
'''

from bottle import Bottle, run, template

app = Bottle()

@app.route('/<temp:re:[r]*>')
def routing(temp):
    return template("{{id}}", id=temp)


run(app, host = "localhost", port = 8080, debug = True)
