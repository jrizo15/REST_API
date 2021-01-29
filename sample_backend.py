from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS;
import random;
import string;
from model_mongodb import User



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
            result = User().find_by_name_job(search_username,search_job)
      elif search_username :
         result = User().find_by_name(search_username)
      else:
            result = User().find_all()
      
      return {"users_list":result}
   elif request.method == 'POST':
      userToAdd = request.get_json() # no need to generate an id ourselves
      newUser = User(userToAdd)
      newUser.save() # pymongo gives the record an "_id" field automatically
      resp = jsonify(newUser), 201
      return resp


@app.route('/users/<id>', methods=['GET','DELETE'])
def get_user(id):
   if request.method == 'DELETE':
      user = User({"_id":id})
      resp = user.remove()
      if resp["n"] == 1:
          return {},204
      else:
          return jsonify({"error": "User not found"}), 404
          
   elif request.method == 'GET':
      user = User({"_id":id})
      if user.reload() :
          return user
      else :
          return jsonify({"error": "User not found"}), 404


