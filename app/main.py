# Uncomment this to pass the first stage
import socket
import threading

def respond_to_ping(connection: socket.socket, id: int):
    with connection:
        while data:=connection.recv(1024):
            print(f"Responding for connection no. {id}")
            connection.send(b"+PONG\r\n")
    print(f"Closed conn no. {id}")

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    conn_count = 1
    while True:
        print(f"Connection no. {conn_count}")
        connection, address = server_socket.accept()
        t = threading.Thread(target=respond_to_ping, args=(connection,conn_count))
        t.start()
        conn_count+=1
    

if __name__ == "__main__":
    main()
