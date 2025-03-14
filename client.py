import socketio

sio = socketio.Client()
user_list = []
@sio.event
def connect():
    print("Connected to the chat server!")

@sio.event
def message(data):
    print(data)

@sio.event
def disconnect():
    print("Disconnected from the chat server.")

def main():
    server_url = "https://socket-dsff.onrender.com"  # Replace with your actual Render URL
    sio.connect(server_url)
    name = input("Enter your Username: ")
    if name not in user_list:
        user_list.append(name)
    else:
        print("This user_name already exit! ")
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
