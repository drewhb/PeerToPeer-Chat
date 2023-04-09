import socket
import threading
from pymongo import MongoClient
import datetime


class ChatServer:
    def __init__(self, host='127.0.0.1', port=55556):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connections = []
        self.client = MongoClient('mongodb+srv://dbrownback:YvIb4SXV7EUfQWwN@document-analyzer-db-14.dnewmyi.mongodb.net/?retryWrites=true&w=majority')
        self.db = self.client["P2P-Chat"]

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Chat server started on {self.host}:{self.port}")
        while True:
            conn, addr = self.sock.accept()
            self.connections.append(conn)
            print(f"Connected to {addr}")
            threading.Thread(target=self.handle_client, args=(conn,)).start()
            
    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                messagesDB = self.db['Messages']

                message_object = {
                        'IPAddress' : self.host,   
                        'Time-Stamp' : datetime.datetime.now(), 
                        'Contents': data
                    }
                                
                print(f"Received message: {data}")
                
                messagesDB.insert_one(message_object);

                self.broadcast(data, conn)
            except:
                break
        self.connections.remove(conn)
        conn.close()
        
    def broadcast(self, message, sender_conn):
        for conn in self.connections:
            if conn != sender_conn:
                try:
                    conn.sendall(message.encode())
                except:
                    self.connections.remove(conn)
                    conn.close()
                    
if __name__ == '__main__':

    server = ChatServer()
    server.start()
