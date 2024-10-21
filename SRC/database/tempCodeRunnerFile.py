

#class Config:
    #SECRET_KEY = 'B!1w8NAt1T^%kvhUI*S^' #aun no se pa q sirve

class DevelopmentConfig(): #esto es pa conectarse a la base datos, ya lo habia hecho pero aqui esta mas bonito
    #DEBUG = True #para que este en modo debug
    connection = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=OR0510;"
        "DATABASE=AdventureWorks2022"
        "UID=sa;" #CONECTADOO tuve que crear un perfil SA para poder acceder
        "PWD=Omar2805!;"
    )   


config = { #un diccionario que apunta a este archivo
    'development': DevelopmentConfig
}

