import os
import random
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

game_state = {"is_active": False, "results": []}

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
    emit('countdown', {"seconds": 3}, broadcast=True)
    socketio.sleep(3.5)
    game_state["is_active"] = True
    emit('unlock_button', broadcast=True)

@socketio.on('press_button')
def handle_press(data):
    if game_state["is_active"]:
        if not any(r['name'] == data['name'] for r in game_state["results"]):
            result = {"name": data['name'], "time": data['time'], "rand_id": random.random()}
            game_state["results"].append(result)
            sorted_results = sorted(game_state["results"], key=lambda x: (x['time'], x['rand_id']))
            emit('update_results', sorted_results, broadcast=True)

@socketio.on('reset_game')
def handle_reset():
    game_state["results"] = []
    game_state["is_active"] = False
    emit('reset_all', broadcast=True)

if __name__ == '__main__':
    # ส่วนนี้สำคัญเพื่อให้ Render รันได้
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)