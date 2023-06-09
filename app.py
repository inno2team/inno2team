from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import certifi, bcrypt, jwt, datetime
from bson import ObjectId
from bson.json_util import dumps


ca = certifi.where()

client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.vouw82r.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)

db = client.dbsparta

app = Flask(__name__)


@app.route('/board/<board_id>')
def room(board_id):
    return render_template('board.html', id = board_id)

@app.route('/')
def home():
    current_user_id = get_current_user_id(request.cookies.get('mytoken'))
    if current_user_id is not None:
        user_info = db.users.find_one({'user_id': current_user_id})
        return render_template('index.html', user_info = user_info)
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
        'user_id'   : user_id,
        'password'  : password,
        'nickname'  : nickname,
        'phone'     : phone
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success', 'msg': '회원가입 되었습니다.'})

@app.route('/validate', methods = ["POST"])
def validate():
    user_id = request.form['user_id']
    findUser = db.users.find_one({'user_id': user_id}, {'_id': False})
    if findUser is not None:
        return jsonify({'result': 'fail', 'msg': '중복된 아이디 입니다. 다시 입력하세요.'})
    else :
        return jsonify({'result': 'success', 'msg': '사용 가능한 아이디 입니다.'})
    
# 로그인
@app.route('/login', methods= ["POST"])
def login():
    user_id = request.form['user_id']
    password = request.form['password']
    user_info = db.users.find_one({'user_id':user_id}, {'_id':False})

    # password check
    if user_info is not None:
        if bcrypt.checkpw(password.encode("utf-8"), user_info['password'].encode("utf-8")) is True:
            # payload와 시크릿 키가 필요
            # 시크릿 키가 있어야 토큰을 디코딩 해서 payload 값을 볼 수 있음.
            payload = {
                'user_id' : user_id,
                'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=3)
            }
            # jwt 암호화
            # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
            token = jwt.encode(payload, "moyoboardza", algorithm="HS256")
            return jsonify({'result' : 'success', 'msg': '로그인 완료!', 'token' : token})
        else :
            return jsonify({'result': 'fail', 'msg': '비밀번호가 일치하지 않습니다.'})
    else : 
        return jsonify({'result': 'fail', 'msg': '아이디가 일치하지 않습니다.'})
# my page 
@app.route('/mypage')
def move_mypage():
   return render_template('mypage.html')

