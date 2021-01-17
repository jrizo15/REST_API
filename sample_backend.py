from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS;
import random;
import string;


app = Flask(__name__)
CORS(app) # <--- add this line



@app.route('/')
def hello_world():
	return 'Hello, world!'

users = { 
   'users_list' :
   [
      { 
         'id' : 'xyz789',
         'name' : 'Charlie',
         'job': 'Janitor',
      },
      {
         'id' : 'abc123', 
         'name': 'Mac',
         'job': 'Bouncer',
      },
      {
         'id' : 'ppp222', 
         'name': 'Mac',
         'job': 'Professor',
      }, 
      {
         'id' : 'yat999', 
         'name': 'Dee',
         'job': 'Aspring actress',
      },
      {
         'id' : 'zap555', 
         'name': 'Dennis',
         'job': 'Bartender',
      }
   ]
}

def rand_id():
    abc = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
    num = ''.join(str(random.randint(0,9)) for i in range(3))
    return abc+num

@app.route('/users', methods=['GET', 'POST', 'DELETE'])
def get_users():
   if request.method == 'GET':
      search_username = request.args.get('name')
      search_job = request.args.get('job')
      if search_username and search_job:
            subdict = {'users_list' : []}
            for user in users['users_list']:
                if user['name'] == search_username:
                    if user['job'] == search_job:
                        subdict['users_list'].append(user)
            return subdict
      if search_username :
         subdict = {'users_list' : []}
         for user in users['users_list']:
            if user['name'] == search_username:
               subdict['users_list'].append(user)
         return subdict
      return users
   elif request.method == 'POST':
      userToAdd = request.get_json()
      if not('id' in userToAdd):
        userToAdd['id'] = rand_id()
      users['users_list'].append(userToAdd)
      resp = jsonify(userToAdd)
      resp.status_code = 201 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp
   elif request.method == 'DELETE':
      userToDelete = request.get_json()
      users['users_list'].remove(userToDelete)
      resp = jsonify(userToDelete)
      resp.status_code = 202 #optionally, you can always set a response code. 
      # 200 is the default code for a normal response
      return resp

@app.route('/users/<id>', methods=['GET','DELETE'])
def get_user(id):
   if request.method == 'DELETE':
      if id :
         for user in users['users_list']:
            if user['id'] == id:
               users['users_list'].remove(user)
               resp = jsonify(user)
               resp.status_code = 202
               return resp
         return ({})
   elif request.method == 'GET':
      if id:
         for user in users['users_list']:
            if user['id'] == id:
                return user
            return({})

   return users

