import os
import random
import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'buzzer_secret_123'
# อนุญาตให้เชื่อมต่อจากทุกที่
socketio = SocketIO(app, cors_allowed_origins="*")

# เก็บสถานะของเกม
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

# เมื่ออาจารย์สั่งเริ่ม
@socketio.on('start_game')
def handle_start():
    game_state["results"] = []
    game_state["is_active"] = False
    # ส่งสัญญาณให้นับถอยหลัง 3 2 1
    emit('countdown', {"seconds": 3}, broadcast=True)
    
    # รอ 3.5 วินาทีเพื่อให้ตรงกับหน้าจอ
    socketio.sleep(3.5)
    
    game_state["is_active"] = True
    emit('unlock_button', broadcast=True)

# เมื่อนักเรียนกดปุ่ม
@socketio.on('press_button')
def handle_press(data):
    if game_state["is_active"]:
        # เช็คว่าชื่อนี้เคยกดหรือยัง
        if not any(r['name'] == data['name'] for r in game_state["results"]):
            result = {
                "name": data['name'],
                "time": data['time'],
                "rand_id": random.random() # สำหรับสุ่มถ้าเวลาเท่ากันเป๊ะ
            }
            game_state["results"].append(result)
            
            # เรียงลำดับตามเวลา ใครน้อยกว่า (เร็วกว่า) อยู่บน
            sorted_results = sorted(game_state["results"], key=lambda x: (x['time'], x['rand_id']))
            
            # ส่งผลลัพธ์กลับไปให้อาจารย์และนักเรียนดู
            emit('update_results', sorted_results, broadcast=True)

# รีเซตเกม
@socketio.on('reset_game')
def handle_reset():
    game_state["results"] = []
    game_state["is_active"] = False
    emit('reset_all', broadcast=True)

if __name__ == '__main__':
    # ตั้งค่า Port สำหรับ Render
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)