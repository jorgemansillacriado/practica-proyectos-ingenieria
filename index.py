from flask import Flask, request, render_template, session, redirect
import pymongo 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import requests
from bs4 import BeautifulSoup
import statistics
import math


# Try connecting without SSL verification (use with caution in production!)

app = Flask(__name__)

@app.route("/",methods=['POST','GET'])
def validar():
    if request.method == 'POST':
        usuario = request.form["login"]
        password = request.form["password"]

        client = MongoClient ('mongodb+srv://jarabers:xxxxxx@clusterjorge.uesqo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJorge', tlsAllowInvalidCertificates=True) 
        db = client['travel']
        collection = db['usuarios']
        x = collection.find_one({'login':usuario, 'password':password})

        if x:
            collection = db['destinos']
            x = collection.find({})

            #incluir el código del recomendador para que nos devuelva el destino con más valoracion
            #lo devolvemos al render en el parámetro favorito un diccionario con los datos para 
            #pintar en la pag
            #obtenemos destinos
            x_p = collection.find({})

            dest = []
            for elem in x_p:
                dest.append(elem['nombre'])

            # #obtenemos usu
            usuarios = []
            collection = db['usuarios']
            x2 = collection.find({})
            for elem in x2:
                usuarios.append(elem['login'])

            collection = db['valoracion']
            travel = list(collection.find())

            def devolver_valoraciones(usuario):
                for i, elem in enumerate(travel):
                    if elem['usuario'] == usuario:
                        return(elem['valoraciones'])

            def calcularmedia(valoracion1,valoracion2):
                cont = 0
                suma1 = 0
                suma2 = 0
                r_a = []
                r_b = []
                for elem in valoracion1:
                    if elem in valoracion2:
                        cont += 1
                        suma1 += valoracion1.get(elem)
                        suma2 += valoracion2.get(elem)
                        r_a.append(valoracion1.get(elem))
                        r_b.append(valoracion2.get(elem))
                return(r_a, r_b, suma1/cont, suma2/cont)

            def calcular_similitud(usuario1, usuario2):
                val1 = devolver_valoraciones(usuario1)
                val2 = devolver_valoraciones(usuario2)
                r_a, r_b, r_a_med, r_b_med = calcularmedia(val1,val2)
                
                numerador = 0
                denominador1 = 0
                denominador2 = 0
                
                for i, elem in enumerate(r_a):
                    numerador += (elem - r_a_med) * (r_b[i] - r_b_med)
                    denominador1 +=  ((elem - r_a_med) ** 2)
                    denominador2 +=  ((r_b[i] - r_b_med) ** 2)

                return(numerador/(math.sqrt(denominador1) * math.sqrt(denominador2)))

            def calcular_similitudes():
                matriz = {}
                for i in range(0,len(usuarios)):
                    elem = {}
                    for j in range(0,len(usuarios)):
                        if i != j:
                            elem[usuarios[j]] = calcular_similitud(usuarios[i],usuarios[j])
                    matriz[usuarios[i]] = elem
                return(matriz)

            def usuarios_parecidos(usuario, g):
                l = []
                valoracion = m[usuario]
                for key, value in valoracion.items():
                    if value >= g:
                        l.append(key)
                return l

            def devolver_destino_preferido(usuario):
                p = -1
                reco = ""
                for i in range(0,len(travel)):
                    if usuario == travel[i]['usuario']:
                        valoracion = travel[i].get('valoraciones')
                        for j in range(0,len(dest)):
                            #si no se ha valorado predecimos
                            if not dest[j] in valoracion:
                                aux = prediccion(usuario,dest[j])
                                if aux > p:                                         
                                    reco = dest[j]
                                    p = aux
                return(reco)

            def calcular_media_total(usu):
                val = devolver_valoraciones(usu)
                return(statistics.mean(tuple(val.values())))

            def prediccion(usu, d):
                l = usuarios_parecidos(usu,0.7)
                numerador = 0
                denominador = 0
                for i in l:
                    numerador += m[usu][i] * (devolver_valoraciones(i).get(d,0) - calcular_media_total(i))
                    denominador += m[usu][i]
                return(numerador / denominador + calcular_media_total(usu))

            def devolver_datos_destino(d):
                collection = db['destinos']
                x3 = collection.find_one({'nombre':d})
                if x3:
                    return(x3)
                
            m = calcular_similitudes()
            l1 = devolver_destino_preferido(usuario)
            fav = devolver_datos_destino(l1)

            return render_template("home.html", login = usuario, destinos = x, favorito = fav)

        else:
            return render_template("login.html",error = True)

    return render_template("login.html")
    
@app.route('/chat', methods=['POST'])
def chat():
    mensaje = request.form['mensaje'].lower()

    # Lógica simple del bot
    if "hola" in mensaje:
        respuesta = "¡Hola! ¿En qué puedo ayudarte?"
    elif "viaje" in mensaje:
        respuesta = "Tenemos destinos increíbles. ¿A cuál quieres ir?"
    else:
        respuesta = "Lo siento, no entiendo. ¿Puedes repetirlo?"

    return render_template('home.html', respuesta=respuesta)

