import pyodbc
from PRIVATE import USER, PASSWORD, DATABASE, SERVER
def dbconnection(): #esto es pa conectarse a la base datos
    try:
        print ("CONECTANDO BASE DE DATITOS...")
        connection = pyodbc.connect(f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={SERVER}; DATABASE={DATABASE}; UID={USER}; PWD={PASSWORD};")
        print ("CONECTAMOS LA BSE")
        return connection
    except Exception as ex:
        print(f"NO PUDE CONECTARLA, EL ERRORCITO ES: {ex} ") 
        return None
        


