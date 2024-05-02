import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pamonha',
    database='aps3',
    port=3307
)
cursor = conexao.cursor()

consulta = "SELECT palavra_boa, palavra_ruim FROM palavras"
cursor.execute(consulta)
palavras = cursor.fetchall()

# Separa as palavras em listas de palavras boas e ruins
palavras_boas = [palavra[0] for palavra in palavras if palavra[0] is not None]
palavras_ruins = [palavra[1] for palavra in palavras if palavra[1] is not None]

def calcular_saldo_palavras(texto):
    saldo = 0
    for palavra in texto.split():
        if palavra.lower() in palavras_boas:
            saldo += 1
        elif palavra.lower() in palavras_ruins:
            saldo -= 1
    return saldo

consulta_titulos = "SELECT titulo FROM posts"
cursor.execute(consulta_titulos)
titulos = cursor.fetchall()

for titulo in titulos:
    titulo_noticia = titulo[0]
    saldo_palavras = calcular_saldo_palavras(titulo_noticia)
    if saldo_palavras > 0:
        classificacao = "boa"
    elif saldo_palavras < 0:
        classificacao = "ruim"
    else:
        classificacao = "neutra"
    print(f"O saldo das palavras no título '{titulo_noticia}' é: {saldo_palavras}. A notícia é classificada como: {classificacao}")

cursor.close()
conexao.close()