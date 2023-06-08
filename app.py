from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi, bcrypt, jwt, datetime
from bson import ObjectId
from bson.json_util import dumps


ca = certifi.where()

client = MongoClient('mongodb+srv://sparta:test@cluster0.vouw82r.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta

app = Flask(__name__)


current_user_id = "nobi1" # 임시

@app.route('/board/<board_id>')
def room(board_id):
    return render_template('board.html', id = board_id)

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        try:
            payload = jwt.decode(token_receive, "moyoboardza", algorithms=['HS256'])
            user_info = db.users.find_one({'user_id' : payload['user_id']})
            return render_template('index.html', user_info = user_info)
        except jwt.ExpiredSignatureError:
            return redirect(url_for('/', msg="로그인 시간이 만료되었습니다."))
        
    return render_template('index.html')

@app.route('/regist')
def signUp():
   return render_template('./auth/signup.html')

# 회원가입
@app.route('/regist', methods = ["POST"])
def regist():
    user_id = request.form['user_id']
    password = bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    nickname = request.form['nickname']
    phone = request.form['phone']
    doc = {
        'room_id'   : None,
        'user_id'   : user_id,
        'password'  : password,
        'nickname'  : nickname,
        'phone'     : phone
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원가입 되었습니다.'})
# 로그인
@app.route('/login', methods= ["POST"])
def login():
    user_id = request.form['user_id']
    password = request.form['password']
    print(user_id, password)
    user_info = db.users.find_one({'user_id':user_id}, {'_id':False})

    # password check
    if user_info is not None:
        if bcrypt.checkpw(password.encode("utf-8"), user_info['password'].encode("utf-8")) is True:
            # payload와 시크릿 키가 필요
            # 시크릿 키가 있어야 토큰을 디코딩 해서 payload 값을 볼 수 있음.
            payload = {
                'user_id' : user_id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            # jwt 암호화
            # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            token = jwt.encode(payload, "moyoboardza", algorithm="HS256")
            print(token)
            return jsonify({'result' : 'success', 'token' : token})
        else :
            return jsonify({'result': 'fail', 'msg': '비밀번호가 일치하지 않습니다.'})
    else : 
        return jsonify({'result': 'fail', 'msg': '아이디가 일치하지 않습니다.'})

@app.route("/board/get/<room_id>", methods=["GET"])
def board_get(room_id):
    board_get = db.room.find_one({"_id": ObjectId(room_id)}, {"max_people": False, "prt": False, "_id": False})
    if (current_user_id in board_get['prt_users']) :
        return jsonify({'result': dumps(board_get)})
    else :
        return jsonify({'msg': '참가한 적이 없는 방입니다!'})

@app.route("/room/list", methods=["GET"])
def room_list_get():
    all_board = list(db.room.find(
        {}, {"user_id": False, "location": False}))
    
# 결과적으로 room_name, room_info, max_people, prt, _id만 나오게 된다.
    return jsonify({'result': dumps(all_board)})

@app.route("/room/join", methods=["UPDATE"])
def room_join():
    room_id = ObjectId(request.form['room_id'])
    prt_users = db.room.find_one({"_id": room_id}, {"prt_users": True, "_id": False})["prt_users"]
    if (current_user_id in prt_users):
        return jsonify({'msg': '이미 참가한 방입니다!'})
    else:
        db.room.update_one({"_id": room_id}, {
                           "$inc": {"prt": 1}, "$push": {"prt_users": current_user_id}})
        return jsonify({'msg': '참가 완료!!'})


@app.route("/user/get/<user_id>", methods=["GET"])
def user_get(user_id):
    user_get = db.user.find_one({"user_id": user_id}, {"_id": False, "phone": True})
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
        return jsonify({'msg': '생성 실패!! 입력값을 확인해 주세요.'})

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
