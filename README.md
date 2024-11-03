**FTP File Transfer Project**


This project is a simple implementation of an FTP-like file transfer system using Python sockets. It enables file upload, download, listing, and deletion between a client and server over a TCP connection. The server listens for incoming connections and handles commands from the client, while the client can connect to the server, send files, retrieve files, and manage files on the server.

## Table of Contents
1. [Features](#features)
2. [Requirements](#requirements)
3. [Setup Instructions](#setup-instructions)
4. [Usage](#usage)
5. [Commands](#commands)
6. [Optimizations](#optimizations)
7. [Limitations](#limitations)

---

## Features

- **File Upload**: Uploads files from the client to the server.
- **File Download**: Downloads files from the server to the client.
- **List Files**: Lists all files stored on the server, including their sizes.
- **File Deletion**: Deletes files from the server.
- **Quit Command**: Disconnects the client from the server gracefully.

## Requirements

- Python 3.x
- Basic knowledge of Python socket programming
- Local or remote server with network connectivity for running the server and client scripts.

## Setup Instructions

1. **Clone the Repository**: Download or clone this repository to your local machine.
2. **Run the Server**:
   - Navigate to the directory containing `server.py`.
   - Run the server script with the command:
     ```bash
     python server.py
     ```
   - The server will start and listen for incoming connections on `127.0.0.1` (localhost) on port `1452`.
3. **Run the Client**:
   - In a separate terminal, navigate to the directory containing `client.py`.
   - Run the client script with the command:
     ```bash
     python client.py
     ```
   - The client is now ready to connect to the server and interact with it.

## Usage

Once the server is running and the client has connected, you can use the following commands in the client terminal to interact with the server:

### Commands

- **Connect to the Server**:
  - **Command**: `CONN`
  - **Description**: Establishes a connection with the server. Run this command first before executing any other commands.
  
- **Upload a File to the Server**:
  - **Command**: `UPLD <filename>`
  - **Example**: `UPLD example.txt`
  - **Description**: Uploads the specified file from the client to the server. Ensure the file exists in the client’s directory.

- **List Files on the Server**:
  - **Command**: `LIST`
  - **Description**: Lists all files on the server, showing each file's name and size. After listing, the total directory size on the server is displayed.

- **Download a File from the Server**:
  - **Command**: `DWLD <filename>`
  - **Example**: `DWLD example.txt`
  - **Description**: Downloads the specified file from the server to the client. The file is saved in the client’s directory with the same name.

- **Delete a File on the Server**:
  - **Command**: `DELF <filename>`
  - **Example**: `DELF example.txt`
  - **Description**: Deletes the specified file from the server. Use with caution, as this action is irreversible.

- **Quit**:
  - **Command**: `QUIT`
  - **Description**: Disconnects from the server and closes the client program.

### Example Usage

```plaintext
> CONN
Connection successful

> UPLD file.txt
Uploaded file: file.txt

> LIST
example1.txt - 1024 bytes
example2.jpg - 2048 bytes
Total directory size: 3072 bytes

> DWLD example1.txt
Downloaded file: example1.txt

> DELF example2.jpg
Deleted file: example2.jpg

> QUIT
Disconnected from server
