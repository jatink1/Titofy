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
    # Check same email throw err --not done

    # hash and store in MongoDB --done
    hashed = hashlib.sha256(_json['password'].encode('utf-8')).hexdigest()
    user = {
      "name": name,
      "email": email,
      "password": hashed
    }
    objid = users.insert_one(user)

    # generate JWT token
    token = jwt.encode({ 'email': email, 'id': str(objid) }, app.config["SECRET_KEY"])

    # Response 200
    message = {'message': 'User registered in successfully', 'token': token.decode('UTF-8')}
    response = jsonify(message)
    response.status_code = 200
    return response
  
  # Response 401
  response = jsonify("Couldn't verify!")
  response.status_code = 401
  return response

@app.route('/login', methods=['POST'])
def login():
  auth = request.json

  if auth and len(auth['email'])>=3 and len(auth['password'])>=8:
    # get document from db and verify then send jwt
    objid = '123456'
    token = jwt.encode({ 'email': auth['email'], 'id': objid }, app.config["SECRET_KEY"])
    message = {'message': 'User logged in successfully', 'token': token.decode('UTF-8')}
    response = jsonify(message)
    response.status_code = 200
    return response

  response = jsonify("Couldn't verify!")
  response.status_code = 401
  return response


if __name__=="__main__":
  app.run(debug=True)