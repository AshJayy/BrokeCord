import socket
import threading
import sys
from config import formatting

TOPICS = ["announcements", "general", "help"]
publishers = {topic: [] for topic in TOPICS}
subscribers = {topic: [] for topic in TOPICS}


def broadcast(message, sender_conn, sender_addr):
    """Send a message from a publisher to all subscribers of the same topic."""
    topic = next((t for t, clients in publishers.items() if sender_conn in clients), None)
    print(f"[Mod {sender_addr} in {topic}]: {message.decode()}")
    if not topic:
        print(f"{formatting['YELLOW']}Mod has not joined any servers.{formatting['RESET']}")
        return
    for client in subscribers[topic][:]:
        try:
            client.sendall(b"[Mod]: " + message)
        except Exception as e:
            print(f"{formatting['RED']}{e}{formatting['RESET']}", flush=True)
            subscribers[topic].remove(client)


def handle_client(conn, addr):
    """Handle communication with a connected client."""
    try:
        register_client(conn, addr)
        while True:
            try:
                message = conn.recv(1024)
                if not message:
                    break
                broadcast(message, conn, addr)
                conn.sendall(b"Ok")
            except OSError:
                break
    except Exception as e:
        print(f"{formatting['YELLOW']}{addr} cannot be reached: {e}{formatting['RESET']}", flush=True)
    finally:
        print(f"{formatting['YELLOW']}{addr} left the chat.{formatting['RESET']}", flush=True)
        for topic in TOPICS:
            publishers[topic] = [c for c in publishers[topic] if c != conn]
            subscribers[topic] = [c for c in subscribers[topic] if c != conn]
        try:
            conn.close()
        except Exception as e:
            print(f"{formatting['RED']}{e}{formatting['RESET']}")


def register_client(conn, addr):
    """Register a client as publisher or subscriber for a topic."""
    client_type = conn.recv(1024).decode().strip().lower()
    topic = get_client_topic(conn)
    if topic not in TOPICS:
        conn.sendall(b"[Bot]: Invalid channel. Kicked from server.")
        conn.close()
        return

    if client_type == 'publisher':
        publishers[topic].append(conn)
        print(f"Mod {addr} joined the server on channel #{topic}")
        conn.sendall(b"[Bot]: Welcome Mod! You're live in #" + topic.encode())
    elif client_type == 'subscriber':
        subscribers[topic].append(conn)
        print(f"User {addr} joined the server on channel #{topic}")
        conn.sendall(b"[Bot]: You're now tuned in to #" + topic.encode())
    else:
        print(f"{formatting['YELLOW']}Unknown client type from {addr}: {client_type}{formatting['RESET']}")
        conn.sendall(b"[Bot]: Invalid role. Kicked from server.")
        conn.close()


def get_client_topic(conn):
    """Prompt the client to select a topic and return it."""
    prompt = "[Bot]: Welcome to the server! Choose a channel to join.\n#" + "\n#".join(TOPICS)
    conn.sendall(prompt.encode())
    topic = conn.recv(1024).decode().strip().lower()
    return topic[1:] if topic.startswith('#') else topic


def setup_server():
    """Initialize and return the server socket."""
    host = socket.gethostname()
    if len(sys.argv) < 2:
        print(f"{formatting['YELLOW']}Usage: python3 server.py <port>{formatting['RESET']}")
        sys.exit(1)
    port = int(sys.argv[1])
    s = socket.socket()
    s.bind((host, port))
    s.listen()
    print(f"{formatting['GREEN']}Server is live on {port}. Type 'yeet' to rage-quit the server.{formatting['RESET']}")
    print("Waiting for someone to join...")
    return s


def admin_commands(server_socket):
    """Listen for admin commands (e.g., shutdown)."""
    while True:
        cmd = input()
        if cmd.lower() == 'yeet':
            for topic in TOPICS:
                for client in publishers[topic] + subscribers[topic]:
                    try:
                        client.sendall(b"[Bot]: Server maintenance initiated. All users have been kicked.")
                        client.close()
                    except Exception as e:
                        print(f"{formatting['YELLOW']}Persistent User. Couldn't kick {client}.\n{e}{formatting['RESET']}", flush=True)
            print(f"{formatting['RED']}You shut down the server. No one knows. Drama!{formatting['RESET']}")
            server_socket.close()
            sys.exit(0)


def main():
    print(f"{formatting['CYAN']}{formatting['BOLD']}Discord is down! We made our own chat server.{formatting['RESET']}")
    server_socket = setup_server()
    threading.Thread(target=admin_commands, args=(server_socket,), daemon=True).start()
    while True:
        try:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except OSError:
            break


if __name__ == "__main__":
    main()
