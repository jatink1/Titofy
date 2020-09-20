from flask import Flask, request, jsonify, send_file
from flask_pymongo import PyMongo, ObjectId
from datetime import datetime, date
import os
import jwt
import hashlib
from spot import *
from input_1 import *

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'public'

app = Flask(__name__)
app.config["SECRET_KEY"] = "this_is_a_secret_which_needs_to_be_randomly_generated_later"
app.config["MONGO_DBNAME"] = "Titofy"
app.config["MONGO_URI"] = "mongodb://admin:admin@cluster0-shard-00-00.whvvy.gcp.mongodb.net:27017,cluster0-shard-00-01.whvvy.gcp.mongodb.net:27017,cluster0-shard-00-02.whvvy.gcp.mongodb.net:27017/titofy?ssl=true&replicaSet=atlas-fk68jm-shard-0&authSource=admin&retryWrites=true&w=majority"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mongo = PyMongo(app)

users = mongo.db.users
lists = mongo.db.lists
chats = mongo.db.chats

@app.route('/signup', methods=['POST'])
def signup():
  _form = request.form
  name = _form['name']
  email = _form['email']
  password = _form['password']
  dob = _form['dob']
  gender = _form['gender']
  orient = _form['orient']
  preferance = _form['preferance']
  spotify = _form['spotify']

  # Calculating age for minimum age limit
  date_of_birth = datetime.strptime(dob, '%d-%m-%Y').date()
  today = date.today()
  age = today.year-date_of_birth.year-((today.month, today.day)<(date_of_birth.month, date_of_birth.day))

  if age<18:
    response = jsonify("The user must be above the age of 18")
    response.status_code = 201
    return response

  if _form and name and email and password and len(password)>=8:
    # Check same email throw err
    checkEmail = users.find_one({ 'email': email })
    if checkEmail:
      response = jsonify("Email already in use!")
      response.status_code = 409
      return response

    # hash and store in MongoDB
    hashed = hashlib.sha256(_form['password'].encode('utf-8')).hexdigest()
    timestamp = datetime.timestamp(datetime.now())
    spotify_username = spotify.split('/').pop()
    main(spotify_username)
    cluster = get_cluster()
    user = {
      "name": name,
      "email": email,
      "password": hashed,
      "gender": gender,
      "orient": orient,
      "preferance": preferance,
      "dob": dob,
      "spotify": spotify,
      "cluster": cluster,
      "last": 0
    }
    objid = users.insert_one(user).inserted_id
    accept_obj = {
      "user": str(objid),
      "accept": []
    }
    list_id = lists.insert_one(accept_obj)
    chat_obj = {
      "user": str(objid),
      "chats": []
    }
    chat_id = chats.insert_one(chat_obj)

    # storing image
    file = request.files['display']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(objid)))

    # generate JWT token
    token = jwt.encode({ 'email': email, 'id': str(objid) }, app.config["SECRET_KEY"])

    # Response 200
    message = {'message': 'User registered in successfully', 'token': token.decode('UTF-8')}
    response = jsonify(message)
    response.status_code = 200
    return response
  
  # Response 401
  response = jsonify("Couldn't register user!")
  response.status_code = 401
  return response

@app.route('/login', methods=['POST'])
def login():
  auth = request.json
  if auth and auth['email'] and len(auth['password'])>=8:
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
  response = jsonify("Couldn't verify user!")
  response.status_code = 401
  return response

@app.route('/profile', methods=['POST'])
def profile():
  # return users profile
  return "Profile"

@app.route('/displaypic/<uid>', methods=['GET'])
def display(uid):
  try:
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'],uid), mimetype='image')
  except: 
    return "User doesn't exist"

@app.route('/action/<action_type>', methods=['POST'])
def cardaction(action_type):
  _form = request.json
  uid = _form['id']
  token = _form['token']
  try: 
    payload = jwt.decode(token, app.config["SECRET_KEY"])
    last = users.find_one({ '_id': ObjectId(payload['id']) })['last']
    query = {"user": uid}
    if action_type=='accept':
      accept_obj = lists.find_one(query)
      if uid in accept_obj['accept']:
        # push notif
        accept_obj['accept'].remove(uid)
        setter = {"$set": { "accept": accept_obj['accept'] }}
        lists.update_one(query, setter)
        chats_obj = chats.find_one(query)
        chats_obj['chats'].append(payload['id'])
        setter = {"$set": { "chats": chats_obj['chats'] }}
        chats.update_one(query, setter)
        # increment last
        users.update_one({ '_id': ObjectId(payload['id']) }, { "$set": { "last": last+1 } })
        return "matched and chat pushed"
      else:
        accept_obj['accept'].append(uid)
        setter = {"$set": { "accept": accept_obj['accept'] }}
        lists.update_one(query, setter)
        # increment last
        users.update_one({ '_id': ObjectId(payload['id']) }, { "$set": { "last": last+1 } })
        return "accepted"
    if action_type=='rejected':
      # increment last
      users.update_one({ '_id': ObjectId(payload['id']) }, { "$set": { "last": last+1 } })
      return "rejected"
    return "Invalid type!"
  except:
    return "Invalid token"

@app.route('/cards/<size>', methods=['POST'])
def carddata(size):
  _form = request.json
  token = _form['token']
  try:
    payload = jwt.decode(token, app.config["SECRET_KEY"])
    user = users.find_one({ '_id': ObjectId(payload['id']) })
    last = user['last']
    # fetch data from mongo based on user preferances
    if last==0:
      query = {
        "gender": user['preferance'],
        "preferance": user['gender'],
        "cluster": user['cluster']
      }
      sent = []
      for human in users.find(query).limit(int(size)):
        date_of_birth = datetime.strptime(human["dob"], '%d-%m-%Y').date()
        today = date.today()
        age = today.year-date_of_birth.year-((today.month, today.day)<(date_of_birth.month, date_of_birth.day))
        data = {
          "id": str(human["_id"]),
          "name": human["name"],
          "gender": human["gender"],
          "age": age,
          "spotify": human["spotify"]
        }
        if data['id'] != payload['id']:
          sent.append(data)
      return jsonify({"data": sent, "message": "card data sent!"})
    else:
      query = {
        "gender": user['preferance'],
        "preferance": user['gender'],
        "cluster": user['cluster']
      }
      sent = []
      for human in users.find(query).skip(last).limit(int(size)):
        date_of_birth = datetime.strptime(human["dob"], '%d-%m-%Y').date()
        today = date.today()
        age = today.year-date_of_birth.year-((today.month, today.day)<(date_of_birth.month, date_of_birth.day))
        data = {
          "id": str(human["_id"]),
          "name": human["name"],
          "gender": human["gender"],
          "age": age,
          "spotify": human["spotify"]
        }
        if data['id']!=payload['id']:
          sent.append(data)
      message = {
        "data": sent,
        "message": "card data sent!"
      }
      return jsonify(message)
  except:
    return "Invalid token!"

if __name__=="__main__":
  app.run(debug=True)