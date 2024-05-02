import mysql.connector

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pamonha',
    database='aps3',
    port=3307
)
cursor = conexao.cursor()

# Lista de palavras boas e ruins
palavras = [
    ("bom", "desmatamento"),
    ("ótimo", "poluição"),
    ("positivo", "desperdício"),
    ("preservação", "contaminação"),
    ("renaturalização", "degradação"),
    ("energia limpa", "extinção"),
    ("proteção ambiental", "aquecimento global"),
    ("regeneração", "efeito estufa"),
    ("bem-estar animal", "exploração"),
    ("consciência ecológica", "inundação"),
    ("conservacionismo", "desflorestamento"),
    ("preservação da água", "calor"),
    ("desenvolvimento sustentável", "alagamento"),
    ("ecologia", "extinguir"),
    ("resgatar","predatória"),
    ("proteção","alagamentos"),
    ("ensinar","prejuízos"),
    ("esperança","alerta")

]

for palavra in palavras:
    cursor.execute("INSERT INTO palavras (palavra_boa, palavra_ruim) VALUES (%s, %s)", palavra)

conexao.commit()

cursor.close()
conexao.close()