from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import json_util
app = Flask(__name__)

client = MongoClient('mongodb+srv://loki:0000@cluster0.wcufqip.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta
@app.route('/')
def home():
    return render_template('create_room.html')

@app.route('/roomlist')
def gotojwpage():
    return render_template('roomlist.html')

@app.route("/create_room", methods=["POST"])
def create_room_post():
    room_name_receive = request.form['room_name_give']
    room_info_receive = request.form['room_info_give']
    max_people_receive = request.form['max_people_give']
    location_receive = request.form['location_give']
    user_id_receive = request.form['user_id_give']
    prt_users=[user_id_receive]


    room_num = list(db.room.find({}, {'_id': False}))
    #room_reader_id=db.room.find({'user_id':''})
    doc = {
        'room_name': room_name_receive,
        'room_info' : room_info_receive,
        'max_people' : max_people_receive,
        'location' : location_receive, 
        'prt' : 1,
        'user_id': user_id_receive,
        'prt_users':prt_users
    } 
    db.room.insert_one(doc)
    

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)