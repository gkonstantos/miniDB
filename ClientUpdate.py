import socket
from database import Database

# Load databases.
db = Database('vsmdb', load=True)
db = Database('smdb', load=True)

HOST = '127.0.0.1'  # The server's hostname or IP address.
PORT = 65432        # The port used by the server.

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Establish IPV4, TCP connection.
    s.connect((HOST, PORT))

    retry = 'y'
    while True and retry == 'y':    # Loop, receive query from input, check if it has the right structure.
        QUERY = input("Waiting for query: ")

        while not QUERY.startswith("UPDATE ") or ' SET ' not in QUERY or ' WHERE ' not in QUERY:
            QUERY = input("Please type the command correctly! ")

        s.sendall(bytes(QUERY, 'utf-8'))    # Send query to server.

        data = s.recv(1024).decode("utf-8")    # Receive table name from server.
        if not data.startswith("An"):   # if no mistakes have been committed, show the updated table.
            db.show_table(data)     # Call show_table() from database.py.
            print("change completed")
        else:
            print(data)
        retry = input("Press y to try again or n to quit: ")    # Option to do another query.

    s.close()   # Close connection.
