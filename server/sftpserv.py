import socket
import ssl
import os
from datetime import datetime
import sys

# Global flag to control the server's main loop
should_server_run = True

def handle_client(connection, client_address, server_socket):
    global should_server_run
    try:
        print(f"Connection from {client_address}")
        while True:
            data = connection.recv(1024).decode()
            if data:
                command, *args = data.split()
                if command == "get":
                    filename = args[0]
                    try:
                        with open(f"../server/{filename}", "r") as file:
                            file_content = file.read()
                            connection.sendall(file_content.encode())
                            print(f"Transferred {len(file_content)} characters")
                    except FileNotFoundError:
                        error_message = "The file does not exist"
                        connection.sendall(error_message.encode())
                elif command == "exit":
                    print("Exit command received")
                    should_server_run = False  # Signal the server to stop after this client disconnects
                    break
            else:
                break
    finally:
        connection.close()
        if not should_server_run:
            server_socket.close()  # Close the server socket if we're shutting down

def start_server(server_port):
    global should_server_run
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="../cert.pem", keyfile="../key.pem")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('0.0.0.0', server_port))
        sock.listen(1)
        print(f"SFTP Server listening on port {server_port}")
        while should_server_run:
            try:
                connection, client_address = sock.accept()
            except socket.error:
                print("Server socket closed, shutting down server.")
                break  # Exit the loop if the socket is closed
            with context.wrap_socket(connection, server_side=True) as secure_conn:
                handle_client(secure_conn, client_address, sock)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 sftpserv.py <server_port>")
        sys.exit(1)
    server_port = int(sys.argv[1])
    start_server(server_port)
