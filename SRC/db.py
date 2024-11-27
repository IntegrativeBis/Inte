import pyodbc
def dbconnection(): #esto es pa conectarse a la base datos
    try:
        print ("CONECTANDO BASE DE DATITOS...")
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=priceseekerbis.ddns.net; DATABASE=PriceSeeker; UID=readeruser; PWD=1234;')
        print ("CONECTAMOS LA BSE")
        return connection
    except Exception as ex:
        print(f"NO PUDE CONECTARLA, EL ERRORCITO ES: {ex} ") 
        return None
        


