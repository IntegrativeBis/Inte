from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect 
import secrets
from werkzeug.security import generate_password_hash
from DbModels import login, user_register
app = Flask('__name__', template_folder="SRC/templates", static_folder="SRC/static") # no es necesario pq la carpeta se llama asi y jinja busca esa por defecto
#login_manager = LoginManager()
#login_manager.init_app(app) #enlazamos con la app
#login_manager.login_view = 'IniciarSesion' #si el usuario intenta entrar a una vista protegida te redirige a esto
#login_manager.login_message = "Inicie sesion para acceder a este contenido"

#INVENTAMOS UNA LLAVE SECRETA ALEATORIA
secret_key = secrets.token_hex(16)
#ASIGNAMOS LA LLAVE SECRETA A LA APP
app.secret_key = secret_key
#csrf=CSRFProtect()

@app.route ('/')
def inicio():
    return render_template("inicio_ss.html")
    
#INICIARSESION RUTA
@app.route ('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    estado = "Introduce data"
    data={} #quien ba a recopilar la info
    telefono=request.args.get ("telefono")
    password=request.args.get ("password")
    
    if telefono and password:
        try:
            user = login(telefono, password)
            if user:
                usuario = session['user'] #hay que ver como guardar al usuario
                estado = "Correct"
                return render_template('/inicio_cs.html', usuario = usuario)
            else:
                estado = "Incorrect"
        except Exception as e:
            print(e)
    #print ([0][1]) #se imprpimira el telefono
    return render_template('iniciar_sesion.html', data = data, estado = estado)
        
@app.errorhandler(404)
def err_handler(e):
    return render_template('error_404.html')
        
#ya estamos iniciados
@app.route('/inicio_cs') #hicimos una ruta donde te llevara a la pagina protegida solo si estas registrado
def inicio_cs():
    
    return "<h1> esta es una vista protegida solo para usuarios </h1>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

@app.route ('/registrar', methods=['GET', 'POST'])
def registrar():
    user ={ #idk si esto debe estar dentro del IF
        'nombre': '',
        'apellido':'',
        'telefono':'',
        } #quien ba a recopilar la info
    mensaje = None
    
    if request.method == 'POST':
        user['nombre']=request.form.get ("nombre")
        user['apellido']=request.form.get ("apellido")
        user['telefono']=request.form.get ("telefono")
        password=request.form.get ("password")
        session['user'] = user
 
        hashed_password=generate_password_hash (password)
        try:
            user_register(user['nombre'], user['apellido'], user['telefono'], hashed_password)
            mensaje = "REGISTRO EXITOSO"
            return render_template('iniciar_sesion.html', mensaje = mensaje)
        except Exception as e:
            print(e)
            mensaje = "ERROR AL REGISTRAR. POR FAVOR INTENTA DE NUEVO."
            return render_template('registrar.html', mensaje = mensaje)
    return render_template('registrar.html', mensaje = mensaje)   

@app.route ('/listas')
def listas():
    return render_template("listas.html")




"""if "user" in session: """

if (__name__)=='__main__':
    #csrf.init_app(app)
    app.run(debug=True) #aqui podrias agregar el host y el puerto al que se quiere conectar y no se que threaded