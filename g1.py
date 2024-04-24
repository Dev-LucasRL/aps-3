import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
import time

def conectar_ao_banco():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='pamonha',
            database='aps3',
            port=3307
        )
        return connection
    except Error as e:
        print(f"Erro na conexão ao banco de dados: {e}")
        return None

def post_existe(cursor, title):
    cursor.execute("SELECT * FROM posts WHERE titulo = %s", (title,))
    return cursor.fetchone() is not None


def extrair_informacoes_mongabay():
    url = 'https://brasil.mongabay.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article', class_='post-news')

    posts = []
    for article in articles:
        title_element = article.find('h2', class_='post-title-news').find('a')
        if title_element:
            title = title_element.text.strip()
            link = title_element['href']
            if not post_existe(cursor, title):
                posts.append({'Título': title, 'Link': link})

    return posts

def extrair_informacoes_g1():
    url = 'https://g1.globo.com/meio-ambiente/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('div', class_='feed-post-body')

    posts = []
    for article in articles:
        title_element = article.find('a', class_='feed-post-link')
        if title_element:
            title = title_element.text.strip()
            link = title_element['href']
            if not post_existe(cursor, title):
                posts.append({'Título': title, 'Link': link})

    return posts

def extrair_informacoes_cnn():
    url = 'https://www.cnnbrasil.com.br/tudo-sobre/meio-ambiente/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', class_='home__list__tag')

    posts = []
    for article in articles:
        title_element = article.find('h3', class_='news-item-header__title market__new__title')
        if title_element:
            title = title_element.text.strip()
            link = article['href']
            if not post_existe(cursor, title):
                posts.append({'Título': title, 'Link': link})

    return posts

def extrair_informacoes_bbc():
    url = 'https://www.bbc.com/portuguese/topics/c5qvpqj1dy4t'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('li', class_='bbc-t44f9r')

    posts = []
    for article in articles:
        title_element = article.find('a')
        if title_element:
            title = title_element.text.strip()
            link = title_element['href']
            if not post_existe(cursor, title):
                posts.append({'Título': title, 'Link': link})

    return posts

connection = conectar_ao_banco()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        titulo VARCHAR(255) NOT NULL,
        link VARCHAR(255) NOT NULL
    )
""")

while True:
    posts_mongabay = extrair_informacoes_mongabay()
    for post in posts_mongabay:
        cursor.execute("INSERT INTO posts (titulo, link) VALUES (%s, %s)", (post['Título'], post['Link']))

    posts_g1 = extrair_informacoes_g1()
    for post in posts_g1:
        cursor.execute("INSERT INTO posts (titulo, link) VALUES (%s, %s)", (post['Título'], post['Link']))

    posts_cnn = extrair_informacoes_cnn()
    for post in posts_cnn:
        cursor.execute("INSERT INTO posts (titulo, link) VALUES (%s, %s)", (post['Título'], post['Link']))

    posts_bbc = extrair_informacoes_bbc()
    for post in posts_bbc:
        cursor.execute("INSERT INTO posts (titulo, link) VALUES (%s, %s)", (post['Título'], post['Link']))

    connection.commit()
    print('Dados salvos com sucesso no banco de dados MySQL.')

    time.sleep(3600)  # Aguarda 10 minutos antes da próxima execução

cursor.close()
connection.close()
