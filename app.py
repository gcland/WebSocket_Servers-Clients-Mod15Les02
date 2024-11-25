from web_socket_server import WebSocketServer, socketio, app
from flask import render_template
import datetime

app = WebSocketServer().create_app()
message_storage = {
    #author (key): (value) [ { time: datetime, message: textMessage }, ... ]
}

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(message_package):
    print(f'Received message: {message_package}')
    user = message_package['user']
    message = message_package['message']
    current_time = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
    payload = {"time": current_time, "message": message}
    print(f'\n{current_time} User: {user}\nMessage: -> {message}')
    if user not in message_storage:
        message_storage[user] = [payload]
    else:
        message_storage[user].append(payload)

    print(message_storage)
    socketio.emit('message', payload)

@socketio.on('get_all_messages')
def handle_get_user_messages(data):
    socketio.emit('get_all_messages', message_storage)

@socketio.on('get_user_messages')
def handle_get_user_messages(data):
    user = data['user']
    print('User:', user)
    print(message_storage[user])
    socketio.emit('get_user_messages', message_storage[user])

@app.route('/')
def index():
    return render_template('WebSocketClient.html')

if __name__ == '__main__':
    socketio.run(app)