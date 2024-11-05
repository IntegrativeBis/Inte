import pyodbc
def dbconnection(): #esto es pa conectarse a la base datos
    try:
        conecction = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=OR0510; DATABASE=INTEGRADOR; UID=sa; PWD=Omar2805!;')
    except Exception as ex:
        print(ex)        
    return conecction


