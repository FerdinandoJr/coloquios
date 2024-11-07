import json
import os
import re
from datetime import datetime
from unidecode import unidecode

def format_cpf(cpf):
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def format_date(date_str):
    return datetime.strptime(date_str, "%d/%m/%Y").strftime("%d/%m/%Y")

def gerar_txt(dados):
    # Define a pasta de saída
    pasta_saida = "eventos_txt"
    os.makedirs(pasta_saida, exist_ok=True)  # Cria a pasta se não existir
    
    for evento in dados:
        # Remove acentos e caracteres especiais do nome do evento
        nome_evento_formatado = unidecode(evento['event'].lower().replace(' ', '_'))
        nome_evento_formatado = re.sub(r'[^a-zA-Z0-9_]', '', nome_evento_formatado)
        nome_arquivo = f"{nome_evento_formatado}.txt"
        caminho_arquivo = os.path.join(pasta_saida, nome_arquivo)  # Caminho completo na pasta de saída
        
        # Formata o conteúdo
        conteudo = f"Data: {format_date(evento['date'])}\n"
        conteudo += f"Evento: {evento['event']}\n\n"
        
        conteudo += "Palestrantes:\n"
        for speaker in evento['speakers']:
            nome = speaker['name']
            nascimento = format_date(speaker['birth_date'])
            cpf = format_cpf(speaker['cpf'])
            conteudo += f"  Nome: {nome}\n"
            conteudo += f"  Data de Nascimento: {nascimento}\n"
            conteudo += f"  CPF: {cpf}\n\n"
        
        # Salva o conteúdo em um arquivo .txt
        with open(caminho_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(conteudo)
        print(f"Arquivo '{caminho_arquivo}' gerado com sucesso.")

# Carregar os dados do JSON
with open("./datas/datas.json", "r", encoding="utf-8") as file:
    dados = json.load(file)

# Gerar arquivos .txt
gerar_txt(dados)
