import os
import socket
import sys
import threading
from config import formatting

live = False


def receive_messages(sock):
    """Background thread: listens for messages from the server."""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print(f"{formatting['RED']}Disconnected from server.{formatting['RESET']}", flush=True)
                handle_exit(sock)

            print(data.decode())

            if b"Server maintenance initiated" in data:
                print(f"{formatting['RED']}Disconnected from server.{formatting['RESET']}", flush=True)
                os._exit(0)

        except KeyboardInterrupt:
            print(f"{formatting['YELLOW']}You rage-quit. Shame.{formatting['RESET']}", flush=True)
            handle_exit(sock)
            return

        except Exception as e:
            global live
            if live:
                print(f"{formatting['RED']}Disconnected from server. {e}{formatting['RESET']}", flush=True)
            handle_exit(sock)
            return


def handle_exit(sock):
    """Cleanly exit the client."""
    global live
    live = False

    print(f"{formatting['RED']}Exiting the server. Bye!{formatting['RESET']}")
    try:
        sock.close()
    except Exception as e:
        print(e, flush=True)
        pass
    os._exit(0)


def publisher(sock):
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    while True:
        message = input("You: ")
        if message.lower() == 'peace out':
            handle_exit(sock)
        try:
            sock.sendall(message.encode())
            res = sock.recv(1024)
            if not res or b"Server maintenance initiated" in res:
                print(res.decode(), flush=True)
                handle_exit(sock)
            if res != b"Ok":
                print(f"{formatting['YELLOW']}Failed to send message.{formatting['RESET']}", flush=True)
        except Exception as e:
            print(f"{formatting['RED']}{e}{formatting['RESET']}", flush=True)
            break


def subscriber(sock):
    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()
    try:
        while True:
            user_input = input()
            if user_input.lower() == 'peace out':
                handle_exit(sock)
    except KeyboardInterrupt:
        handle_exit(sock)


def parse_args():
    """Parse command-line arguments."""
    if len(sys.argv) < 3:
        print(f"{formatting['YELLOW']}Usage: python3 client.py <port> <PUBLISHER/SUBSCRIBER>{formatting['RESET']}")
        sys.exit(1)
    return int(sys.argv[1]), sys.argv[2].lower()


def connect_to_server(host, port):
    """Establish connection to the server."""
    try:
        sock = socket.socket()
        sock.connect((host, port))
        print(f"{formatting['GREEN']}Connected to server! Type 'peace out' to leave.{formatting['RESET']}", flush=True)
        return sock
    except Exception as e:
        print(f"{formatting['RED']}Connection failed: {e}", flush=True)
        sys.exit(1)


def negotiate_client_type(sock, client_type):
    """Send client type and handle server response."""
    sock.sendall(client_type.encode())
    if client_type not in ['publisher', 'subscriber']:
        print(f"{formatting['RED']}Invalid client type. Use 'PUBLISHER' or 'SUBSCRIBER'.{formatting['RESET']}")
        sock.close()
        sys.exit(1)


def select_topic(sock):
    """Prompt user to select a topic and send to server."""
    res = sock.recv(1024)
    if not res:
        print(f"{formatting['RED']}Disconnected from server.{formatting['RESET']}", flush=True)
        sys.exit(0)
    print(f"{formatting['CYAN']}{res.decode()}{formatting['RESET']}", flush=True)
    topic = input(">> ")
    sock.sendall(topic.encode())
    res = sock.recv(1024)
    print(res.decode())


def client():
    """Main client logic."""
    print(f"{formatting['CYAN']}=" * 60)
    print(f"{formatting['BOLD']}Welcome to BrokeCord — Because Discord went down.")
    print(f" No emojis. No stickers. No gifs. Just plain old text messages.{formatting['RESET']}")
    print("Connecting to our bootleg chat server...")
    print(f"{formatting['CYAN']}={formatting['RESET']}" * 60)

    port, client_type = parse_args()
    host = socket.gethostname()
    sock = connect_to_server(host, port)

    negotiate_client_type(sock, client_type)

    global live
    live = True

    select_topic(sock)

    if client_type == 'publisher':
        publisher(sock)
    elif client_type == 'subscriber':
        subscriber(sock)
    else:
        print(f"{formatting['YELLOW']}Invalid client type. Use 'PUBLISHER' or 'SUBSCRIBER'.{formatting['RESET']}")
    sock.close()


if __name__ == "__main__":
    client()
