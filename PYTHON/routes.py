
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import secrets
from datetime import timedelta
#from DbModels import (login, register_user, modify_user, delete_user, busqueda_productos_AD, modify_password, busqueda_productos_AD_by_category, 
#busqueda_productos, busqueda_productos_by_id, busqueda_categoria, ver_lista, modificar_producto, borrar_producto, integrar_producto)
from DbModels import *

app = Flask('__name__', template_folder="SRC/templates", static_folder="SRC/static") 


app.secret_key = secrets.token_hex(16) 

#AQUI SE ENCONTRARAN LAS RUTAS PRINCIPALES-------------------------------------------------------------------------------------

@app.route('/') 
def inicio(): 
    categorias = busqueda_categoria()
    if 'cel' in session :
        id_usuario = session['id']
        listas = obtener_listas(id_usuario)
        return render_template('inicio_cs.html', usuario=session, categorias=categorias, listas=listas)
    return render_template('inicio_ss.html', categorias = categorias)

#AQUI EN ADELANTE SOLO SE VERA LO QUE TENGA QUE VER CON EL USUARIOOOOOO----------------------------------------------------------------

@app.route ('/registrar', methods=['GET', 'POST'])
def registrar():
    mensaje = None
    print ("voy a hacer el request POST")
    if request.method == 'POST':
        nombre=request.form.get ("nombre")
        apellido=request.form.get ("apellido")
        celular=request.form.get ("celular")
        contrasena=request.form.get ("contrasena")
        confirmar_contrasena=request.form.get("confirmar_contrasena")
        print(f"Nombre: {nombre} \nApellido: {apellido} \ncelular: {celular} \nPassword: {contrasena} \nConfirmed_Password: {confirmar_contrasena}")
        if contrasena != confirmar_contrasena:
            mensaje = "Las contraseñas no coinciden"
            return render_template('registrar.html', mensaje = mensaje)   
        try:
            register_user(nombre, apellido, celular, contrasena)
            mensaje = "REGISTRO EXITOSO"
            return render_template('iniciar_sesion.html', mensaje = mensaje)
        except Exception as e:
            print(e)
            mensaje = "ERROR AL REGISTRAR. POR FAVOR INTENTA DE NUEVO."
    return render_template('registrar.html', mensaje = mensaje)   

#INICIARSESION RUTA
@app.route ('/iniciar_sesion', methods=[ 'POST'])
def iniciar_sesion():
    mensaje = "Introduce celular y contraseña"
    celular=request.form.get ("celular")
    contrasena=request.form.get ("contrasena")
    print(celular, contrasena)
    if celular and contrasena is not None:
        try:
            print("voy a usar la funcion LOGIN")
            usuario_info = login(celular, contrasena)
            print("login depositado")
            print(f"el id es: {usuario_info['id_usuario']}")
            session['id'] = usuario_info['id_usuario']
            session['cel'] = celular 
            session['nombre'] = usuario_info['nombre']
            session['apellido'] = usuario_info['apellido']
            print(session)
            mensaje = "Correct"
            return redirect(url_for('inicio', usuario_info = {usuario_info['nombre'], usuario_info['apellido']} ))
        except Exception as e:
                print(f"Error de login (routes): {e}" )
                mensaje = "Celular o Contraseña incorrectas"
    return render_template('iniciar_sesion.html', mensaje = mensaje)
    
@app.route('/cuenta')
def cuenta():
    if 'cel' in session:
        return render_template('cuenta.html')
    return pagina_no_encontrada(404)

