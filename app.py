from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
from bson import ObjectId
from bson.json_util import dumps

ca = certifi.where()

client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.vouw82r.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_room')
def create_room():
    return render_template('create_room.html')


@app.route("/room/list", methods=["GET"])
def room_list_get():
    all_board = list(db.room.find(
        {}, {"user_id": False, "location": False}))
# 결과적으로 room_name, room_info, max_people, prt, _id만 나오게 된다.
    return jsonify({'result': dumps(all_board)})

@app.route("/room/join", methods=["UPDATE"])
def room_join():
    user_id = request.form['user_id']
    room_id = ObjectId(request.form['room_id'])
    prt_users = db.room.find_one({"_id": room_id})["prt_users"]
    # user_room_id = db.user.find_one({"user_id": user_id})["room_id"]
    # if (room_id == user_room_id):
    #     return jsonify({'msg':'이미 참가한 방입니다!'})
    # else :
    #     if (user_room_id is None) :
    #         db.room.update_one({"_id" : room_id}, {"$inc" : {"prt" : 1}, "$push" :{"prt_users" : user_id}})
    #         return jsonify({'msg':'참가 완료!!'})
    #     else :
    #         return jsonify({'msg':'이미 참가중인 방이 있습니다!'})
    if (user_id in prt_users) :
        return jsonify({'msg':'이미 참가한 방입니다!'})
    else :
        db.room.update_one({"_id" : room_id}, {"$inc" : {"prt" : 1}, "$push" :{"prt_users" : user_id}})
        return jsonify({'msg':'참가 완료!!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
