from werkzeug.security import check_password_hash #, generate_password_hash
from flask_login import UserMixin
class User(UserMixin): #valores de la tabla usuarios #esto para que herede de esa clase y active algo importante llamado is active
    
    def __init__(self, id, username, password, fullname) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        
        
    @classmethod
    def check_password(self, hashed_password,password): #generamos una password hasheada para que no puedan hacer cositas malas en nuestra cuenta
        #la hashed password es la contrasenia ya hash y las psw es en archivo plano
        return check_password_hash(hashed_password, password)
#print(generate_password_hash("suscri"))#esto se uso para wue en el sql pongamos esa contra, asi agregando un perfil para luego autenticar