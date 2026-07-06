# Athletic Performance Pipeline 🏃‍♂️📊

Proyecto integral de Ciencia de Datos enfocado en el análisis del rendimiento deportivo en la prueba de **100 metros lisos** en la categoría masculina a nivel absoluto. Este proyecto explora la posible correlación entre el rendimiento de los atletas y factores externos como el poder adquisitivo de sus comunidades autónomas y la altitud de las ciudades donde compiten.

## 🚀 Arquitectura del Proyecto

El proyecto implementa un *pipeline* completo de datos:
1. **Adquisición:** Web Scraping automatizado de la web oficial de la RFEA (Real Federación Española de Atletismo) e INE mediante Selenium y BeautifulSoup.
2. **Procesamiento:** Limpieza y normalización de datos utilizando OpenRefine y Pandas.
3. **Análisis:** Análisis estadístico mediante correlaciones de Pearson con Seaborn y Matplotlib.
4. **Distribución:** Sistema Cliente-Servidor basado en Sockets TCP para realizar consultas sobre la base de datos resultante.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.11
* **Web Scraping:** Selenium, BeautifulSoup4
* **Análisis de Datos:** Pandas, Seaborn, Matplotlib, NumPy
* **Arquitectura:** Sockets TCP (Python `socket` library)

## 📈 Hallazgos Principales
**Relación Riqueza-Rendimiento** (r = -0.3229): Se observa una correlación negativa moderada, sugiriendo que comunidades con mayor renta per cápita tienden a presentar marcas de tiempo ligeramente inferiores (mejor rendimiento).

**Relación Altitud-Rendimiento** (r = 0.0676): No existe una relación lineal significativa entre la altitud de la ciudad y el rendimiento en la prueba de 100 metros lisos.

## ⚙️ Instrucciones de Ejecución
Requisitos: Asegúrate de tener instalado Python 3.x y las dependencias:

    pip install pandas seaborn selenium beautifulsoup4 matplotlib

  - Ejecución del Pipeline:

    Para procesar los datos, ejecuta el orquestador principal:

        python src/main.py

  - Sistema de Consultas (TCP):

    Inicia primero el servidor: 

        python src/servidorTCP.py

    En otra terminal, realiza consultas:

        python src/clienteTCP.py
