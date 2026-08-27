from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

game_state = {
    "is_active": False,
    "results": []
}

@app.route('/')
def student_page():
    return render_template('student.html')

@app.route('/teacher')
def teacher_page():
    return render_template('teacher.html')

@socketio.on('start_game')
def handle_start():
    game_state["results"] = []
    game_state["is_active"] = False
    # 1. ส่งคำสั่งให้นักเรียนเริ่มนับถอยหลัง 3 2 1 บนหน้าจอ
    emit('countdown', {"seconds": 3}, broadcast=True)
    
    # 2. ให้ Server รอ 3 วินาที (ให้ตรงกับที่นักเรียนนับ)
    socketio.sleep(3.5) # เผื่อดีเลย์นิดหน่อย 0.5 วิ
    
    # 3. ปลดล็อคปุ่มทุกคนพร้อมกัน
    game_state["is_active"] = True
    emit('unlock_button', broadcast=True)

@socketio.on('press_button')
def handle_press(data):
    if game_state["is_active"]:
        if not any(r['name'] == data['name'] for r in game_state["results"]):
            result = {
                "name": data['name'],
                "time": data['time'],
                "rand_id": random.random()
            }
            game_state["results"].append(result)
            sorted_results = sorted(game_state["results"], key=lambda x: (x['time'], x['rand_id']))
            emit('update_results', sorted_results, broadcast=True)

@socketio.on('reset_game')
def handle_reset():
    game_state["results"] = []
    game_state["is_active"] = False
    emit('reset_all', broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)