@app.route("/detalle",methods=['POST','GET'])
def detalle():
    if request.method == 'POST':
        usuario = request.form["login"]
        destino = request.form["destino"]
        client = MongoClient ('mongodb+srv://jarabers:xxxxxx@clusterjorge.uesqo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJorge', tlsAllowInvalidCertificates=True) 
        db = client['travel']
        collection = db['destinos']
        x = collection.find_one({'nombre':destino})
        print(x)
        #obtengo el destino indicado por el usuario en la BD, por si no existe
        collection2 = db['valoracion']
        
        x2 = collection2.find_one({'usuario':usuario})
        print(x2)
        val = x2['valoraciones'].get(destino,0)
        print(destino)
        print(val)
        return render_template("detalle.html", login=usuario, destino=x, valoracion=val)

@app.route("/actualizar_like",methods=['POST','GET'])
def actualizar_like():
    if request.method == 'POST':
        valor = request.form["value"]
        usuario = request.form["usuario"]
        destino = request.form["destino"]
        client = MongoClient ('mongodb+srv://jarabers:xxxxxx@clusterjorge.uesqo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJorge', tlsAllowInvalidCertificates=True) 
        db = client['travel']
        collection = db['valoracion']
        x = collection.find_one({'usuario':usuario})
        valoracion_nueva = x["valoraciones"]
        print(valoracion_nueva)
        valoracion_nueva[destino] = int(valor)
        print(valoracion_nueva)
        collection.update_one({'usuario':usuario},{"$set":{"valoraciones":valoracion_nueva}})
        return("ok")
    
@app.route("/me_gustara",methods=['POST'])
def me_gustara():
    def calcular_media_total(usu):
        val = devolver_valoraciones(usu)
        return(statistics.mean(tuple(val.values()))) 
    def usuarios_parecidos(usuario, g):
        l = []
        valoracion = m[usuario]
        for key, value in valoracion.items():
            if value >= g:
                l.append(key)
        return l

    def devolver_valoraciones(usuario):
        for i, elem in enumerate(travel):
            if elem['usuario'] == usuario:
                return(elem['valoraciones'])

    def calcular_similitud(usuario1, usuario2):
        val1 = devolver_valoraciones(usuario1)
        val2 = devolver_valoraciones(usuario2)
        r_a, r_b, r_a_med, r_b_med = calcularmedia(val1,val2)
        numerador = 0
        denominador1 = 0
        denominador2 = 0
        for i, elem in enumerate(r_a):
            numerador += (elem - r_a_med) * (r_b[i] - r_b_med)
            denominador1 += ((elem - r_a_med) ** 2)
            denominador2 += ((r_b[i] - r_b_med) ** 2)
        return(numerador/(math.sqrt(denominador1) * math.sqrt(denominador2)))
    def calcular_similitudes():
        matriz = {}
        for i in range(0,len(usuarios)):
            elem = {}
            for j in range(0,len(usuarios)):
                if i != j:
                    elem[usuarios[j]] = calcular_similitud(usuarios[i],usuarios[j])
            matriz[usuarios[i]] = elem
        return(matriz)
    def calcularmedia(valoracion1,valoracion2):
        cont = 0
        suma1 = 0
        suma2 = 0
        r_a = []
        r_b = []
        for elem in valoracion1:
            if elem in valoracion2:
                cont += 1
                suma1 += valoracion1.get(elem)
                suma2 += valoracion2.get(elem)
                r_a.append(valoracion1.get(elem))
                r_b.append(valoracion2.get(elem))
        return(r_a, r_b, suma1/cont, suma2/cont)

    if request.method == 'POST':
        usuario = request.form["usuario"]
        destino = request.form["destino"]
        client = MongoClient ('mongodb+srv://jarabers:vzlqOjNzmsBdASty@clusterjorge.uesqo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterJorge', tlsAllowInvalidCertificates=True) 
        db = client['travel']
        collection = db['destinos']
        x = collection.find({})
        dest = []
        for elem in x:
            dest.append(elem['nombre'])
        usuarios = []
        collection = db['usuarios']
        x2 = collection.find({})
        for elem in x2:
            usuarios.append(elem['login'])
        collection = db['valoracion']
        travel = list(collection.find())
        m = calcular_similitudes()
        l = usuarios_parecidos(usuario,0.7)
        numerador = 0
        denominador = 0
        for i in l:
            numerador += m[usuario][i] * (devolver_valoraciones(i).get(destino,0) - calcular_media_total(i))
            denominador += m[usuario][i]
        p = (numerador / denominador + calcular_media_total(usuario))
        print(usuario)
        print(p)
        if p > 4:
            return("<p style='color:white;font-family: Arial, Helvetica, sans-serif;font-size:20pt;'>Seguro</p>")
        else:
            return("<p style='color:white;font-family: Arial, Helvetica, sans-serif;font-size:20pt;'>No tanto</p>")

"""
@app.route('/scrape')
def scrape():
    url = 'https://news.ycombinator.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    titulos = [a.text for a in soup.select('.titleline a')]
    return render_template('scrape.html', titulos=titulos)

"""

if __name__ == '__main__':
    app.run(port=8000,debug=True)



