# Uncomment this to pass the first stage
import socket
import threading
from .parser import RedisParser
from .storage import RedisStorage

redis_storage = RedisStorage()

def generate_response(data: bytes):
    print(f"Data recieved:{data}")
    parser = RedisParser()
    arr, _ = parser.parse(data)
    command: str = arr[0].decode().lower()
    if command == "ping":
        return "+PONG\r\n".encode()
    elif command == "echo":
        bulk_str = arr[1].decode()
        response = f"${len(bulk_str)}\r\n{bulk_str}\r\n"
        response = response.encode()
        print("Response:", repr(response))
        return response
    elif command == "set":
         key = arr[1].decode()
         if len(arr)>2:
            val = arr[2].decode()
            redis_storage.add(key, val)
         return "+OK\r\n".encode()
    elif command == "get":
        key = arr[1].decode()
        val = redis_storage.get(key)
        if val:
            response = f"${len(val)}\r\n{val}\r\n"
            return response.encode()
        else:
            return "$-1\r\n".encode()
        
    else:
        return "_\r\n".encode()
    
def respond(connection: socket.socket, id: int):
    with connection:
        while data:=connection.recv(1024):
            print(f"Responding for connection no. {id}")
            response = generate_response(data)
            connection.send(response)
    print(f"Closed conn no. {id}")

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    conn_count = 1
    while True:
        print(f"Connection no. {conn_count}")
        connection, address = server_socket.accept()
        t = threading.Thread(target=respond, args=(connection,conn_count))
        t.start()
        conn_count+=1
        print("Storage:", redis_storage.get_storage())
    

if __name__ == "__main__":
    main()
