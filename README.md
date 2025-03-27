📚  📚  📚  📚 <h1>Generador de Cuentos</h1> 📚  📚  📚  📚

🔽 🔽 🔽Este es el UML de la aplicación a desarrollar. 🔽 🔽 🔽


[UML_GeneradorDeCuentos.pdf](https://github.com/user-attachments/files/18738338/UML_GeneradorDeCuentos.pdf)
<h3><n>Descripción:</n></h3>
<p>Creación de historias cortas a partir de un dibujo usando IA</p>


<h2>🥤 Antes de empezar... </h2>
Lo ideal seía tener un contenedor de Docker, pero vamos a hacer todo como si no existiese esa posibilidad

<h2> 🚀 Pasos para clonar y ejecutar </h2>
<h3>Clonar el repositorio</h3>

```bash
git clone ESTE-REPOSITORIO
```

<h3>💻 Configurar un entorno virtual</h3>

```bash
python -m venv venv
source venv/bin/activate #Linux o max
venv\Scripts\activate # Windows al poder >:)
```

<h3>🔀 Instalar dependencias</h3>

```bash
pip install -r requirements.txt
```

<h3>🔩 Configurar las variables de entorno</h3>
Crea un archivo .env en la raiz y pon lo siguiente:

```bash
SEGMIND_API_KEY= clave-modelo
SEGMIND_URL_IMG= modelo-img-url
SEGMIND_URL_VOICE= modelo-voice-url
OPENAI_API_KEY= clave-modelo
OPENAI_URL= url-modelo-texto
```
<h3>🏎️ Ejecutar el backend y el frontend</h3>

Consola #1(en la raiz):

```bash
python __main__.py
```

Consola #2(en front):

```bash
cd frontend
streamlit run __main_.py
```


