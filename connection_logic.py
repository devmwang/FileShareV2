import socket
import tqdm
import time
import os
import sys

# Default settings for websockets and such
separator = '<SEPARATOR>'
buffer_size = 4096

# Allow user to pick either send or receive
side = input("""[s]end or [r]eceive?
""")

if side.lower() == 's' or side.lower() == 'send':
    # Gets the user to input a filepath and attempts to parse it, if fails, exit
    filepath = input("""Input path to file:
""")
    filesize = 0
    try:
        filesize = os.path.getsize(filepath)
    except FileNotFoundError:
        print("The program cannot find the file specified.")
        time.sleep(5)
        sys.exit()

    # IPs and ports
    host = input("Sending to IP: ")
    port = int(input("Sending to TCP port: "))

    # Websocket connection handlers
    s = socket.socket()
    print(f"Connecting to {host} on TCP port {port}")
    s.connect((host, port))
    print(f"Connected to {host} on TCP port {port}")

    # Send file
    s.send(f"{filepath}{separator}{filesize}".encode())
    progress = tqdm.tqdm(range(filesize), f"Sending {filepath}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filepath, "rb") as f:
        for _ in progress:
            bytes_read = f.read(buffer_size)
            if not bytes_read:
                break
            s.sendall(bytes_read)
            progress.update(len(bytes_read))
    s.close()

if side.lower() == 'r' or side.lower() == 'receive':
    host = "0.0.0.0"
    port = int(input("Receving on TCP port: "))

    # Websocket connection
    s = socket.socket()
    s.bind((host, port))
    s.listen(2)
    print(f"Listening as {host} on TCP port {port}")
    client_socket, address = s.accept()
    print(f"{address} connected on TCP port {port}")

    # Receving files
    received = client_socket.recv(buffer_size).decode()
    filepath, filesize = received.split(separator)
    filename = os.path.basename(filepath)
    filesize = int(filesize)

    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for _ in progress:
            bytes_read = client_socket.recv(buffer_size)
            if not bytes_read:
                break
            f.write(bytes_read)
            progress.update(len(bytes_read))

    client_socket.close()
    s.close()
