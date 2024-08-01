# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    with socket.create_server(("localhost", 6379), reuse_port=True) as server_socket:
        client, addr = server_socket.accept() # wait for client
        while data:=client.recv(1024):
            # print("data:",data.decode())
            client.send(b"+PONG\r\n")

if __name__ == "__main__":
    main()
