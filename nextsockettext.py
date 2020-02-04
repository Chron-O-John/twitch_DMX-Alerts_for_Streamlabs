import time
import socketio
import threading

sio = socketio.Client(logger=True)
start_timer = None


def send_ping():
    print('send_ping called')
    global start_timer
    start_timer = time.time()
    sio.emit('ping_from_client')


@sio.event
def connect():
    print('connected to server123')
    #send_ping()


@sio.event
def pong_from_server(data):
    global start_timer
    latency = time.time() - start_timer
    print('latency is {0:.2f} ms'.format(latency * 1000))
    sio.sleep(1)
    send_ping()

@sio.event
def message(data):
    print('tqwtw')

@sio.event
def event(data):
    print('Received data: ', data)

class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_my_event(self, data):
        #self.emit('my_response', data)
        print("TEst")


if __name__ == '__main__':
    url = "https://sockets.streamlabs.com/socket.io/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbiI6IkYwNzBBNUZDQjhDN0UxQzY5MDEwIiwicmVhZF9vbmx5Ijp0cnVlLCJwcmV2ZW50X21hc3RlciI6dHJ1ZSwidHdpdGNoX2lkIjoiNDMyMjk0NDg2In0.RCu48_ocKe_4nSmz1ZniDT0rB-ezIX1TJh5cpRSLz1g"
    #sio.connect(url)
    #sio.register_namespace(MyCustomNamespace())
    wst = threading.Thread(target=sio.connect(url))
    wst.daemon = True
    wst.start()
    count = 0
    while True:
        count = count+1
        print(count)
        time.sleep(1)

    # sio.connect(url)
    #sio.wait()