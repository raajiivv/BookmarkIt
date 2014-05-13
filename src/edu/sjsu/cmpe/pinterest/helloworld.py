'''
Created on May 4, 2014

@author: rajiv
'''
from bottle import route, run, template

@route('/')
@route('/hello/<name>')

def hello(name = "Stranger"):
    return template("<b>Hello {{name}}! How are you?<b>", name = name);

run(host='localhost', port=8080, debug=True)