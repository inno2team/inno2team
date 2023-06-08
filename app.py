from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi, bcrypt
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

@app.route('/regist')
def signUp():
   return render_template('./auth/signup.html')

# 회원가입
@app.route('/regist', methods = ["POST"])

def regist():
    print(request.form)
    user_id = request.form['user_id']
    password = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    nickname = request.form['nickname']
    phone = request.form['phone']
    doc = {
        'rood_id'   : None,
        'user_id'   : user_id,
        'password'  : password,
        'nickname'  : nickname,
        'phone'     : phone
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원가입 되었습니다.'})


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
    if (user_id in prt_users):
        return jsonify({'msg':'이미 참가한 방입니다!'})
    else:
        db.room.update_one({"_id" : room_id}, {"$inc" : {"prt" : 1}, "$push" :{"prt_users" : user_id}})
        return jsonify({'msg':'참가 완료!!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
