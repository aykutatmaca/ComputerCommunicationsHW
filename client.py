import hashlib
import socket

### Aykut Atmaca 150170008, Computer Communications Project 1, Socked Programming Assignment
### client.py

HOST = "127.0.0.1"
PORT = 7070
privateString = "comComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomCom".encode("utf-8")

print("\n------- CLIENT PROCESS START")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.sendall("Start_Connection".encode("utf-8"))
    data = sock.recv(1024).decode("utf-8").encode("utf-8")
    hash = hashlib.sha1(data + privateString).hexdigest().encode("utf-8")
    sock.sendall(hash)
    data = sock.recv(1024).decode("utf-8")
    print(data)
    sock.sendall(input().encode("utf-8"))

