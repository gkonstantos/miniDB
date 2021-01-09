import socket
from database import Database

# Load databases.
db = Database('vsmdb', load=True)
db = Database('smdb', load=True)


def update_table(QUERY):    # Function responsible for executing th update command.
# Split the query into the right parts.
    QUERY = QUERY.lstrip("UPDATE")  # query without UPDATE keyword.
    table_name = QUERY.split("SET")[0].split(",")[0].lstrip().split(" ")[0]    # Get table name.
    updated_column = QUERY.split("SET")[1].split("WHERE")[0].split("==")[0].lstrip().split(" ")[0]   # Get column to be updated.
    updated_value = QUERY.split("SET")[1].split("WHERE")[0].split("==")[1].split(" ")[1]    # Get new value.
    where_condition = QUERY.split("WHERE")[1].lstrip()   # Get needed condition in order to update.
    db.update(table_name, updated_value, updated_column, where_condition)   # Call update() from database.py.
    db.unlock_table(table_name)  # Table locks for some reason, force unlock.
    return table_name


HOST = '127.0.0.1'  # Standard loopback interface address (localhost).
PORT = 65432        # Port to listen on.


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Establish IPV4, TCP connection.
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        print('Waiting for query: ')

        x = True    # Loop, receive queries, check if they have the right structure and send to client.
        while x:
            QUERY = conn.recv(1024)
            QUERY = QUERY.decode('utf-8')
            if QUERY.startswith('UPDATE'):
                try:
                    table = update_table(QUERY)    # Call above function.
                except:
                    print("Wrong column name! ")
                    db.unlock_table(table)  # Table locks for some reason, force unlock.
                    conn.send("Wrong column name! ".encode())
                else:
                    conn.send(table.encode())   # Send table name to client.
                    print("change completed")

            if not QUERY.startswith("UPDATE"):  # End loop.
                x = False

        s.close()   # Close connection.
