import socket
from tabulate import tabulate
from database import Database

db = Database('vsmdb' , load=True)
db = Database('smdb', load=True)

HOST = '127.0.0.1'
PORT = 65432


def delete_from_table(QUERY):
    QUERY = QUERY.lstrip("DELETE FROM")
    table_name = QUERY.split()[0].lstrip(" ")
    where_condition = QUERY.split("WHERE")[1].lstrip()
    db.delete(table_name, where_condition)
    db.unlock_table(table_name)
    return table_name


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:    # Establish IPV4, TCP connection.
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        print('Waiting for query: ')

        x = True
        while x:
            QUERY = conn.recv(1024)
            QUERY = QUERY.decode('utf-8')
            if QUERY.startswith('DELETE FROM'):
                try:
                    table = delete_from_table(QUERY)
                except Exception as e:
                    err = "An error has occured: " + str(e)
                    db.unlock_table(table)
                    conn.sendall(bytes(err, "utf-8"))
                else:
                    conn.send(table.encode())  # Send table name to client.
                    print("Delete completed")
            if not QUERY.startswith('DELETE FROM'):
                x = False

        s.close()   # Close connection.
