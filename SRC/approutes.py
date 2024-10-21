from flask import Flask, render_template, request, redirect, url_for, flash, Response, session
from database.DevelopmentConfig import config, DevelopmentConfig #ME DA UN ERROR NO SE PORQUEEEEE
import pyodbc
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect 
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
app=Flask(__name__) #template_folder=("templates") no es necesario pq la carpeta se llama asi y jinja busca esa por defecto
#INVENTAMOS UNA LLAVE SECRETA ALEATORIA
secret_key = secrets.token_hex(16)
#ASIGNAMOS LA LLAVE SECRETA A LA APP
app.secret_key = secret_key
csrf=CSRFProtect()

API_KEY = 'AIzaSyBpT4O929acaKiKmxevg9hl8sjanWnnOW0'
# Inicializa la conexión y el cursor
db=pyodbc.connect(DevelopmentConfig.connection) 
cursor=db.cursor()

#dentro de esto la viene la conexion con la base
login_manager_app=LoginManager(app)

@app.route ('/')
def Inicio():
    return render_template('Inicio_CS') #Inicio_SS


#FUNCION PARA INICIAR SESION
@app.route ('/IniciarSesion', method= ["GET","POST"])
def IniciarSesion():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form: 
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        cursor.execute('SELECT password FROM usuarios WHERE correo = ?', (correo,))
        usuario = cursor.fetchone() #loq ue arroje el sql sera la variable usuario
        #comprobamos si las contrasenias son correctas con el check hacemos que la revise 
        if usuario and check_password_hash(usuario.password, password): #usuario[0] en lugar de usaurio.pass si hay error
            cursor.execute('SELECT id FROM usuarios WHERE correo = ?' (correo,))
            IdUsuario= cursor.fetchone()
            session['loggeado'] = True
            session['id'] = IdUsuario['id'] # IdUsuario[0] si da error
            return redirect(url_for("Inicio_CS")) #aqui puse un ejemplo de redireccion cuando Ana lo coloque lo cambio
        
    else:
        # La contraseña es incorrecta
        return render_template('Iniciar_Sesion.html', mensaje="Correo o contraseña incorrecta")#lo regresamos al login y le decimos el mensaje si ANA hace lo que le pedi
    return render_template('Iniciar_Sesion.html')
        
    """
        account = cursor.fetchone()
        if account:
            session['loggeado'] = True
            session['id'] = account['id']
            return render_template("logged.html") #aqui puse un ejemplo de redireccion cuando Ana lo coloque lo cambio
        else: #AQUI SE SUPONE QUE TE SALTA EL ERROR YA DEFINIDO DEBAJO que significa que no estas registrado
            return render_template('Iniciar_Sesion.html', mensaje="usuario no encontrado") #lo regresamos al login y le decimos el mensaje si ANA hace lo que le pedi"""
        
        
#ya estamos iniciados
@app.route('/InicioSesion_CS') #hicimos una ruta donde te llevara a la pagina protegida solo si estas registrado
@login_required
def logged():
    return "<h1> esta es una vista protegida solo para usuarios </h1>"


#este es el acceso para registrarnos
@app.route ('/Registrarse', methods= ["GET", "POST"]) 
def registro(): 
    if request.method == 'POST':    
        Nombre = request.form['txtNombre']
        Celular = request.form['txtNumeroCel'] #obligatorio
        Correo = request.form['txtCorreo'] #puede ser nulo
        Password = generate_password_hash(request.form['txtPassword'])
        Apellido = request.form['txtApellido']
        #Apm = request.form['txtApellidoM']
        #Ubi = request.form['txtUbicacion']

        # Verificar si el correo ya está registrado
        cursor.execute("SELECT * FROM usuario WHERE Celular = ?", (Celular,))
        usuario_existente = cursor.fetchone()  # Si hay un resultado, significa que el correo ya está registrado

        if usuario_existente:
            # Si ya existe, devolver al formulario con un mensaje de error
            return render_template('Registrar.html', error="Este Celular ya está registrado.")
        
        # Si no existe, insertar el nuevo usuario
        cursor.execute("INSERT INTO usuario (Nombre, correo, password, apm, app, ciudad) VALUES (?, ?, ?, ?, ?, ?)", (Nombre, Correo, Password, Apm, App, Ubi))
        db.commit()
        
    return redirect(url_for('IniciarSesion', mensajito="usuario correctamente registrado"))

    
@app.route('/logout') #aqui se hara un boton en la ppagina para deslogearte estoy hablando en html aqui ya no
def logout():
    logout_user()
    return redirect(url_for('login'))

if (__name__)=='__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run(debug=True) #aqui podrias agregar el host y el puerto al que se quiere conectar y no se que threaded