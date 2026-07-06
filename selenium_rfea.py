from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://atletismorfea.es")

def extracción(sexo, sector, prueba):
    #sexo
    lista_sexos = driver.find_element(By.ID, "edit-gender")
    selector1 = Select(lista_sexos)
    selector1.select_by_visible_text(sexo)
    time.sleep(2)

    #sector
    lista_sectores = driver.find_element(By.ID, "edit-type")
    selector2 = Select(lista_sectores)
    selector2.select_by_visible_text(sector)
    time.sleep(2)
    #prueba
    lista_pruebas = driver.find_element(By.ID, "edit-event")
    selector3 = Select(lista_pruebas)
    selector3.select_by_visible_text(prueba)
    time.sleep(2)

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
            time.sleep(10)
        except:
            break
    
    
    tabla = driver.find_element(By.CLASS_NAME, "bloque_tabla_ranking").get_attribute("outerHTML")
    def lista_comunidades(tabla):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(tabla, 'html.parser') 
        filas = soup.find_all('tr')[1:]
        dic = {}
        for fila in filas:
            celdas = fila.find_all('td')
            comunidad = celdas[7].get_text(strip=True)
            marca, viento = celdas[1].get_text(strip=True), celdas[2].get_text(strip=True)
            if comunidad in dic:
                dic[comunidad].append((marca, viento))
            else:
                dic[comunidad] = [(marca, viento)]
        
        return dic

    
    datos = lista_comunidades(tabla)
    return datos
        

aceptar = driver.find_element(by=By.XPATH, value="//*[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']")
aceptar.click()
time.sleep(2)

ranking = driver.find_element(By.CSS_SELECTOR, "a.ranking-menu")
ranking.click()


res = extracción("Hombre","Velocidad","100m")
print(res)


# Comunidades
# Altura
# Pillar tota la tabla pa lo dels sockets
# Filtrado en tota la tabla: indexs i normalitzar posicions

cont=0
for key in res:
    cont+=len(res[key])
print(cont)




