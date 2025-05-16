# -*- coding: utf-8 -*-
"""
Recomendador de destinos mejorado con visualización
"""
import math
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pprint import pprint

viajes = [{'usuario': 'pantolin',
  'valoraciones': {'DUBAI': 5, 'PUNTA CANA': 3, 'DISNEYLAND PARIS': 4, 'SANTIAGO': 4}},
 {'usuario': 'saka92',
  'valoraciones': {'DUBAI': 3, 'PUNTA CANA': 1, 'DISNEYLAND PARIS': 2, 'SANTIAGO': 3, 'FORMIGAL': 3}},
 {'usuario': 'agarrido',
  'valoraciones': {'DUBAI': 4, 'PUNTA CANA': 3, 'DISNEYLAND PARIS': 4, 'SANTIAGO': 3, 'FORMIGAL': 5}},
 {'usuario': 'chari89',
  'valoraciones': {'DUBAI': 3, 'PUNTA CANA': 3, 'DISNEYLAND PARIS': 1, 'SANTIAGO': 5, 'FORMIGAL': 4}},
 {'usuario': 'mario_pzk',
  'valoraciones': {'DUBAI': 1, 'PUNTA CANA': 5, 'DISNEYLAND PARIS': 5, 'SANTIAGO': 2, 'FORMIGAL': 1}}]

# Todos los destinos posibles definidos manualmente (mejor si se conoce el conjunto)
destinos = ["DUBAI", "PUNTA CANA", "DISNEYLAND PARIS", "SANTIAGO", "FORMIGAL"]
usuarios = ["pantolin","saka92","agarrido","chari89","mario_pzk"]

def obtener_usuarios(viajes):
    return [v["usuario"] for v in viajes]

def devolver_valoraciones_usuario(usuario):
    for elem in viajes:
        if elem["usuario"] == usuario:
            return elem["valoraciones"]
    return {}

def calcular_media(val1, val2):
    r_a, r_b, suma1, suma2, cont = [], [], 0, 0, 0
    for destino in val1:
        if destino in val2:
            cont += 1
            r_a.append(val1[destino])
            r_b.append(val2[destino])
            suma1 += val1[destino]
            suma2 += val2[destino]
    return r_a, r_b, suma1/cont if cont else 0, suma2/cont if cont else 0

def similitud(user_a, user_b):
    val1 = devolver_valoraciones_usuario(user_a)
    val2 = devolver_valoraciones_usuario(user_b)
    if not val1 or not val2:
        return 0
    r_a, r_b, r_a_med, r_b_med = calcular_media(val1, val2)
    if len(r_a) < 2:
        return 0  # Penalización por pocos elementos comunes

    num, den1, den2 = 0, 0, 0
    for i in range(len(r_a)):
        num += (r_a[i] - r_a_med) * (r_b[i] - r_b_med)
        den1 += (r_a[i] - r_a_med)**2
        den2 += (r_b[i] - r_b_med)**2

    return num / (math.sqrt(den1) * math.sqrt(den2)) if den1 and den2 else 0

def calcular_similitudes(viajes):
    usuarios = obtener_usuarios(viajes)
    matriz = {}
    for i in usuarios:
        matriz[i] = {}
        for j in usuarios:
            if i != j:
                matriz[i][j] = similitud(i, j)
    return matriz

def usuarios_parecidos(usuario, umbral, similitudes):
    return [u for u, sim in similitudes[usuario].items() if sim >= umbral]

def devolver_destinos_sin_valorar(viajes, destinos):
    faltantes = []
    for idx, v in enumerate(viajes):
        for d in destinos:
            if d not in v['valoraciones']:
                faltantes.append({'usuario': v['usuario'], 'posicion': idx, 'destino': d})
    return faltantes

def predecir(viajes, destinos, similitudes):
    faltantes = devolver_destinos_sin_valorar(viajes, destinos)
    for falta in faltantes:
        usuario = falta['usuario']
        destino = falta['destino']
        pos = falta['posicion']
        suma_sim, suma_ponderada = 0, 0
        for otro, sim in similitudes[usuario].items():
            val_otro = devolver_valoraciones_usuario(otro)
            if destino in val_otro:
                suma_ponderada += sim * val_otro[destino]
                suma_sim += abs(sim)
        prediccion = suma_ponderada / suma_sim if suma_sim else 3
        viajes[pos].setdefault('predicciones', {})[destino] = round(prediccion, 2)

def recomendar_destinos(usuario, viajes):
    for v in viajes:
        if v['usuario'] == usuario:
            return sorted(v.get('predicciones', {}).items(), key=lambda x: -x[1])
    return []

def explicar_recomendacion(usuario, destino, similitudes):
    similares = sorted(similitudes[usuario].items(), key=lambda x: -x[1])
    razon = []
    for otro, sim in similares:
        valor = devolver_valoraciones_usuario(otro).get(destino)
        if valor:
            razon.append(f"{otro} valoró {destino} con {valor}")
    return razon[:3] if razon else ["No hay explicación disponible"]

def guardar_viajes(viajes, filename="viajes.json"):
    with open(filename, 'w') as f:
        json.dump(viajes, f, indent=4)

def cargar_viajes(filename="viajes.json"):
    with open(filename, 'r') as f:
        return json.load(f)

# Funciones de visualización
def mostrar_matriz_similitud(similitudes):
    df = pd.DataFrame(similitudes).fillna(0)
    plt.figure(figsize=(8,6))
    sns.heatmap(df, annot=True, cmap="coolwarm", square=True)
    plt.title("Matriz de Similitud entre Usuarios")
    plt.show()

def mostrar_predicciones_global(viajes):
    datos = []
    for v in viajes:
        if "predicciones" in v:
            for destino, puntuacion in v["predicciones"].items():
                datos.append({"usuario": v["usuario"], "destino": destino, "puntuacion": puntuacion})
    df = pd.DataFrame(datos)
    plt.figure(figsize=(10,6))
    sns.barplot(data=df, x="destino", y="puntuacion", hue="usuario")
    plt.title("Predicciones de puntuaciones por destino y usuario")
    plt.ylim(0, 5)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def actualizar_predicciones_para_todos(viajes, similitudes):
    destinos = ["DUBAI", "PUNTA CANA", "DISNEYLAND PARIS", "SANTIAGO", "FORMIGAL"]
    predecir(viajes, destinos, similitudes)

# === EJECUCIÓN ===
usuarios = obtener_usuarios(viajes)
similitudes = calcular_similitudes(viajes)
actualizar_predicciones_para_todos(viajes, similitudes)

# Mostrar diccionario completo con predicciones
print("\nDICCIONARIO COMPLETO DE VIAJES (con predicciones):")
pprint(viajes)

# Mostrar recomendaciones por usuario
print("\nRECOMENDACIONES POR USUARIO:")
for u in usuarios:
    print(f"\nUsuario: {u}")
    recomendaciones = recomendar_destinos(u, viajes)
    for destino, pred in recomendaciones:
        print(f"  Recomiendo {destino} (predicción: {pred})")
        razones = explicar_recomendacion(u, destino, similitudes)
        for r in razones:
            print(f"     → {r}")

# Mostrar visualizaciones
mostrar_matriz_similitud(similitudes)
mostrar_predicciones_global(viajes)
