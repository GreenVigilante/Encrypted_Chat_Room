import socket
import threading
import rsa

public_key, private_key = rsa.newkeys(1024)
partner = None
yapper = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
yapper.connect(("localhost", 9999))
yapper.send(public_key.save_pkcs1("PEM"))
partner = rsa.PublicKey.load_pkcs1(yapper.recv(1024))

def send(yapper):
    while True:
        message = str(input(""))
        yapper.send(rsa.encrypt(message.encode(),partner))
        print("You: "+ message)
        if message == "exit()":
            break

def recv(yapper):
    while True:
        print("Him: "+rsa.decrypt(yapper.recv(1024), priv_key=private_key).decode())

t1 = threading.Thread(target=send, args=(yapper, ))
t1.start()
t2 = threading.Thread(target=recv, args=(yapper, ))
t2.start()