from flask_login import UserMixin, LoginManager
from werkzeug.security import check_password_hash
import Models

login_manager = LoginManager()
class User(UserMixin):

    def __init__(self, id, nombre, apellido, telefono, correo, password) -> None:
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.password = password
#creamos un usuaraio de ejemplo  
user = User(id=1, nombre="Juan", apellido="si", telefono=623, correo="juancho@gmail.com")

@login_manager.user_loader
def load_user(user_id):
    return Models.get_by_id(id)

@classmethod
def Confirm_Password(self, hashed_password, password):
    return check_password_hash(hashed_password, password)