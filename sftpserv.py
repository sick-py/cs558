import socket
import ssl
import os
from datetime import datetime

def handle_client(connection, client_address):
    try:
        print(f"Connection from {client_address}")
        while True:
            data = connection.recv(1024).decode()
            if data:
                command, *args = data.split()
                if command == "get":
                    filename = args[0]
                    try:
                        with open(f"server/{filename}", "r") as file:
                            file_content = file.read()
                            connection.sendall(file_content.encode())
                            print(f"Transferred {len(file_content)} characters")
                    except FileNotFoundError:
                        error_message = "The file does not exist"
                        connection.sendall(error_message.encode())
                elif command == "exit":
                    print("Exit command received")
                    break
            else:
                break
    finally:
        connection.close()

def start_server(server_port):
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', server_port))
        sock.listen(1)
        print(f"SFTP Server listening on port {server_port}")
        while True:
            connection, client_address = sock.accept()
            with context.wrap_socket(connection, server_side=True) as secure_conn:
                handle_client(secure_conn, client_address)

if __name__ == "__main__":
    start_server(3479)  # Change this to use a different port
