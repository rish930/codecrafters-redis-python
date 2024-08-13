import socket
import threading
from .parser import RedisParser
from .storage import RedisStorage
from .redisValueObj import RedisValueObj

redis_storage = RedisStorage()

def handle_ping():
    return "+PONG\r\n".encode()

def handle_echo(arr):
    bulk_str = arr[1]
    response = f"${len(bulk_str)}\r\n{bulk_str}\r\n"
    response = response.encode()
    return response

def handle_set(arr):
    key = arr[1]
    if len(arr)>2:
        val = arr[2]
        rdo = redis_storage.add(key, val)
        if len(arr)>3:
            command2 = arr[3]
            if command2.lower()=="px":
                rdo.set_expiry_after(int(arr[4]))
    return "+OK\r\n".encode()

def handle_get(arr):
    key = arr[1]
    val_obj: RedisValueObj = redis_storage.get(key)
    if val_obj and not val_obj.is_expired():
        val = val_obj.get_value()
        response = f"${len(val)}\r\n{val}\r\n"
        return response.encode()
    else:
        return "$-1\r\n".encode()

def generate_response(data: bytes):
    print(f"Data recieved:{data}")
    parser = RedisParser()
    arr, _ = parser.parse(data.decode())
    command: str = arr[0].lower()
    
    if command == "ping":
        response = handle_ping()
    elif command == "echo":
        response = handle_echo(arr)
    elif command == "set": # TODO add thread safety
        response = handle_set(arr)
    elif command == "get":
        response = handle_get(arr)
    else:
        response = "_\r\n".encode()
    
    print("Response:", repr(response))
    return response
    
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
