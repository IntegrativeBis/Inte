import pyodbc
def dbconnection(): #esto es pa conectarse a la base datos
    try:
        print ("CONECTANDO ESTA CHINGADERA")
        connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=priceseekerbis.ddns.net; DATABASE=PriceSeeker; UID=SA; PWD=1234;')
        print ("CANCEROIDE")
        return connection
    except Exception as ex:
        print(f"ERRORCITO {ex} ") 
        


