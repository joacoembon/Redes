import socket
from threading import Thread, Event
import signal
import sys

clients = []
threads = []
server_socket = None
stop_event = Event()  # Flag to notify threads to stop

def handle_client(connection, addr):
    print(f"Nueva conexión desde {addr}")
    try:
        connection.settimeout(1.0)  # check stop_event periodically
        while not stop_event.is_set():
            try:
                data = connection.recv(1000)
                if not data:
                    break
                text = data.decode().strip()
                print(f"[{addr}] {text}")
                if text.lower() == "quit":
                    break
            except socket.timeout:
                continue
            except ConnectionResetError:
                break
    finally:
        print(f"Conexión {addr} terminada")
        connection.close()
        if connection in clients:
            clients.remove(connection)

def signal_handler():
    print("\nCerrando sockets y threads...")
    stop_event.set()  # notify threads to stop

    for t in threads:
        t.join()

    for c in clients:
        try:
            c.close()
        except:
            pass

    if server_socket:
        try:
            server_socket.close()
        except:
            pass

    sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print("Te olvidaste IP o puerto master")
        exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    global server_socket

    signal.signal(signal.SIGINT, signal_handler)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    server_socket.settimeout(1.0) # Para verificar el stop_event

    print(f"Server escuchando en {host}:{port}")

    while not stop_event.is_set():
        try:
            connection, address = server_socket.accept()
            clients.append(connection)
            t = Thread(target=handle_client, args=(connection, address))
            threads.append(t)
            t.start()
        except socket.timeout:
            continue

if __name__ == "__main__":
    main()
