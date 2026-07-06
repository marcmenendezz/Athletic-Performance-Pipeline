import funciones_adquisicion as f_a
import pandas as pd
import ast

### EJECUCION PRINCIPAL ###

datos, atletas_info, ciudades_info = f_a.extraccion("Hombre", "Velocidad", "100m", "2025")

comunidades_marcas_renta = f_a.search_ine(datos) 

# Al ejecutar esta función, no se debe salir de la pestaña, para evitar pop-ups
# de anuncios aleatorios que produzcan errores.
ciudades_marcas_altura = f_a.obtener_altura(ciudades_info)


# Aquí sacamos un .txt de cada resultado para utilizar en los sockets
try:
    with open("comunidades_marca_renta.txt", "w") as archivo:
        archivo.write(f"{comunidades_marcas_renta}")
except:
    pass

try:
    with open("atletas_info.txt", "w") as archivo:
        archivo.write(f"{atletas_info}")
except:
    pass

try:
    with open("ciudades_marcas_altura.txt", "w") as archivo:
        archivo.write(f"{ciudades_marcas_altura}")
except:
    pass

# 1. Leer el contenido del archivo .txt
with open('atletas_info.txt', 'r') as f:
    contenido = f.read()

# 2. Convertir el texto (string) en un diccionario real de Python
# Usamos ast.literal_eval porque es más seguro que eval()
diccionario = ast.literal_eval(contenido)

# 3. Convertir el diccionario a un DataFrame de Pandas
# Si el diccionario es simple {llave: valor}, usa orient='index'
df = pd.DataFrame.from_dict(diccionario, orient='index')

# 4. Guardar a Excel
df.to_excel('resultado_atletas.xlsx', header=False) 



coeficiente = f_a.calcular_correlacion_R_riqueza(comunidades_marcas_renta)
f_a.grafico_renta_marcas(comunidades_marcas_renta)

coeficiente2 = f_a.calcular_correlacion_R_altura(ciudades_marcas_altura)
f_a.grafico_altura_marcas(ciudades_marcas_altura)