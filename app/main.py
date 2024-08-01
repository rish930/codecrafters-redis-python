# Uncomment this to pass the first stage
import socket
import threading

def respond_to_ping(server_socket: socket.socket):
    client, addr = server_socket.accept()
    while data:=client.recv(1024):
        client.send(b"+PONG\r\n")

def main():
    concurrent_clients = 2
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    threads = []
    for i in range(concurrent_clients):
        t = threading.Thread(target=respond_to_ping, kwargs={"server_socket":server_socket})
        print(f"starting thread {i}")
        t.start()
    

if __name__ == "__main__":
    main()
