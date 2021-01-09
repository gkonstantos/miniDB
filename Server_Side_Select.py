import socket
from tabulate import tabulate
from database import Database

db = Database('vsmdb' , load=True)

HOST = '127.0.0.1'
PORT = 65432

def Select_From_Table(QUERY):
    db.unlock_table('classroom')
    QUERY = QUERY.lstrip("SELECT") # query = "[*,[column1,column2,..,columnN]] from table [where condition]"
    table = Find_Table_In_Select(QUERY)
    table_columns = Find_TableColumns_In_Select(QUERY)
    where_condition = Find_WhereCondition_In_Select(QUERY)
    return Execute_Select_Query(table,table_columns,where_condition)

def Find_Table_In_Select(QUERY):
    return QUERY.split("FROM")[1].split("WHERE")[0].strip()

def Find_TableColumns_In_Select(QUERY):
    columns = QUERY.split("FROM")[0].split(",")
    for i in range(len(columns)):
        columns[i] = columns[i].strip()
    return columns

def Find_WhereCondition_In_Select(QUERY):
    return QUERY.split("WHERE")[1].strip() if QUERY.find("WHERE") != -1 else ""

def Execute_Select_Query(table,table_columns,where_condition):
    if where_condition == "" and table_columns[0] == '*':
        return db.select(table,"*",None,None,False,None,None,True)
    elif where_condition != "" and table_columns[0] == "*":
        return db.select(table,"*",where_condition,None,False,None,None,True)
    elif(where_condition == "" and len(table_columns) == 1):
        return db.select(table,[table_columns[0]],None,None,False,None,None,True)
    elif where_condition == "" and len(table_columns) > 1:
        return db.select(table,table_columns,None,None,False,None,None,True)
    elif where_condition != "" and len(table_columns) == 1:
        return db.select(table,[table_columns[0]],where_condition,None,False,None,None,True)
    elif where_condition != "" and len(table_columns) > 1:
        return db.select(table,table_columns,where_condition,None,False,None,None,True)

def Convert_ResultSetTable_toString(ResultSet):
    ConvertedResultSet = f"\n## {ResultSet._name} ##"
    headers = [f'{col} ({tp.__name__})' for col, tp in zip(ResultSet.column_names, ResultSet.column_types)]
    if ResultSet.pk_idx is not None:
        headers[ResultSet.pk_idx] = headers[ResultSet.pk_idx]+' #PK#'
    non_none_rows = [row for row in ResultSet.data if any(row)]
    ConvertedResultSet = tabulate(non_none_rows[:None], headers=headers)+'\n'
    return ConvertedResultSet

with socket.socket(socket.AF_INET , socket.SOCK_STREAM) as s:
    s.bind((HOST , PORT))
    s.listen()
    conn , addr = s.accept()
    with conn:
        print('Connected by' , addr)
        print('Waiting for query: ')
        while True:
            QUERY = conn.recv(1024)
            QUERY = QUERY.decode("utf-8")
            if QUERY.startswith("SELECT"):
                try:
                    ResultSet = Select_From_Table(QUERY)
                    Converted_Result_Set = Convert_ResultSetTable_toString(ResultSet)
                    conn.sendall(bytes(str(Converted_Result_Set),'utf-8'))
                except Exception as e:
                    message = "An error has occured: " + str(e)
                    conn.sendall(bytes(message, "utf-8"))
            else:
                conn.sendall(bytes("Your query must begin with SELECT(SQL reserved keywords must be written with capital letters)." , "utf-8"))
            if not QUERY:
                break

#|-------|
#Select_From_Table: Parse the QUERY string and find the table name,desired columns and where condition
#We need an if statement in Execute_Select_Query(...) because the asterisk needs to be declared explicitly in db.select()
#while any column alone must be inside an array(db.select(...,table_columns[0]...) throws an exception due to db.select() implementation.
#Finally,an exception is thrown if where_condition == "" inside db.select(...).
# ---
#Convert_ResultSetTable_toString() copies the code from table.show() in table.py and returns the output from tabulate in 
#Converted_Result_Set.The variable is then passed to client where it is printed.
#|-------|