import socket
import threading
import sys

publishers = []
subscribers = []


def broadcast(message, sender_conn):
    for client in subscribers[:]:  # Use a copy to avoid issues during iteration
        if client != sender_conn:
            try:
                client.sendall(b"[Mod]: " + message)
            except:
                subscribers.remove(client)


def handle_client(conn, addr):
    try:
        client_type = conn.recv(1024).decode().strip().lower()

        if client_type == 'publisher':
            publishers.append(conn)
            print(f"Mod {addr} joined the server")
            conn.sendall(b"[Bot]: Welcome Mod! You're live in #announcements.")
        elif client_type == 'subscriber':
            subscribers.append(conn)
            print(f"[Bot]: {addr} joined the server")
            conn.sendall(b"[Bot]: You're now tuned in to #announcements.")
        else:
            print(f"Unknown client type from {addr}: {client_type}")
            conn.sendall(b"[Bot]: Invalid role. Kicked from server.")
            conn.close()
            return

        while True:
            message = conn.recv(1024)
            if not message:
                break
            print(f"[Mod {addr}]: {message.decode()}")
            if conn in publishers:
                broadcast(message, conn)
                conn.sendall(b"Ok")

    except Exception as e:
        print(f"{addr} cannot be reached: {e}")

    finally:
        print(f"Kicked {addr}")
        if conn in publishers:
            publishers.remove(conn)
        if conn in subscribers:
            subscribers.remove(conn)
        conn.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 server.py <port>")
        sys.exit(1)

    print("Discord in disguise!")

    host = socket.gethostname()
    port = int(sys.argv[1])

    s = socket.socket()
    s.bind((host, port))
    s.listen()
    print(f"Server is live on {port}. Type 'yeet' to rage-quit the server.")
    print("Waiting for someone to join...")

    threading.Thread(target=admin_commands, daemon=True).start()

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


def admin_commands():
    while True:
        cmd = input()
        if cmd.lower() == 'yeet':
            for client in publishers + subscribers:
                try:
                    client.sendall(b"[Bot]: Server maintenance initiated. All users have been kicked.")
                    client.close()
                except Exception as e:
                    print(f"Persistent User. Couldn't kick {client}.\n{e}")
                    pass
            print("You shut down the server. No one knows. Drama!")
            sys.exit(0)


if __name__ == "__main__":
    main()
