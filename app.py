from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
from bson import ObjectId
from bson.json_util import dumps


ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.vouw82r.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)

current_user_id = "nobi1" # 임시


@app.route('/board/<board_id>')
def room(board_id):
    return render_template('board.html', id=board_id)


@app.route('/')
def home():
    return render_template('index.html')


@app.route("/board/get/<room_id>", methods=["GET"])
def board_get(room_id):
    board_get = db.room.find_one({"_id": ObjectId(room_id)})
    if (current_user_id in board_get['prt_users']) :
        return jsonify({'result': dumps(board_get)})
    else :
        return jsonify({'msg': '참가한 적이 없는 방입니다!'})
    # 남들방 왜 들어가짐?
    # if user_id in board_get['prt_user'] # 유저아이디를 jwt로 받아서 그 아이디 값이 있는걸 확인 받고 값을 돌려주자. else로 msg를 보내면...


@app.route("/room/list", methods=["GET"])
def room_list_get():
    all_board = list(db.room.find(
        {}, {"user_id": False, "location": False}))
# 결과적으로 room_name, room_info, max_people, prt, _id만 나오게 된다.
    return jsonify({'result': dumps(all_board)})


@app.route("/room/join", methods=["UPDATE"])
def room_join():
    room_id = ObjectId(request.form['room_id'])
    prt_users = db.room.find_one({"_id": room_id})["prt_users"]
    if (current_user_id in prt_users):
        return jsonify({'msg': '이미 참가한 방입니다!'})
    else:
        db.room.update_one({"_id": room_id}, {
                           "$inc": {"prt": 1}, "$push": {"prt_users": current_user_id}})
        return jsonify({'msg': '참가 완료!!'})


@app.route("/user/get/<user_id>", methods=["GET"])
def user_get(user_id):
    user_get = db.user.find_one({"user_id": user_id}, {"_id": False})
    return jsonify({'result': user_get})


@app.route('/create_room')
def create_room():
    return render_template('create_room.html')


@app.route("/create_room", methods=["POST"])
def create_room_post():
    room_name_receive = request.form['room_name_give']
    room_info_receive = request.form['room_info_give']
    max_people_receive = request.form['max_people_give']
    location_receive = request.form['location_give']
    prt_users = [current_user_id]

    if (len(room_name_receive) < 1 or
        len(room_info_receive) < 1 or
        int(max_people_receive) < 2 or
        len(location_receive) < 1):
        return jsonify({'msg': '생성 실패!!'})

    # room_num = list(db.room.find({}, {'_id': False}))
    # room_reader_id=db.room.find({'user_id':''})
    doc = {
        'room_name': room_name_receive,
        'room_info': room_info_receive,
        'max_people': max_people_receive,
        'location': location_receive,
        'prt': 1,
        'user_id': current_user_id,
        'prt_users': prt_users
    }
    db.room.insert_one(doc)
    return jsonify({'msg': '생성 완료!!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
