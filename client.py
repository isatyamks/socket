import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the isatyamks_socket server!")

@sio.event
def message(data):
    print(data)

@sio.event
def disconnect():
    print("Disconnected from the chat server.")

@sio.event
def error(data):
    print("Error:", data.get("msg", "Unknown error"))

def main():
    server_url = "https://socket-dsff.onrender.com"
    sio.connect(server_url)
    name = input("Enter your Username: ")
    sio.emit('join', name)
    
    try:
        while True:
            msg = input(f"{name}: ")
            if msg.lower() == 'exit':
                break
            sio.send(msg)
    except KeyboardInterrupt:
        pass
    finally:
        sio.disconnect()

if __name__ == "__main__":
    main()
