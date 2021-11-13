import hashlib
from math import fabs
import socket
import threading

### Aykut Atmaca 150170008, Computer Communications Project 1, Socked Programming Assignment
### client.py

HOST = "127.0.0.1"
PORT = 7070
privateString = "comComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomCom".encode("utf-8")
exit_event = threading.Event()
gameRunning = 0

def getDataFromServer():
    while(True):
        if exit_event.is_set():
            exit_event.clear()
            return
        data = sock.recv(1024)
        if(data):
            parseDataFromServer(data)


def parseDataFromServer(data):
    global gameRunning
    type = int.from_bytes(bytes(data[0:1]), "big", signed=False)
    if type == 0:
        gameRunning = True
        stringToPrint = str(bytes(data[1:]), "utf-8")
    elif type == 1:
        stringToPrint = "TIME REMAINING: " + str(int.from_bytes(bytes(data[1:3]), "big", signed=False)) + " SECONDS"
    elif type == 2:
        gameRunning = False
        stringToPrint = "GAME OVER! SCORE: " + str(int.from_bytes(bytes(data[1:3]), "big", signed=True))
    print(stringToPrint)

print("\n------- CLIENT PROCESS START")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.sendall("Start_Connection".encode("utf-8"))
    data = sock.recv(1024).decode("utf-8").encode("utf-8")
    hash = hashlib.sha1(data + privateString).hexdigest().encode("utf-8")
    sock.sendall(hash)
    data = sock.recv(1024).decode("utf-8")
    sock.sendall(input().encode("utf-8"))

    thread = threading.Thread(target=getDataFromServer)
    thread.start()
    while(True):
        userInput = input()
        if gameRunning:
            bytesToSend = int(3).to_bytes(1,"big", signed=False) + userInput.encode("utf-8")
            print(bytesToSend)
            sock.sendall(bytesToSend)
        else:    
            if(userInput == "0" or userInput == "1" or userInput == "2"):
                bytesToSend = int(userInput).to_bytes(1,"big", signed=False)
                sock.sendall(bytesToSend)
    


