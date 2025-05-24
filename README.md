

# Recomendador de Destinos Turísticos

Aplicación web que recomienda destinos turísticos personalizados a los usuarios, utilizando un sistema de recomendación colaborativo.

## Características

- **Login de usuarios**: Acceso seguro mediante autenticación.
- **Recomendación personalizada**: Sugerencia de destinos basada en valoraciones previas de usuarios similares.
- **Valoración de destinos**: Los usuarios pueden puntuar y actualizar sus valoraciones.
- **Chatbot básico**: Responde preguntas sencillas sobre viajes.
- **Detalle de destino**: Visualización de información y valoración de cada destino.
- **Predicción de afinidad**: El sistema indica si a un usuario probablemente le gustará un destino.

## Tecnologías utilizadas

- **Backend**: Python, Flask
- **Base de datos**: MongoDB Atlas
- **Frontend**: HTML (Jinja2), CSS
- **Librerías**: pymongo, python-dotenv, statistics, math, requests, BeautifulSoup

## Seguridad

Las credenciales sensibles, como la URI de MongoDB, se almacenan en variables de entorno usando un archivo .env y la librería `python-dotenv`.

## Estructura del repositorio

```
index.py                # Lógica principal y rutas Flask
templates/              # Plantillas HTML
static/                 # Archivos estáticos (imágenes)
sprint1/                # Código auxiliar y experimentos
uso-xpath/              # Utilidades adicionales
requirements.txt        # Dependencias del proyecto
.env                    # Variables de entorno (no subir al repositorio)
```

## Instalación y ejecución

1. Clona el repositorio.
2. Crea un archivo .env con la URI de tu base de datos MongoDB:
   ```
   MONGODB_URI=tu_uri_de_mongodb
   ```
3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
4. Ejecuta la aplicación:
   ```
   python index.py
   ```
5. Accede a `http://localhost:8000` en tu navegador.

