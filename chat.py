from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import socket
import threading
BUFFER_SIZE = 1024

class ChatListener(threading.Thread):
    def __init__(self, node, listening_address):
        print("Initializing chat listener. Listening on " + str(listening_address))
        threading.Thread.__init__(self)
        self.node = node
        self.listening_address = listening_address

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(self.listening_address)
        sock.listen()

        connection, address = sock.accept()
        print(self.node.public_key)
        pem = self.node.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        connection.recv(BUFFER_SIZE)
        connection.send(pem)
        while True:
            cipher = connection.recv(BUFFER_SIZE)
            plaintext = self.node.private_key.decrypt(
                cipher,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            ).decode()
            print(plaintext)

class ChatSender(threading.Thread):
    def __init__(self, node, destination_address):
        print("Initializing chat sender with the destination address at " + str(destination_address))
        threading.Thread.__init__(self)
        self.node = node
        self.destination_address = destination_address

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.destination_address)

        sock.send(b"1") #request for other's private key
        public_key = sock.recv(BUFFER_SIZE)
        public_key = load_pem_public_key(public_key)
        while True:
            message = input("Message: ").encode()
            cipher = public_key.encrypt(
                message,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label = None
                )
            )
            sock.send(cipher)