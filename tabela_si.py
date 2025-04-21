import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL da página
url = 'https://www.infoescola.com/matematica/notacao-cientifica/'

# Faz a requisição HTTP
response = requests.get(url)
response.raise_for_status()

# Faz o parse do HTML
soup = BeautifulSoup(response.content, 'html.parser')

# Encontra a tabela no artigo
tabela = soup.find("article").find("table")
linhas = tabela.find_all("tr")

# Extrai os dados das linhas
dados = []
for linha in linhas:
    colunas = linha.find_all(['td', 'th'])
    dados_linha = [col.get_text(strip=True) for col in colunas]
    if dados_linha:
        dados.append(dados_linha)

# Encontra o índice da linha que contém a palavra "iota"
iota_index = None
for i, linha in enumerate(dados):
    if 'iota' in linha[0].lower():
        iota_index = i
        break

if iota_index is not None and len(dados) > iota_index:
    # Mantém apenas as colunas desejadas
    conteudo = [linha for linha in dados[iota_index:] if len(linha) == 4]
    dados_filtrados = [[linha[0], linha[1], linha[3]] for linha in conteudo]

    # Cria o DataFrame
    df = pd.DataFrame(dados_filtrados, columns=['nome', 'simbolo', 'equivalente_numerico'])

    # Remove espaços, troca vírgula por ponto e converte para float
    df['equivalente_numerico'] = (
        df['equivalente_numerico']
        .str.replace(' ', '')
        .str.replace(',', '.')
        .astype(float)
    )

    print(df)

    # Salva o DataFrame em um arquivo CSV
    df.to_csv('prefixos_si.csv', index=False, encoding='utf-8')