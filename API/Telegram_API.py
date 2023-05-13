try:
    from flask import Flask, jsonify, request
    from pymongo import MongoClient
    from bson.json_util import dumps
    from bson.objectid import ObjectId
    import json
    from datetime import datetime
    import time
    from bson import json_util
    from flask_socketio import SocketIO
    from flask_cors import CORS
except Exception as e:
    print("Some Modules are Missing :{}".format(e))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# socketio = SocketIO(app, cors_allowed_origins="*")
# CORS(app)

# database connection
def databaseConnection():
   CONNECTION_STRING = "mongodb+srv://emseccomandcenter:TUXnEN09VNM1drh3@cluster0.psiqanw.mongodb.net/?retryWrites=true&w=majority"
   client = MongoClient(CONNECTION_STRING)
   return client['Telegram_Server']
db = databaseConnection()
# this database contain information about Channel
collection = db["channel_info"]

# display all channel
@app.route('/allChannel',methods=['GET'])
def users():
	users = collection.find()
	resp = dumps(users)
	return resp

# socket send data
# @app.route('/sendData',methods=['POST'])
# def sendData():
#     data=request.json['data']
#     socketio.emit('data',data)
#     return jsonify({'result':'OK'})

# # socket send log
# @app.route('/sendLog',methods=['POST'])
# def sendLog():
#     data=request.json['msg']
#     socketio.emit('log',data)
#     return jsonify({'result':'OK'})

# GET and UPDATE Channel
@app.route('/TelegramChannel/<id>', methods=['GET','DELETE','PUT'])
def Telegram_Channel(id):
    if request.method=='GET':
        try:
            data =collection.find_one({'_id':ObjectId(id)})
            user = dumps(data)
            return user
        except:
            resp = jsonify("No Content")
            resp.status_code = 204
            return resp

    if request.method=='DELETE':
        try:
            query = {"_id": ObjectId(id)}
            collection.delete_one(query)
            resp = jsonify("Channel Deleted")
            resp.status_code = 200
            return resp
        except:
            resp = jsonify("Already Deleted")
            resp.status_code = 208
            return resp

    if request.method=='PUT':
        _isUrgent = request.json['isUrgent']
        collection.update_one({"_id":ObjectId(id)},{"$set":{"isUrgent":_isUrgent}})
        resp = jsonify("Updated")
        resp.status_code = 200
        return resp

# Add Channel
@app.route('/TelegramChannel', methods=['POST'])
def post():
    url =request.json['url'] 
    failed_count = 0
    status = "not started"
    time = datetime.strptime(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), "%Y-%m-%dT%H:%M:%S")
    isUrgent = False
    
    if collection.count_documents({'url':url})>0:
        resp = jsonify("Channel Already exist.. Update the field if you need")
        resp.status_code = 207
        return resp
    if request.method == "POST":
        collection.insert_one({'url':url,'failedCount':failed_count,'status':status,'time':time,'isUrgent':isUrgent})
        resp = jsonify("Channel added successfully")
        resp.status_code = 200
        return resp
    else:
        return not_found()

# Error Handler
@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status': 404,
        'message' : 'Not Found' + request.url
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp    

# main Function
if __name__=='__main__':
    app.run(debug=True)
