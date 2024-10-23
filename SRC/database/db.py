import pyodbc
def dbconnection(): #esto es pa conectarse a la base datos
    return pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=OR0510; DATABASE=TIENDITA; UID=sa; PWD=Omar2805!;')
def cursor():
    cursor=pyodbc.Cursor

    