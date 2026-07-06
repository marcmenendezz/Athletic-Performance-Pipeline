import time
import collections
import pandas as pd 
import seaborn as sns 
from selenium import webdriver
import matplotlib.pyplot as plt
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def extraccion(sexo, sector, prueba, temporada):

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://atletismorfea.es")

    aceptar = driver.find_element(By.XPATH, "//*[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']")

    aceptar.click()
    time.sleep(3)

    if driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/button"):
        driver.find_element(By.XPATH, "/html/body/div[6]/div[1]/button").click()
        time.sleep(3)

    ranking = driver.find_element(By.CSS_SELECTOR, "a.ranking-menu")
    ranking.click()
    time.sleep(4)
    
    #temporada
    lista_temps = driver.find_element(By.ID, "edit-season")
    selector0 = Select(lista_temps)
    selector0.select_by_visible_text(temporada)
    time.sleep(2)

    #sexo
    lista_sexos = driver.find_element(By.ID, "edit-gender")
    selector1 = Select(lista_sexos)
    selector1.select_by_visible_text(sexo)
    time.sleep(2)

    #sector
    lista_sectores = driver.find_element(By.XPATH, "//*[@id='edit-type']")
    selector2 = Select(lista_sectores)
    selector2.select_by_visible_text(sector)
    time.sleep(2)
    
    #prueba
    lista_pruebas = driver.find_element(By.ID, "edit-event")
    selector3 = Select(lista_pruebas)
    selector3.select_by_visible_text(prueba)
    time.sleep(2)

    #ranking
    ver_ranking = driver.find_element(By.XPATH, "//*[@id='edit-button']")  
    ver_ranking.click()
    time.sleep(7)

    #todas
    lista_tops = driver.find_element(By.XPATH, "//*[@id='ranking_container']/div[1]/div/select")
    selector4 = Select(lista_tops) 
    selector4.select_by_visible_text('Todas')
    time.sleep(7)

    while True:
        try:
            cargar_mas = driver.find_element(By.CLASS_NAME,"ranking-pager-link")
            cargar_mas.click()
            time.sleep(8)
        except:
            break
    
    
    tabla = driver.find_element(By.CLASS_NAME, "bloque_tabla_ranking").get_attribute("outerHTML")
    
    def comunidades(tabla):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(tabla, 'html.parser') 
        filas = soup.find_all('tr')[1:]
        dic = {}
        for fila in filas:
            celdas = fila.find_all('td')
            comunidad = celdas[7].get_text(strip=True)
            marca = float(celdas[1].get_text(strip=True))
            if comunidad in dic:
                dic[comunidad].append(marca)
            else:
                dic[comunidad] = [marca]
        
        return dic 
    
    def atletas(tabla):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(tabla, 'html.parser') 
        filas = soup.find_all('tr')[1:]
        dic = {}
        for fila in filas:
            celdas = fila.find_all('td')
            atleta = celdas[3].get_text(strip=True)
            ranking, marca, viento, club, fn, pais, fed, pos, ciudad, fecha = celdas[0].get_text(strip=True), celdas[1].get_text(strip=True), celdas[2].get_text(strip=True), celdas[4].get_text(strip=True), celdas[5].get_text(strip=True), celdas[6].get_text(strip=True), celdas[7].get_text(strip=True), celdas[8].get_text(strip=True), celdas[9].get_text(strip=True), celdas[10].get_text(strip=True)
            if atleta not in dic:
                dic[atleta] = (ranking, marca, viento, club, fn, pais, fed, pos, ciudad, fecha)
        return dic
    
    datos = comunidades(tabla)
    atletas_info = atletas(tabla)

    # Diccionario con las ciudades de las primeras 500 marcas: 
    def ciudad_marca(atletas_info):
        ciudades_info = collections.defaultdict(list)
        i = 0
        for atleta, info in atletas_info.items():
            if i < 500:
                ciudad = info[8]
                marca = info[1]
                ciudades_info[ciudad].append(marca)   
                i+=1
            else:
                break

        return ciudades_info

    ciudades_info = ciudad_marca(atletas_info)

    return datos, atletas_info, ciudades_info


