import socket
import sys

def client():
    if len(sys.argv) < 2:
        print("Usage: python3 client.py <port>")
        sys.exit(1)
    host = socket.gethostname()
    port = int(sys.argv[1])

    s = socket.socket()
    s.connect((host, port))
    print("You have entered the chat. Type 'peace out' to leave.")

    while True:
        message = input("You: ")
        if message.lower() == 'peace out':
            print("You left the chat.")
            break
        s.send(message.encode())
        data = s.recv(1024)
        if not data:
            print("Server left you on read.")
            break
        print(f"Server says: {data.decode()}")
    s.close()

if __name__ == "__main__":
    client()