import socket
from database import Database

db = Database('vsmdb', load=True)
db = Database('smdb', load=True)

HOST = '127.0.0.1'
PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
    s.connect((HOST, PORT))

    redo = 'y'
    while True and redo == 'y':
        QUERY = input("Insert DELETE query: ")
       
        while not QUERY.startswith("DELETE FROM ") or ' WHERE ' not in QUERY:
            QUERY = input("Please type the command correctly! ")
        
        s.sendall(bytes(QUERY, 'utf-8'))

        data = s.recv(1024).decode()

        if not data.startswith("An"):
            db.show_table(data)
            print("Delete Completed")
        else:
            print(data)
        redo = input("Press y if you wish to try again or n to exit: ")
     
    s.close()   # Close connection.