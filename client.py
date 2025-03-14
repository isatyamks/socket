import socketio

# Create a Socket.IO client instance
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the chat server!")

@sio.event
def message(data):
    print("Message received:", data)

@sio.event
def disconnect():
    print("Disconnected from the chat server.")

def main():
    server_url = "https://socket-dsff.onrender.com"
    sio.connect(server_url)
    
    try:
        name = input("Enter your Username: ")
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
