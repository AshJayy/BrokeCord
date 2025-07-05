import socket
import sys
import threading


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Disconnected from server.")
                sys.exit(0)
            print(data.decode())
        except Exception as e:
            print(f"Disconnected from server. {e}")
            sys.exit(0)


def publisher(sock):
    while True:
        message = input("You: ")
        if message.lower() == 'peace out':
            print("You left the server.")
            break
        try:
            sock.sendall(message.encode())
            res = sock.recv(1024)
            if not res:
                print("Disconnected from server.")
                sys.exit(0)
            if res != b"Ok":
                print(f"res: {res}")
                print("Failed to send message.")
        except Exception as e:
            print(e)
            break


def subscriber(sock):
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    try:
        while True:
            user_input = input()
            if user_input.lower() == 'peace out':
                print("Exiting the server. Bye!")
                break
    except KeyboardInterrupt:
        print("You rage-quit. Shame.")


def negotiate_client_type(sock, type):
    sock.sendall(type.encode())
    res = sock.recv(1024)
    print(res.decode())


def client():
    if len(sys.argv) < 3:
        print("Usage: python3 client.py <port> <PUBLISHER/SUBSCRIBER>")
        sys.exit(1)

    print("Discord in disguise. Welcome to the server!")

    host = socket.gethostname()
    port = int(sys.argv[1])
    client_type = sys.argv[2].lower()

    try:
        sock = socket.socket()
        sock.connect((host, port))
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    negotiate_client_type(sock, client_type)

    if client_type == 'publisher':
        publisher(sock)
    elif client_type == 'subscriber':
        subscriber(sock)
    else:
        print("Invalid client type. Use 'PUBLISHER' or 'SUBSCRIBER'.")
    sock.close()


if __name__ == "__main__":
    client()