def search_ine(datos):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.ine.es/")

    time.sleep(3)

    #comprobar pop-up molesto (felicitación de Navidad en el momento de hacerlo)
    try:
        driver.find_element(By.XPATH, "//button[@aria-label='Cerrar']")
        cerrar = driver.find_element(By.XPATH, "//button[@aria-label='Cerrar']")
        cerrar.click()
        time.sleep(3)
    except:
        pass
    
    #cookies
    aceptar = driver.find_element(By.XPATH, "//*[@id='aceptarCookie']")
    aceptar.click()
    time.sleep(3)
    
    #temas
    ipc = driver.find_element(By.XPATH, "//*[@id='temas']/div/nav/ul/li[8]/a/img")
    ipc.click()
    time.sleep(3)
    
    #condiciones de vida
    desplegable = driver.find_element(By.XPATH, "//span[normalize-space()='Condiciones de vida']")
    desplegable.click()
    time.sleep(3)

    #calidad de vida
    calidad_vida = driver.find_element(By.XPATH, '//*[@id="header_1254735976608_1254736176936"]/a')
    calidad_vida.click()
    time.sleep(3)

    #condiciones materiales
    driver.switch_to.window(driver.window_handles[-1]) # Nueva pestaña abierta
    materiales = driver.find_element(By.XPATH, "//*[contains(text(), 'Condiciones materiales de vida')]")
    materiales.click()
    time.sleep(3)

    #condiciones economicas
    economicas = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[3]/div/section/div/article[1]/div/table/tbody/tr/td[2]/a')
    economicas.click()
    time.sleep(3)

    
    desplegable2 = driver.find_element(By.XPATH, '//*[@id="c_11281"]')
    desplegable2.click()
    time.sleep(3)
    
    renta = driver.find_element(By.XPATH, '//*[@id="t_68338"]')
    renta.click()
    time.sleep(3)

    renta_m = driver.find_element(By.XPATH, '//*[@id="cri144489"]/option[2]')
    renta_m.click()
    time.sleep(3)

    def normalizar_coms(datos):
        mapping = {
            'AND': 'Andalucía',
            'ARA': 'Aragón',
            'AST': 'Asturias, Principado de',
            'BAL': 'Balears, Illes',
            'CNR': 'Canarias',
            'CAN': 'Cantabria',
            'CLM': 'Castilla - La Mancha',
            'CYL': 'Castilla y León',
            'CAT': 'Cataluña',
            'MAD': 'Madrid, Comunidad de',
            'CVA': 'Comunitat Valenciana',
            'EXT': 'Extremadura',
            'GAL': 'Galicia',
            'RIO': 'Rioja, La',
            'NAV': 'Navarra, Comunidad Foral de',
            'PVA': 'País Vasco',
            'MUR': 'Murcia, Región de'
        }
        normalized_data = {}
        for com, values in datos.items():
            if com in mapping:
                normalized_name = mapping.get(com, com)
                normalized_data[normalized_name] = values
        return normalized_data

    datos_normalizados = normalizar_coms(datos)

    
    select_todos = driver.find_element(By.XPATH, '//*[@id="tg142940"]/div/fieldset/div[2]/button[1]/i')
    select_todos .click()
    time.sleep(3)
    
    consultar = driver.find_element(By.XPATH, '//*[@id="botonConsulSele"]')
    consultar .click()
    time.sleep(3)

    tabla = driver.find_element(By.XPATH, '//*[@id="tabs"]')

    def datos_tabla(tabla):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(tabla, 'html.parser') 
        filas = soup.find_all('tr')[3:19]
        for fila in filas:
            comunidades = fila.find_all('th')
            riquezas = fila.find_all('td')
            com = comunidades[0].get_text(strip=True)
            ric = riquezas[0].get_text(strip=True)
            com_real = com[3:]
            datos_normalizados[com_real]= (datos_normalizados[com_real], ric)
        return datos_normalizados
    
    html_de_la_tabla = tabla.get_attribute('outerHTML')
    comunidad_marcas_renta = datos_tabla(html_de_la_tabla)

    return comunidad_marcas_renta 


def obtener_altura(ciudades_info): 
    alturas = {}
    web = "https://coordinates-converter.com/es/altimetro"
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(web)
    time.sleep(3) 
    
    # cookies
    try:
        aceptar = driver.find_element(By.CLASS_NAME, 'fc-button-label')
        aceptar.click()
        time.sleep(1)
    except:
        pass
    
    for ciudad, info in ciudades_info.items():

        buscador = driver.find_element(By.ID, 'geo-keyword')
        buscador.clear() # limpiar el buscador 
            
        # escribir y buscar la ciudad
        buscador.send_keys(ciudad)
        time.sleep(1)
        
        clicker = driver.find_element(By.XPATH, '//*[@id="contentcontainer"]/div[3]/div/div[2]/div/div[1]/div[2]/div[1]')
        clicker.click()
        
        time.sleep(3) 
        
        altura = driver.find_element(By.XPATH, '//*[@id="contentcontainer"]/div[3]/div/div[2]/div/div[1]/div[4]/div/div/div[2]/div').text
        altura = int(altura.split()[0])
        alturas[ciudad] = (info, altura)

    return alturas


