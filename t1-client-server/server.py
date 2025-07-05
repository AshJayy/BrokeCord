import socket
import time
import sys


def server():
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)
    host = socket.gethostname()
    port = int(sys.argv[1])

    s = socket.socket()
    s.bind((host, port))
    print("Server online. Type 'yeet' to rage-quit the chat.")
    print("Waiting for someone to show up...")

    s.listen(1)
    conn, addr = s.accept()
    print(f"{addr} entered the chat")
    while True:
        data = conn.recv(1024)
        if not data:
            print(f"{addr} last seen at {time.strftime('%H:%M:%S')}")
            break
        print(f"Client says: {data.decode()}")
        res = input("You: ")
        if res.lower() == "yeet":
            print("You left the chat. Drama!")
            break
        conn.send(res.encode())
    conn.close()


if __name__ == "__main__":
    server()
