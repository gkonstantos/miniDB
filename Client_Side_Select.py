import socket

HOST = '127.0.0.1'
PORT = 65432

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.connect((HOST , PORT))

    while True:
        QUERY = input("Insert your SELECT query or press e for exit: \n")
        print("#-#-#")
        if QUERY == "e":
            break
        else:
            s.sendall(bytes(QUERY,'utf-8'))
            data = s.recv(1024)
            data = data.decode("utf-8")
            print(data)
 
    s.close()