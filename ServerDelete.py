import socket
from tabulate import tabulate
from database import Database

db = Database('vsmdb' , load=True)
db = Database('smdb', load=True)

HOST = '127.0.0.1'
PORT = 65432

def Delete_From_Table(QUERY):
	QUERY = QUERY.lstrip("DELETE FROM")
	table_name = QUERY.split()[0].lstrip(" ")
	column_name = QUERY.split("WHERE")[1].split("=")[0].lstrip(" ")
	value_name = QUERY.split("WHERE")[1].split("=")[1].replace("'"," ").lstrip(" ")
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

while True:
    QUERY = conn.recv(1024)
    QUERY = QUERY.decode('utf-8')
    if QUERY.startswith('DELETE FROM'):
        try:
            tablen = Delete_From_Table(QUERY)
        except:
            print("An error occured")
    else:
        conn.send(tablen.encode())   # Send table name to client.
        print("Delete completed")
    if not QUERY.startswith('DELETE FROM'):
        break

s.close()