from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from nltk.corpus import stopwords
import mysql.connector

import nltk
nltk.download('stopwords')

stop_words = stopwords.words('portuguese')

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='pamonha',
    database='aps3',
    port=3307
)
cursor = conexao.cursor()

consulta = "SELECT titulo FROM posts"
cursor.execute(consulta)
titulos = cursor.fetchall()

titulos = [titulo[0] for titulo in titulos]

vectorizer = TfidfVectorizer(stop_words=stop_words)
X = vectorizer.fit_transform(titulos)

kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(X)

clusters = kmeans.labels_

for i in range(2):
    cluster_words = []
    for j, titulo in enumerate(titulos):
        if clusters[j] == i:
            cluster_words.extend(titulo.split())
    print(f"Cluster {i+1}: {', '.join(cluster_words)}")

cursor.close()
conexao.close()
