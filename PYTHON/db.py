# import pyodbc
# from PRIVATE import USER, PASSWORD, DATABASE, SERVER, DRIVER
# def dbconnection(): #esto es pa conectarse a la base datos
#     try:
#         print ("CONECTANDO BASE DE DATITOS...")
#         connection = pyodbc.connect(f"DRIVER={DRIVER};SERVER={SERVER}; DATABASE={DATABASE}; UID={USER}; PWD={PASSWORD};")
#         print ("CONECTAMOS LA BSE")
#         return connection
#     except Exception as ex:
#         print(f"NO PUDE CONECTARLA, EL ERRORCITO ES: {ex} ") 
#         return None
        
import supabase
from PRIVATE import url, key
def connectionDB():
    try:
        print("accediendo a la DB")
        supabase.Client(url, key)
        print("Se accedio a la DB")
    except Exception as err:
        print(f"no se logro conectar a la DB {err}")
    




