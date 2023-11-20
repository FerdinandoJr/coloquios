from datetime import datetime
import re
import unicodedata
from entities.speaker import Speaker

class Colloquium:
    def __init__(self, date, speakers, name):
        self.date = date
        # Ensure that speakers is a list of Speaker instances
        self.speakers = speakers if all(isinstance(s, Speaker) for s in speakers) else []
        self.name = name
        
    def get_name_format(self):
        # Normaliza a string para a forma decomposta NFD e remove os diacríticos
        texto_sem_acento = ''.join(c for c in unicodedata.normalize('NFD', self.name) if unicodedata.category(c) != 'Mn')
        # Remove caracteres especiais, exceto espaços
        texto_sem_caracteres_especiais = re.sub(r'[^\w\s]', '', texto_sem_acento)
        # Substitui espaços por underlines e converte para minúsculas
        texto_formatado = texto_sem_caracteres_especiais.replace(" ", "_").lower()
        return texto_formatado
    
    def formatar_data(self):
        # Converte a string de data no formato 'dd/mm/yyyy' para um objeto datetime
        data_obj = datetime.strptime(self.date, '%d/%m/%Y')

        # Formata a data no estilo "realizado em 30 de dezembro de 2000"
        data_formatada = data_obj.strftime('realizado em %d de %B de %Y')

        # Substituir o nome do mês em inglês pelo equivalente em português
        meses_pt = {
            'January': 'janeiro', 'February': 'fevereiro', 'March': 'março', 'April': 'abril',
            'May': 'maio', 'June': 'junho', 'July': 'julho', 'August': 'agosto',
            'September': 'setembro', 'October': 'outubro', 'November': 'novembro', 'December': 'dezembro'
        }
        for ingles, portugues in meses_pt.items():
            data_formatada = data_formatada.replace(ingles, portugues)

        # Remove o zero à esquerda do dia, se houver
        data_formatada = data_formatada.replace(' 0', ' ')

        return data_formatada