def calcular_correlacion_R_riqueza(riquezas):
    datos_limpios = []
    
    for com, info in riquezas.items():

        if not isinstance(info, (tuple, list)):
            continue

        renta = info[1]
        try:
            if isinstance(renta, str):
                renta = float(renta.replace('.', '').replace(',', '.'))
            else:
                renta = float(renta)
        except:
            continue
    
        lista_marcas = info[0]
 
        if isinstance(lista_marcas, (list, tuple)):
            tiempos = [float(m) for m in lista_marcas if isinstance(m, (int, float))]
            if tiempos:
                marca_media = sum(tiempos)/len(tiempos) 
                datos_limpios.append({'Comunidad': com, 'Renta': renta, 'Marca_Media': marca_media })

    df = pd.DataFrame(datos_limpios)

    coeficiente = df['Renta'].corr(df['Marca_Media'])
    print(f"\n--- Análisis Estadístico - Riqueza---")
    print(f"Resultado del Coeficiente de Pearson: {coeficiente:.4f}")
    return coeficiente


def grafico_renta_marcas(riquezas):
    filas = []
    for com, info in riquezas.items():

        if not isinstance(info, (tuple, list)):
            continue

        lista_marcas = info[0]
        renta = info[1]
        
        if isinstance(renta, str):
            renta_limpia = float(renta.replace('.', '').replace(',', '.'))
        else:
            renta_limpia = float(renta)
            
        if isinstance(lista_marcas, (list, tuple)):
            tiempos = [float(m) for m in lista_marcas]
            if tiempos:
                marca_media = sum(tiempos) / len(tiempos) # Usamos marca media para el gráfico
                filas.append({'Comunidad': com, 'Renta': renta_limpia, 'Marca_Media': marca_media})
    
    df = pd.DataFrame(filas)

    sns.set_theme(style="whitegrid", context="talk")
    plt.figure(figsize=(15, 10))
    
    sns.regplot(data=df, x='Renta', y='Marca_Media', ci=None, scatter=False, 
                line_kws={'color': '#e74c3c', 'linewidth': 3, 'linestyle': '--'})

    sns.scatterplot(data=df, x='Renta', y='Marca_Media', hue='Comunidad', 
                    palette='viridis', s=250, edgecolor='white', linewidths=2)

    for i in range(len(df)):
        plt.text(df.iloc[i]['Renta'] + 50, df.iloc[i]['Marca_Media'], 
                 df.iloc[i]['Comunidad'], fontsize=10, fontweight='bold')

    plt.title('Relación: Renta Media vs Marca Media', fontsize=22, fontweight='bold')
    plt.gca().invert_yaxis() # Invertir eje Y: tiempos bajos arriba
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.tight_layout()


def calcular_correlacion_R_altura(alturas):
    
    datos_limpios = []
    
    for ciudad, info in alturas.items():
        altura = info[1]
        marcas_list = info[0]
        tiempos = [float(m) for m in marcas_list]
        if tiempos:
            marca_media = sum(tiempos) / len(tiempos)
            datos_limpios.append({
                'Ciudad': ciudad, 
                'Altitud': float(altura), 
                'Marca_Media': marca_media
            })

    df = pd.DataFrame(datos_limpios)

    coeficiente = df['Altitud'].corr(df['Marca_Media'])
    
    print(f"\n--- Análisis Estadístico - Altura ---")
    print(f"Resultado del Coeficiente de Pearson: {coeficiente:.4f}")
    return coeficiente


def grafico_altura_marcas(alturas):
    filas = []
    for ciudad, info in alturas.items():
        if not isinstance(info, (tuple, list)) or len(info) < 2:
            continue

        marcas_lim = info[0]
        altura = info[1]
            
        try:
            tiempos = [float(m) for m in marcas_lim]
            if tiempos:
                marca_media = sum(tiempos) / len(tiempos)
                filas.append({'Ciudad': ciudad, 'Altitud': float(altura), 'Marca_Media': marca_media})
        except:
            continue
    
    df = pd.DataFrame(filas)

    sns.set_theme(style="whitegrid", context="talk")
    plt.figure(figsize=(15, 10))
    
    sns.regplot(data=df, x='Altitud', y='Marca_Media', ci=None, scatter=False, 
                line_kws={'color': '#27ae60', 'linewidth': 3, 'linestyle': '--'})

    sns.scatterplot(data=df, x='Altitud', y='Marca_Media', hue='Ciudad', 
                    palette='magma', s=250, edgecolor='white', linewidths=2, alpha=0.9)

    if len(df) < 50:
        for i in range(len(df)):
            plt.text(df.iloc[i]['Altitud'] + 5, df.iloc[i]['Marca_Media'], 
                     df.iloc[i]['Ciudad'], fontsize=8, va='center')

    plt.title('Relación: Altitud vs Marca Media', fontsize=22, fontweight='bold', pad=20)
    plt.xlabel('Altitud sobre el nivel del mar (m)', fontsize=14)
    plt.ylabel('Marca Media', fontsize=14)

    plt.gca().invert_yaxis() 

    plt.gca().get_legend().remove()
    sns.despine()
    plt.tight_layout()
    plt.show()
    plt.tight_layout()