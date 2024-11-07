import json
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from pathlib import Path
from datetime import date
import time

from entities.colloquium import Colloquium
from entities.speaker import Speaker


# Substitua 'caminho_do_arquivo_json' pelo caminho do seu arquivo JSON
caminho_do_arquivo_json = 'C:\\Users\\junio\\OneDrive\\Documentos\\GitHub\\gerador_de_certificados\\datas\\datas.json'

# Ler o arquivo JSON
with open(caminho_do_arquivo_json, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Imprimir o evento de cada entrada no JSON
colloquiums = []
for entry in data:
    colloquiums.append(
        Colloquium(
            date=entry['date'],
            name=entry['event'],
            speakers = [Speaker(**speaker) for speaker in entry['speakers']]
        )
    )


# Inicializa o driver do Chrome
webBrowser = webdriver.Chrome()
webBrowser.get('https://www.cct.udesc.br/formularios.php?idFormulario=61')

# --- PREENCHENDO O FORMULÁRIO ----

timeDelay = 0

for colloquium in colloquiums :
    # Nome do Evento
    webBrowser.find_element(By.ID, "texto[2]").send_keys(colloquium.name)
    time.sleep(timeDelay)

    # Variação (checkbox)
    checkbox = webBrowser.find_element(By.ID, "checkbox[36][2]")
    if not checkbox.is_selected():
        checkbox.click()
    time.sleep(timeDelay)

    # Modalidade
    webBrowser.find_element(By.ID, "texto[6]").send_keys("Palestra")
    time.sleep(timeDelay)

    # Data Inicial
    webBrowser.find_element(By.ID, "texto[8]").send_keys(colloquium.date)
    time.sleep(timeDelay)

    # Data Final
    webBrowser.find_element(By.ID, "texto[9]").send_keys(colloquium.date)
    time.sleep(timeDelay)

    # Título
    webBrowser.find_element(By.ID, "texto[12]").send_keys("Certificado")
    time.sleep(timeDelay)

    # Primeira Linha
    webBrowser.find_element(By.ID, "texto[14]").send_keys("Certificamos que")
    time.sleep(timeDelay)

    # Texto do Certificado
    webBrowser.find_element(By.ID, "textoArea[16]").send_keys(f'Ministrou a palestra no Colóquio da Computação intitulado "{colloquium.name}", {colloquium.formatar_data()}, com uma contribuição de 1 hora para o evento.')
    time.sleep(timeDelay)

    # Data de Emissão
    webBrowser.find_element(By.ID, "texto[18]").send_keys("19/11/2023")
    time.sleep(timeDelay)

    # Cidade
    webBrowser.find_element(By.ID, "texto[20]").send_keys("Joinville")
    time.sleep(timeDelay)

    # Local
    webBrowser.find_element(By.ID, "texto[21]").send_keys("UDESC- Centro de Ciências")
    time.sleep(timeDelay)

    # Coordenadora dos Colóquios
    webBrowser.find_element(By.ID, "texto[23]").send_keys("Profa. Karina Girardi Roggia")
    time.sleep(timeDelay)

    # Coordenadora dos Colóquios
    webBrowser.find_element(By.ID, "texto[24]").send_keys("Coordenadora do Programa de Extensão")
    time.sleep(timeDelay)

    # Modelo de certificado (upload de arquivo)
    webBrowser.find_element(By.ID, "arquivo[35]").send_keys(r"C:\Users\junio\OneDrive\Documentos\GitHub\gerador_de_certificados\model\modelo.pdf")
    time.sleep(timeDelay)

    elemento_encontrado = False
    while not elemento_encontrado:
        try:
            # Tenta encontrar o elemento pelo ID
            elemento = webBrowser.find_element(By.ID, "caixaMensagem")
            elemento_encontrado = True  # Se encontrou, sair do loop
            print(f"\nEnviou formulario do Coloquio: {colloquium.name}\n")
        except NoSuchElementException:
            # Se o elemento não estiver presente, espere um pouco e tente novamente
            print("Esperando enviar...")
            time.sleep(1)  # Espera por 1 segundo antes de tentar novamente

    webBrowser.get('https://www.cct.udesc.br/formularios.php?idFormulario=61')
    time.sleep(1)    


# Fecha o navegador
webBrowser.quit()
