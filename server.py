import hashlib
import socket
import random
import string

### Aykut Atmaca 150170008, Computer Communications Project 1, Socked Programming Assigment
### server.py

HOST = "127.0.0.1"
PORT = 7070
privateString = "comComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomComcomCom".encode("utf-8")

print("\n------- SERVER PROCESS START")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((HOST, PORT))
    sock.listen()
    connection, address = sock.accept()
    with connection:
        print("------- CONNECTION SUCCESSFULL, ADDRESS:", address)
        while True:
            data = connection.recv(1024).decode("utf-8")

            ### AUTHORIZATION 
            if not data or data != "Start_Connection":
                connection.close()
                break

            randomString = "".join(random.choices(string.ascii_letters + string.digits, k=32)).encode("utf-8")
            connection.sendall(randomString)
            correctHash = hashlib.sha1(randomString + privateString).hexdigest()
            data = connection.recv(40).decode("utf-8")
            print(data)
            print(correctHash)
            if not data:
                connection.close()
                break
            elif data != correctHash:
                print("------- UNAUTHORIZED")
                connection.close()
                break
            else:
                print("------- AUTHORIZED")
                connection.sendall("Authentication succesful. Do you wish to proceed? ('Y', 'N')".encode("utf-8"))
                data = connection.recv(1024).decode("utf-8")
                if not data:
                    connection.close()
                    break
                elif data == "Y":
                    print("------- CLIENT WISHES TO PROCEED")
                else:
                    print("------- CLIENT DOES NOT WISHES TO PROCEED, CLOSING CONNECTION")
                    connection.close()
                    break
