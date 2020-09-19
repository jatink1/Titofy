from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import jwt
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "this_is_a_secret_which_needs_to_be_randomly_generated_later"
app.config["MONGO_DBNAME"] = "Titofy"
app.config["MONGO_URI"] = "mongodb://admin:admin@cluster0-shard-00-00.whvvy.gcp.mongodb.net:27017,cluster0-shard-00-01.whvvy.gcp.mongodb.net:27017,cluster0-shard-00-02.whvvy.gcp.mongodb.net:27017/titofy?ssl=true&replicaSet=atlas-fk68jm-shard-0&authSource=admin&retryWrites=true&w=majority"

# "mongodb://admin:admin@cluster0-shard-00-00.whvvy.gcp.mongodb.net:27017,cluster0-shard-00-01.whvvy.gcp.mongodb.net:27017,cluster0-shard-00-02.whvvy.gcp.mongodb.net:27017/titofy?ssl=true&replicaSet=atlas-fk68jm-shard-0&authSource=admin&retryWrites=true&w=majority"

mongo = PyMongo(app)

users = mongo.db.users

@app.route('/signup', methods=['POST'])
def signup():
  _json = request.json

  name = _json['name']
  email = _json['email']
  password = _json['password']

  if _json and name and email and password and len(password)>=8:
    # Check same email throw err
    checkEmail = users.find_one({ 'email': email })
    if checkEmail:
      response = jsonify("Email already in use!")
      response.status_code = 409
      return response

    # hash and store in MongoDB
    hashed = hashlib.sha256(_json['password'].encode('utf-8')).hexdigest()
    user = {
      "name": name,
      "email": email,
      "password": hashed
    }
    objid = users.insert_one(user).inserted_id
    # generate JWT token
    token = jwt.encode({ 'email': email, 'id': str(objid) }, app.config["SECRET_KEY"])

    # Response 200
    message = {'message': 'User registered in successfully', 'token': token.decode('UTF-8')}
    response = jsonify(message)
    response.status_code = 200
    return response
  
  # Response 401
  response = jsonify("Couldn't signup!")
  response.status_code = 401
  return response

@app.route('/login', methods=['POST'])
def login():
  auth = request.json

  if auth and len(auth['email'])>=3 and len(auth['password'])>=8:
    # get document from db and verify then send jwt
    hashed = hashlib.sha256(auth['password'].encode('utf-8')).hexdigest()
    user = users.find_one({ 'email': auth['email'], 'password': hashed })
    if user:
      # generate JWT token
      objid = user['_id']
      token = jwt.encode({ 'email': auth['email'], 'id': str(objid) }, app.config["SECRET_KEY"])
      message = {'message': 'User logged in successfully', 'token': token.decode('UTF-8')}
      # Response 200
      response = jsonify(message)
      response.status_code = 200
      return response
    else:
      # Response 201
      response = jsonify("Incorrect email or password!")
      response.status_code = 201
      return response

  # Response 401
  response = jsonify("Couldn't verify!")
  response.status_code = 401
  return response

@app.route('/update', methods=['POST'])
def update():
  return "Update Profile"

if __name__=="__main__":
  app.run(debug=True)