import socket
import struct
import os

TCP_IP = "127.0.0.1"
TCP_PORT = 1452
BUFFER_SIZE = 8192  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Server started, waiting for connections...")

while True:
    conn, addr = s.accept()
    print("Connection established with:", addr)
    
    while True:
        # Receive command from client
        cmd = conn.recv(4).decode()
        if not cmd:
            break

        if cmd == "UPLD":
            try:
                # Receive filename and size
                filename_size = struct.unpack("h", conn.recv(2))[0]
                filename = conn.recv(filename_size).decode()
                file_size = struct.unpack("i", conn.recv(4))[0]
                
                # Prepare to receive file
                with open(filename, "wb") as f:
                    bytes_received = 0
                    while bytes_received < file_size:
                        data = conn.recv(min(BUFFER_SIZE, file_size - bytes_received))
                        if not data:
                            break
                        f.write(data)
                        bytes_received += len(data)
                conn.sendall(struct.pack("f", 0.0)) 
                conn.sendall(struct.pack("i", file_size))
                print(f"Uploaded file: {filename}")
            except Exception as e:
                print("Upload error:", e)

        elif cmd == "LIST":
            try:
                files = os.listdir(".")
                conn.sendall(struct.pack("i", len(files)))
                total_size = 0
                for filename in files:
                    file_size = os.path.getsize(filename)
                    total_size += file_size
                    conn.sendall(struct.pack("i", len(filename)) + filename.encode())
                    conn.sendall(struct.pack("i", file_size))
                    conn.recv(1) 
                conn.sendall(struct.pack("i", total_size))
                print("Sent file list to client")
            except Exception as e:
                print("List error:", e)

        elif cmd == "DWLD":
            try:
                filename_size = struct.unpack("h", conn.recv(2))[0]
                filename = conn.recv(filename_size).decode()
                if os.path.isfile(filename):
                    conn.sendall(struct.pack("i", os.path.getsize(filename)))
                    with open(filename, "rb") as f:
                        data = f.read(BUFFER_SIZE)
                        while data:
                            conn.sendall(data)
                            data = f.read(BUFFER_SIZE)
                    conn.sendall(struct.pack("f", 0.0)) 
                else:
                    conn.sendall(struct.pack("i", -1)) 
                print(f"Downloaded file: {filename}")
            except Exception as e:
                print("Download error:", e)

        elif cmd == "DELF":
            try:
                filename_size = struct.unpack("h", conn.recv(2))[0]
                filename = conn.recv(filename_size).decode()
                if os.path.isfile(filename):
                    os.remove(filename)
                    conn.sendall(struct.pack("i", 1))  
                else:
                    conn.sendall(struct.pack("i", -1))  
                print(f"Deleted file: {filename}")
            except Exception as e:
                print("Delete error:", e)

        elif cmd == "QUIT":
            conn.close()
            print("Client disconnected")
            break
