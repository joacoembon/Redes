import socket
import sys

if len(sys.argv) != 3:
    print("Te olvidaste IP y puerto master")
    exit(1)

host = sys.argv[1]
port = int(sys.argv[2])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Opción para reutilizar puerto
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((host, port))
print(f"Server UDP escuchando en puerto {port}.")

while True:
    data, addr = server_socket.recvfrom(1024)

    server_socket.connect(addr)

    if not data or data.decode() == "FIN\n":
        break

    print(f"Recibo desde {addr}: {data.decode()}")

    server_socket.sendto(b"Mensaje recibido :D\n", addr)

server_socket.close()
