import os # เพิ่มไว้ด้านบนสุดของไฟล์

# ... โค้ดเดิมของคุณ ...

if __name__ == '__main__':
    # ดึงค่า Port ที่ Render กำหนดมาให้ ถ้าไม่มีให้ใช้ 10000
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port)