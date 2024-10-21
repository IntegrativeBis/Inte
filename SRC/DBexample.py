#aqui hacemos la conexion
import pyodbc
from database.dbconnection import DevelopmentConfig

try:
    db=pyodbc.connect(DevelopmentConfig.connection) #aqui hay que cambiarle el sql
    #connection=pyodbc.connect('DRIVER={SQL Server};SERVER=OR0510;DATABASE=AdventureWorks2022')
    #print("conexion exitosa")
    #lo que hay entre parentesis es lo que se debe de poner
    print('coneccion exitosa')
    """cursor=db.cursor()
    cursor.execute("SELECT * FROM Person.Address") #cursor.execute("SELECT @@version")
    row=cursor.fetchone() 
    print(row)
    #ES PARA MOSTRAR LO QUE EJECUTE EL CURSOR"""
    
   # rows=cursor.fetchall() #para imprimir todas las columnas?
   # for row in rows:
   #     print(row)
except Exception as ex:
    print(ex)
#finally:
    #connection.close()
    #print("ya cerramos la conexion")
    
    
    #CRUD