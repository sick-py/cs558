import socket
import ssl
from datetime import datetime

def sftp_client(server_domain, server_port):
    context = ssl.create_default_context()

    with socket.create_connection((server_domain, server_port)) as sock:
        with context.wrap_socket(sock, server_hostname=server_domain) as secure_sock:
            print("sftp >", end=' ')
            command = input()
            while command != "exit":
                if command.startswith("get"):
                    secure_sock.sendall(command.encode())
                    data = secure_sock.recv(1024).decode()
                    if data == "The file does not exist":
                        print(data)
                    else:
                        filename = command.split()[1]
                        with open(f"client/{filename}", "w") as file:
                            file.write(data)
                            print(f"Transferred {len(data)} characters")
                            print(f"File received at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print("Invalid Command")
                print("sftp >", end=' ')
                command = input()
            secure_sock.sendall(command.encode())

if __name__ == "__main__":
    sftp_client("remote06.cs.binghamton.edu", 1968)  
