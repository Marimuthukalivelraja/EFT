import socket
import struct
import sys
import os


TCP_IP = "127.0.0.1"
TCP_PORT = 1452
BUFFER_SIZE = 8192 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10) 

def conn():
    try:
        s.connect((TCP_IP, TCP_PORT))
        print("Connection successful")
    except socket.error as e:
        print("Connection failed:", e)

def upld(file_name):
    try:
        with open(file_name, "rb") as f:
            s.sendall("UPLD".encode())
            s.sendall(struct.pack("h", len(file_name)) + file_name.encode())
            s.sendall(struct.pack("i", os.path.getsize(file_name)))
            data = f.read(BUFFER_SIZE)
            while data:
                s.sendall(data)
                data = f.read(BUFFER_SIZE)
        print(f"Uploaded file: {file_name}")
    except Exception as e:
        print("Upload error:", e)

def list_files():
    try:
        s.sendall("LIST".encode())
        num_files = struct.unpack("i", s.recv(4))[0]
        for _ in range(num_files):
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size).decode()
            file_size = struct.unpack("i", s.recv(4))[0]
            print(f"{file_name} - {file_size} bytes")
            s.sendall(b"1")
        total_size = struct.unpack("i", s.recv(4))[0]
        print(f"Total directory size: {total_size} bytes")
    except Exception as e:
        print("List error:", e)

def dwld(file_name):
    try:
        s.sendall("DWLD".encode())
        s.sendall(struct.pack("h", len(file_name)) + file_name.encode())
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            print("File not found on server.")
            return
        with open(file_name, "wb") as f:
            bytes_received = 0
            while bytes_received < file_size:
                data = s.recv(min(BUFFER_SIZE, file_size - bytes_received))
                if not data:
                    break
                f.write(data)
                bytes_received += len(data)
        print(f"Downloaded file: {file_name}")
    except Exception as e:
        print("Download error:", e)

def delf(file_name):
    try:
        s.sendall("DELF".encode())
        s.sendall(struct.pack("h", len(file_name)) + file_name.encode())
        file_exists = struct.unpack("i", s.recv(4))[0]
        if file_exists == 1:
            print(f"Deleted file: {file_name}")
        else:
            print("File not found on server.")
    except Exception as e:
        print("Delete error:", e)

def quit():
    s.sendall("QUIT".encode())
    s.close()
    print("Disconnected from server")


print("FTP Client: Connect with CONN, upload with UPLD, list files with LIST, download with DWLD, delete with DELF, quit with QUIT")

while True:
    cmd = input("\nEnter command: ").strip().split()
    if cmd[0].upper() == "CONN":
        conn()
    elif cmd[0].upper() == "UPLD" and len(cmd) > 1:
        upld(cmd[1])
    elif cmd[0].upper() == "LIST":
        list_files()
    elif cmd[0].upper() == "DWLD" and len(cmd) > 1:
        dwld(cmd[1])
    elif cmd[0].upper() == "DELF" and len(cmd) > 1:
        delf(cmd[1])
    elif cmd[0].upper() == "QUIT":
        quit()
        break
    else:
        print("Invalid command")
