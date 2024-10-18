from flask import Flask, render_template, request, url_for, redirect #importamos flask


app= Flask(__name__)

@app.route ('/') #para indicar que es la urta raiz
def index():
    productos = ['frijoles', 'atun', 'mierda', 'aire']
    data = {
        'titulo': 'Index',
        'Bienvenida': 'Saludos',
        'Productos': productos, #MUCHO CUIDADO CON LAS MAYUSCULAS
        'numero_productos': len(productos) #0 por si quieres comprobar
    }
    
    return render_template('index.html', data=data) #regresamos el documento HTML
    #return "Hola" #esto se puede meter como estructura HTML

def web_notfound (error):
    #return render_template('404.html'), 404[este es el codigo de error] #esto funciona [ara que a; definir una pagina que no exista te redireccione a una pagina que te diga error]
    return redirect(url_for('index')) #esto es para que en lugar de llevarte al error, te redireccione a la pagina principa o index


@app.route('/contacto/<nombre>/<int:edad>')
def contacto(nombre, edad):
    data1 = {
        'titulo': ' contacto',
        'nombre': nombre,
        'edad': edad
    }
    return render_template('contacto.html', data1=data1)

def query_string():
    print(request)
    return "ok"

if __name__ == '__main__':
    app.register_error_handler(404, web_notfound)
    #app.add_template_test('/query_string', view_func=query_string)
    app.run(debug=True,port=5000)
    #debug es para que constantemente la pagina se actuelice con los cambios guardados en lugar de tener que cerrar el servidor y volverlo a activar
    #el port es para cambiar a que puerto rediriges la pagina