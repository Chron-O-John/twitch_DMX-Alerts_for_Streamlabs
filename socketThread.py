import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

url = "https://sockets.streamlabs.com/socket.io/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkYwNzBBNUZDQjhDN0UxQzY5MDEwIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiNDMyMjk0NDg2In0.RCu48_ocKe_4nSmz1ZniDT0rB-ezIX1TJh5cpRSLz1g"
sio.connect(url)
#sio.wait()