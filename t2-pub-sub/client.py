import socket
import sys
import threading


def receive_messages(sock):
    """Listen for messages from the server in a background thread."""
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


def handle_exit(sock, message):
    """Cleanly exit the client."""
    print(message)
    try:
        sock.close()
    except Exception:
        pass
    sys.exit(0)


def publisher(sock):
    """Publisher: send messages to the server."""
    while True:
        message = input("You: ")
        if message.lower() == 'peace out':
            handle_exit(sock, "You left the server.")
        try:
            sock.sendall(message.encode())
            res = sock.recv(1024)
            if not res:
                handle_exit(sock, "Disconnected from server.")
            if res != b"Ok":
                print(f"Failed to send message. Server response: {res.decode()}")
        except Exception as e:
            print(f"Error: {e}")
            break


def subscriber(sock):
    """Subscriber: receive messages from the server."""
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    try:
        while True:
            user_input = input()
            if user_input.lower() == 'peace out':
                handle_exit(sock, "Exiting the server. Bye!")
    except KeyboardInterrupt:
        handle_exit(sock, "You rage-quit. Shame.")


def negotiate_client_type(sock, client_type):
    """Negotiate client type with the server."""
    sock.sendall(client_type.encode())
    res = sock.recv(1024)
    print(res.decode())


def main():
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
    main()
