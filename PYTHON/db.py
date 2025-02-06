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
        
import os
import supabase
def connectionDB():
    try:
        print("accediendo a la DB")
        url = "https://grisdoxyktoiepndxbdp.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdyaXNkb3h5a3RvaWVwbmR4YmRwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg2OTE2NDAsImV4cCI6MjA1NDI2NzY0MH0.b2VJ04SY2uo7svxQIi3S-TJq0hOmJg7fhGuuxutYHGQ"
        print("Se accedio a la DB")
    except Exception as err:
        print(f"no se logro conectar a la DB {err}")
    supabase.Client(url, key)




