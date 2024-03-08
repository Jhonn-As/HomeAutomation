import socketio

sio = socketio.Client()

# URL del servidor Flask donde se encuentra Socket.IO
server_url = 'http://localhost:5000'

@sio.event
def connect():
    print('Connection established')

@sio.event
def connect_error():
    print('Connection failed')

@sio.event
def disconnect():
    print('Disconnected from server')

# Define una función para manejar la respuesta de 'mqtt_message'
@sio.on('upd_act_state_resp')
def handle_respuesta(response):
    print(response)

@sio.on('upd_act_state')
def handle_upd_act_state(data):
    sio.emit('upd_act_state', data)

# Conectarse al servidor de Socket.IO
sio.connect(server_url)

# Mantener el programa en funcionamiento
sio.wait()