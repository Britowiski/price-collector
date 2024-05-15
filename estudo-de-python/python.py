import requests
from bs4 import BeautifulSoup
import csv

def coletar_dados_produto(nome_produto, url_produto):
    # Fazendo uma solicitação GET para a página do produto
    response = requests.get(url_produto)
    
    # Verificando se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Parseando o conteúdo HTML da página
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrando todos os elementos que contêm o preço do produto
        price_elements = soup.find_all('span', class_='a-price-whole') # Substitua pela classe real do elemento
        
        # Lista para armazenar os preços
        precos = []
        
        # Iterando sobre os elementos de preço
        for price_element in price_elements:
            # Extraindo o texto do elemento
            price_text = price_element.get_text()
            # Limpando o texto para remover espaços em branco extras e caracteres indesejados
            cleaned_price = price_text.strip().replace('\n', '')
            # Adicionando o preço à lista de preços
            precos.append(cleaned_price)
        
        # Retornar o nome do produto, o link e a lista de preços
        return nome_produto, url_produto, precos
    else:
        print(f"Erro ao acessar a página do produto {nome_produto}")
        return None

def analisar_precos(produtos):
    # Abrir o arquivo CSV em modo de escrita
    with open('precos.csv', mode='w', newline='', encoding='utf-8') as file:
        # Criar um escritor CSV
        writer = csv.writer(file)
        # Escrever o cabeçalho
        writer.writerow(['Nome', 'Link', 'Preço'])
        
        # Iterar sobre os produtos
        for produto in produtos:
            nome_produto, url_produto = produto['nome'], produto['url']
            # Coletar os dados do produto
            dados_produto = coletar_dados_produto(nome_produto, url_produto)
            if dados_produto:
                # Desempacotar os dados do produto
                nome, url, precos = dados_produto
                # Iterar sobre os preços e escrever no arquivo CSV
                for preco in precos:
                    writer.writerow([nome, url, preco])
                    print(f"Preço do {nome}: {preco}")
            else:
                print(f"Não foi possível coletar os dados do produto {nome_produto}")

# Lista de produtos
produtos = [
    {'nome': 'Placa de Vídeo RTX 4070', 'url': 'https://www.amazon.com.br/s?k=rtx+4070&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=24I9786RIPKCV&sprefix=rtx+407%2Caps%2C194&ref=nb_sb_noss_2'}
]

# Análise dos preços
analisar_precos(produtos)
