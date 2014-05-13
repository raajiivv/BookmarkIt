'''
Created on May 5, 2014

@author: rajiv
'''
from bottle import get, post, request, run, Bottle, route

#app = Bottle()

#@app.get('/login')
@route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

#@app.post('/login')
@route('/login', method = 'POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"

def check_login(u,p):
    print u,p
    if (u=="rajiv") and ("p==rajiv"):
        return True
    else:
        return False

run( host = "localhost", port = 8080, debug = True)
