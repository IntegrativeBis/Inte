import pyodbc
def dbconnection(): #esto es pa conectarse a la base datos
    try:
        print ("CONECTANDO BASE DE DATITOS")
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=189.237.88.4; DATABASE=PriceSeeker; UID=sa; PWD=1234;')#tiene que ser por IP porque por dns no esta jalando
        return connection
    except Exception as ex:
        print(f"CANCEROIDE NO PUDE CONECTARLA, ERRORCITO: {ex} ") 
        


