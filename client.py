import socket
import threading

class ChatClient:
    def __init__(self, host='127.0.0.1', port=55556):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        self.sock.connect((self.host, self.port))
        threading.Thread(target=self.handle_server).start()
        while True:
            message = input()
            if message.lower() == 'quit':
                break
            self.sock.sendall(message.encode())
            
    def handle_server(self):
        while True:
            data = self.sock.recv(1024).decode()
            if not data:
                break
            print(f"Received message: {data}")
            
if __name__ == '__main__':
    client = ChatClient()
    client.connect()
