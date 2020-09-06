import random

IP = '127.0.0.1'
ALICE_DESTINATION_PORT = 49152
BOB_DESTINATION_PORT = 49153
ALICE_RECEIVING_PORT = 49154
BOB_RECEIVING_PORT = 49155
#ALICE_DESTINATION_ADDRESS = (IP, ALICE_DESTINATION_PORT)
#BOB_DESTINATION_ADDRESS = (IP, BOB_DESTINATION_PORT)
ALICE_RECEIVING_ADDRESS = (IP, ALICE_RECEIVING_PORT)
BOB_RECEIVING_ADDRESS = (IP, BOB_RECEIVING_PORT)

def check_availabity(location):
    """
    Checks to see if the port is available on the localhost
    """
    availability = a_socket.connect_ex(location)
    if availabity == 0:
        print("Port is open")
    else:
        print("Port is not open")
        while availability != 0:
            PORT = randrange(49152, 65535)
            location = (IP, PORT)
            availability = a_socket.connect_ex(location)
        print("Port is now open")