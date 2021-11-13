import hashlib
from math import fabs
import socket
import random
import string
import threading
import time

### Aykut Atmaca 150170008, Computer Communications Project 1, Socked Programming Assigment
### server.py

HOST = "127.0.0.1"
PORT = 7070
privateString = "comComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomCom".encode("utf-8")

_PERIODFORSENDINGREMANINGTIME_ = 3
_TIMEFORGUESSING_ = 12
remainingTime = _TIMEFORGUESSING_
exit_event = threading.Event()
gameRunning = False
askedNumber = 0
playerScore = 0


def sendRemainingTimePeriodically():
    global playerScore
    global remainingTime
    remainingTime = _TIMEFORGUESSING_
    while(True):
        if exit_event.is_set():
            exit_event.clear()
            return
        if remainingTime <= 0:
            bytes = int(1).to_bytes(1, "big", signed=False) + int(0).to_bytes(2 ,"big", signed=False)
            connection.send(bytes)
            playerScore -= 1
            sendCurrentScore()
            exit_event.set()
        else:        
            bytes = int(1).to_bytes(1, "big", signed=False) + int(remainingTime).to_bytes(2 ,"big", signed=False)
            connection.send(bytes)

        for i in range(_PERIODFORSENDINGREMANINGTIME_):
            if exit_event.is_set():
                exit_event.clear()
                return
            time.sleep(1)
            remainingTime -= 1


def terminateGame():
    global gameRunning
    gameRunning = False
    exit_event.set()
    thread.join()
    exit()

def startGame():
    global gameRunning
    gameRunning = True
    askQuestion()
    
def sendRemainingTime():
    if gameRunning:
        bytesToSend = int(1).to_bytes(1, "big", signed=False) + int(remainingTime).to_bytes(2 ,"big", signed=False)
        connection.sendall(bytes(bytesToSend))

def guess(data):
    global playerScore
    if gameRunning and remainingTime > 0:
        exit_event.set()
        guess = str(data, "utf-8")
        if guess == "even":
            if askedNumber % 2 == 0:
                playerScore += 1
            else:
                playerScore -= 1
        elif guess == "odd":
            if askedNumber % 2 == 1:
                playerScore += 1
            else:
                playerScore -= 1
        else:
            guess = int(guess)
            if guess == askedNumber:
                playerScore += 35
            else:
                playerScore -= 1
        sendCurrentScore()

def askQuestion():
    global askedNumber
    askedNumber = random.randint(0,36)
    print(askedNumber)
    stringToSend = "What is your guess? Number, even, odd?".encode("utf-8")
    bytesToSend = int(0).to_bytes(1, "big", signed=False) + stringToSend
    connection.sendall(bytesToSend)
    thread = threading.Thread(target=sendRemainingTimePeriodically)
    thread.start()

def sendCurrentScore():
    bytesToSend = int(2).to_bytes(1, "big", signed=False) + int(playerScore).to_bytes(2 ,"big", signed=True)
    connection.sendall(bytesToSend)


print("\n------- SERVER PROCESS START")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    connection, address = sock.accept()
    with connection:
        print("------- CONNECTION SUCCESSFULL, ADDRESS:", address)
    
        data = connection.recv(1024).decode("utf-8")

        ### AUTHORIZATION 
        if not data or data != "Start_Connection":
            connection.close()
        randomString = "".join(random.choices(string.ascii_letters + string.digits, k=32)).encode("utf-8")
        connection.sendall(randomString)
        connection.send
        correctHash = hashlib.sha1(randomString + privateString).hexdigest()
        data = connection.recv(40).decode("utf-8")
        #print(data)
        #print(correctHash)
        if not data:
            connection.close()
        elif data != correctHash:
            print("------- UNAUTHORIZED")
            connection.close()
        else:
            print("------- AUTHORIZED")
            connection.sendall("Authentication succesful. Do you wish to proceed? ('Y', 'N')".encode("utf-8"))
            data = connection.recv(1024).decode("utf-8")
            if not data:
                connection.close()
            elif data == "Y":
                print("------- CLIENT WISHES TO PROCEED")
            else:
                print("------- CLIENT DOES NOT WISHES TO PROCEED, CLOSING CONNECTION")
                connection.close()
                exit()

            thread = threading.Thread(target=sendRemainingTimePeriodically)
            #thread.start()

            while(True):
                data = connection.recv(1024)
                if(not data):
                    continue

                #PARSE DATA
                
                command = int.from_bytes(data[0:1], "big", signed=False)
                print("command=", command)
                if command == 0:
                    print("startgame")
                    startGame()
                elif command == 1:
                    print("terminateGame")
                    terminateGame()
                elif command == 2:
                    print("sendRemainingTime")
                    sendRemainingTime()
                elif command == 3:
                    print("guess")
                    guess(data[1:])
                #print(int.from_bytes(data, "big"))