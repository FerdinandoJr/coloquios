import json

from entities.colloquium import Colloquium
from entities.speaker import Speaker

# Substitua 'caminho_do_arquivo_json' pelo caminho do seu arquivo JSON
caminho_do_arquivo_json = 'C:\\Users\\junio\\Documents\\certificados\\datas\\datas.json'

# Ler o arquivo JSON
with open(caminho_do_arquivo_json, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Imprimir o evento de cada entrada no JSON
for entry in data:
    colloquium = Colloquium(
        date=entry['date'],
        name=entry['event'],
        speakers = [Speaker(**speaker) for speaker in entry['speakers']]
    )

    print(colloquium.speakers[0].cpf)