@app.route("/mypage/update", methods=["UPDATE"])
def update_user_info():
    current_user_id = get_current_user_id(request.cookies.get('mytoken'))
    password_recieve = request.form['password_give']
    new_password_recieve = bcrypt.hashpw(request.form['new_password_give'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    nickname_recieve = request.form['nickname_give']
    phone_recieve = request.form['phone_give']

    user_info= db.users.find_one({"user_id": current_user_id})
    if bcrypt.checkpw(password_recieve.encode("utf-8"), user_info['password'].encode("utf-8")) is True:
        db.users.update_one({"user_id": current_user_id}, {"$set" : {"password": new_password_recieve, "nickname": nickname_recieve, "phone": phone_recieve}})
        return jsonify({'msg': '수정 완료'})
    else:
        return jsonify({'msg': '비밀번호가 틀립니다!'})
    
@app.route("/mypage/room/list", methods=["GET"])
def mypage_room_list_get():
    current_user_id = get_current_user_id(request.cookies.get('mytoken'))
    mypage_room_list = list(db.rooms.find(
        {"user_id": current_user_id}, {"user_id": False, "location": False}))
    return jsonify({'result': dumps(mypage_room_list)})

# 방 내부
@app.route("/board/get/<room_id>", methods=["GET"])
def board_get(room_id):
    current_user_id = get_current_user_id(request.cookies.get('mytoken'))
    board_get = db.rooms.find_one({"_id": ObjectId(room_id)}, {"_id": False})
    owner = board_get['user_id']
    owner_nickname = db.users.find_one({"user_id": owner})['nickname']
    if (current_user_id in board_get['prt_users']) :
        return jsonify({'result': board_get, 'nickname': owner_nickname})
    elif (current_user_id == None):
        return jsonify({'msg': '로그인이 필요합니다!'})
    else :
        return jsonify({'msg': '이미 마감된 방입니다!'})
# 방 리스트
@app.route("/room/list", methods=["GET"])
def room_list_get():
    all_board = list(db.rooms.find(
        {}, {"user_id": False, "location": False}))
# 결과적으로 room_name, room_info, max_people, prt, _id만 나오게 된다.
    return jsonify({'result': dumps(all_board)})

@app.route("/room/join", methods=["UPDATE"])
def room_join():
    current_user_id = get_current_user_id(request.cookies.get('mytoken'))
    room_id = ObjectId(request.form['room_id'])
    prt_users = db.rooms.find_one({"_id": room_id}, {"prt_users": True, "_id": False})["prt_users"]
    if (current_user_id in prt_users):
        return jsonify({'msg': '이미 참가한 방입니다!'})
    elif (current_user_id == None):
        return jsonify({'msg': '로그인이 필요합니다!'})
    else:
        db.rooms.update_one({"_id": room_id}, {
                           "$inc": {"prt": 1}, "$push": {"prt_users": current_user_id}})
        return jsonify({'msg': '참가 완료!!'})


@app.route("/user/get/<user_id>", methods=["GET"])
def user_get(user_id):
    user_get = db.users.find_one({"user_id": user_id}, {"_id": False})
    return jsonify({'result': user_get})


@app.route('/create_room')
def create_room():
    return render_template('create_room.html')



@app.route("/delete", methods=["DELETE"])
def delete_room():
    room_id_recieve = ObjectId(request.form['room_id'])
    token_receive = request.cookies.get('mytoken')
    if token_receive is not None:
        try:
            payload = jwt.decode(token_receive, "moyoboardza", algorithms=['HS256'])
            user_info = db.users.find_one({'user_id': payload['user_id']})
        except jwt.ExpiredSignatureError:
            return None
        reader_recieve = db.rooms.find_one({'_id':room_id_recieve})
        if reader_recieve['user_id'] == user_info['user_id']:
            db.rooms.delete_one({'_id': reader_recieve['_id']})
            return jsonify({'msg': '삭제 완료'})
        else:
            return jsonify({'msg': "삭제 불가"})




@app.route("/create_room", methods=["POST"])
def create_room_post():
    current_user_id = get_current_user_id(request.cookies.get('mytoken'))
    room_name_receive = request.form['room_name_give']
    room_info_receive = request.form['room_info_give']
    max_people_receive = request.form['max_people_give']
    location_receive = request.form['location_give']
    prt_users = [current_user_id]

    if (current_user_id == None):
        return jsonify({'msg': '로그인이 필요합니다!'})
    elif (len(room_name_receive) < 1 or
        len(room_info_receive) < 1 or
        int(max_people_receive) < 2 or
        len(location_receive) < 1):
        return jsonify({'msg': '생성 실패!! 입력값을 확인해 주세요.'})
    else:

        doc = {
            'room_name': room_name_receive,
            'room_info': room_info_receive,
            'max_people': max_people_receive,
            'location': location_receive,
            'prt': 1,
            'user_id': current_user_id,
            'prt_users': prt_users
        }
        db.rooms.insert_one(doc)
        return jsonify({'msg': '생성 완료!!'})

def get_current_user_id(token_receive):
    if token_receive is not None:
        try:
            payload = jwt.decode(token_receive, "moyoboardza", algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
    return None       

@app.route("/comment/get/<room_id>", methods=["GET"])
def comment_get(room_id):
    all_comment = list(db.comment.find({"room_id": room_id}))
    return jsonify({'result': dumps(all_comment)})

@app.route("/comment/save/<room_id>", methods=["POST"])
def comment_save(room_id):
    comment_receive = request.form['comment_give']
    room_id_receive = room_id
    current_user_id = get_current_user_id(request.cookies.get('mytoken'))
    user_info = db.users.find_one({'user_id': current_user_id})

    doc = {
        'comment' : comment_receive,
        'room_id': room_id_receive,
        'nickname': user_info['nickname'],
        'user_id' : user_info['user_id']
    }
    db.comment.insert_one(doc)

    return jsonify({'msg': '저장완료'})

@app.route("/comment/delete", methods=["POST"])
def comment_delete():
    comment_obj_id = ObjectId(request.form['comment_id_give'])
    current_user_id = get_current_user_id(request.cookies.get('mytoken'))
    user_info = db.users.find_one({'user_id': current_user_id})

    comment_user_id = db.comment.find_one({'_id' : comment_obj_id})['user_id']

    if user_info['user_id'] == comment_user_id:
        doc = {
            '_id' : comment_obj_id
        }
        db.comment.delete_one(doc)
        return jsonify({'msg': '삭제완료'})
    else:
        return jsonify({'msg': '작성자가 아닙니다.'})
    


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)