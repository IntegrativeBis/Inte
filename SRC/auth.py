from flask import Flask, render_template, request, redirect, url_for, session
from db import cursor
from werkzeug.security import check_password_hash
app = Flask('__name__', template_folder="SRC/templates")
#FUNCION PARA INICIAR SESION
def IniciarSesion():
    if request.method == 'POST' and 'txtCorreo' in request.form and 'txtPassword' in request.form: 
        correo = request.form['txtCorreo']
        password = request.form['txtPassword']
        cursor.execute('SELECT password FROM usuarios WHERE correo = ?', (correo,))
        usuario = cursor.fetchone() #loq ue arroje el sql sera la variable usuario
        #comprobamos si las contrasenias son correctas con el check hacemos que la revise 
        if usuario and check_password_hash(usuario.password, password): #usuario[0] en lugar de usaurio.pass si hay error
            cursor.execute('SELECT id FROM usuarios WHERE correo = ?', (correo,))
            IdUsuario= cursor.fetchone()
            session['loggeado'] = True
            session['id'] = IdUsuario['id'] # IdUsuario[0] si da error
            return redirect(url_for("Inicio_CS")) #aqui puse un ejemplo de redireccion cuando Ana lo coloque lo cambio
        
    else:
        # La contraseña es incorrecta
        return render_template('Iniciar_Sesion.html', mensaje="Correo o contraseña incorrecta")#lo regresamos al login y le decimos el mensaje si ANA hace lo que le pedi
    return render_template('Iniciar_Sesion.html')
        