@app.route('/cambiar_contrasena', methods=['GET', 'POST'])
def cambiar_contrasena():
    print("inicio con cambiar contrasena")
    if 'cel' in session:
        celular = session['cel']
        if request.method == 'POST':
            contrasena = request.form.get("contrasena")
            nuevacontrasena = request.form.get("nuevacontrasena")
            confirmar_nuevacontrasena = request.form.get("confirmar_nuevacontrasena")
            if nuevacontrasena == confirmar_nuevacontrasena:
                print(contrasena, nuevacontrasena)
                if contrasena == session.get('contrasena'):
                    try:
                        print("voy a usar la funcion MODIFY PASSWORD")
                        mensaje = modify_password(celular, nuevacontrasena)
                        return redirect(url_for('cuenta', mensaje=mensaje)) 
                    except Exception as e:
                        print(f"Error al modificar la contraseña: {e}")
                        mensaje = "No se logró modificar la contraseña"
                else:
                    mensaje = "La contraseña actual no es correcta."
            else:
                mensaje = "Las contraseñas nuevas no coinciden."
            # Redirigir con el mensaje de error
            return redirect(url_for('cuenta', mensaje=mensaje))
    # Si no hay un usuario 
    return pagina_no_encontrada(404)

    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('inicio'))

#DE AQUI EN ADELANTE SE ENCUENTRA TODO LO RELACIONADO CON PRODUCTOSSS Y BUSQUEDA-------------------------------------------------------------

@app.route('/buscar_productos') #esta ruta la usa el JS realtime durante se esta buscando producto en la barra buscadora
def buscar_productos():#aqui a medida que la barra se rellene se va a modificar todos los productos de abajo
    termino = request.args.get('q', '').lower()
    resultados = busqueda_productos(termino) 
    print(resultados)
    return jsonify(resultados) #se envian en formato Jaison

@app.route ('/busqueda', methods = ['GET']) #te redirecciona a alguna busqueda con el q que se le fue enviado desde el FORM inicio_ss.html
def busqueda(): 
    termino = request.args.get('q', '').lower() #agarra el argumento y lo hace minuscula
    pagina_actual = request.args.get('pagina_actual', 1)
    pagina_final = request.args.get('pagina_final', 5)
    resultados = busqueda_productos_AD(termino, pagina_actual, pagina_final)
    if 'cel' in session:
        return render_template('busqueda_cs.html')
    return render_template('busqueda_ss.html', pagina_actual=pagina_actual, pagina_final=pagina_final, resultados = resultados)

@app.route ('/busqueda_categorias/<int:id_categoria>', methods = ['GET']) #te redirecciona a alguna busqueda con el q que se le fue enviado desde el FORM inicio_ss.html
def busqueda_categorias(id_categoria): 
    #termino = request.args.get('q', '').lower() #NO SE SI SEA MEDIANTE ARGS O FORM
    pagina_actual = request.args.get('pagina_actual', 1)
    pagina_final = request.args.get('pagina_final', 5)
    resultados = busqueda_productos_AD_by_category(id_categoria, pagina_actual, pagina_final)
    if 'cel' in session:
        return render_template('busqueda_cs.html', pagina_actual=pagina_actual, pagina_final=pagina_final, resultados = resultados)
    return render_template('busqueda_ss.html', pagina_actual=pagina_actual, pagina_final=pagina_final, resultados = resultados)

@app.route ('/producto/<int:id_producto>') #va a tomar el argumento buscado (aqui debe tomar el argumento del producto seleccionado en busqueda NO SE ACERLO) para que te aparezca el producto 
def producto(id_producto): #   DEBERIA DE TOMAR EL ID
    """termino = request.args.get('q', '').lower()
    print(termino)"""
    productos = busqueda_productos_by_id(id_producto)
    print(productos) 
    if 'cel' in session:
        return render_template('producto_cs.html', producto=productos[0], recomendaciones=productos[1])
    return render_template('producto_ss.html', producto=productos[0], recomendaciones=productos[1]) #al ver otro producto el SQL no se vuelve a ejecutar

# AQUI IRA TODO LO NECESARIO PARA LA LISTA
@app.route ('/listas')
def listas(id_lista):
    if 'cel' in session:
        id_usuario = session['id']
        
        ver_lista(id_usuario, id_lista)
    return render_template("listas.html")


#A PARTIT DE AQUI SON ERRORES Y DEMAS COSAS --------------------------------------------------------------------------------------------------

@app.errorhandler(404)
def pagina_no_encontrada(e):
    return render_template('error_404.html'), 404
    
if (__name__)=='__main__':
    #csrf.init_app(app)
    app.permanent_session_lifetime = timedelta(minutes=30)
    app.run(debug=True) 