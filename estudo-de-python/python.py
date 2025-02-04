import requests
from bs4 import BeautifulSoup
import csv

def coletar_dados_produto(nome_produto, url_produto):
    response = requests.get(url_produto)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')

        price_elements = soup.find_all('span', class_='a-price-whole') # Substitua pela classe real do elemento
        precos = []
        for price_element in price_elements:
            price_text = price_element.get_text()
            cleaned_price = price_text.strip().replace('\n', '')
            precos.append(cleaned_price)
        

        return nome_produto, url_produto, precos
    else:
        print(f"Erro ao acessar a página do produto {nome_produto}")
        return None

def analisar_precos(produtos):
    with open('precos.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Nome', 'Link', 'Preço'])
        
        for produto in produtos:
            nome_produto, url_produto = produto['nome'], produto['url']
            dados_produto = coletar_dados_produto(nome_produto, url_produto)
            if dados_produto:
                nome, url, precos = dados_produto
                for preco in precos:
                    writer.writerow([nome, url, preco])
                    print(f"Preço do {nome}: {preco}")
            else:
                print(f"Não foi possível coletar os dados do produto {nome_produto}")

produtos = [
    {'nome': 'Placa de Vídeo RTX 4070', 'url': 'https://www.amazon.com.br/s?k=rtx+4070&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=24I9786RIPKCV&sprefix=rtx+407%2Caps%2C194&ref=nb_sb_noss_2'}
]

# Análise dos preços
analisar_precos(produtos)
