from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.zqvmomu.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/board/<board_id>')
def room(board_id):
   return render_template('board.html', id = board_id)


@app.route("/board/get/<room_id>", methods=["GET"])
def board_get(room_id):
    board_get = db.board.find_one({'room_id':room_id},{'_id':False})
    return jsonify({'result':board_get})



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)