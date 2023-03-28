# %%
# pip install beautifulsoup4
# !pip install requests
# !pip install mysql-connector-python


# %%
import requests
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin
import json
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from tqdm import tqdm
nltk.download('wordnet')
nltk.download('omw')
nltk.download('omw-1.4')

# %%
def webscrap(input_url, max_depth):

    url_regex = re.compile(
    r'^(?:http|https):\/\/',
    re.IGNORECASE
    )

    # Define a página web a ser analisada
    url = input_url
    max_depth = max_depth
    data = {}
    content = []

    res = requests.get(url)
    soup_queue = BeautifulSoup(res.content, 'html.parser')

    # Inicia a fila com o elemento raiz
    queue = deque([soup_queue])

    # Enquanto houver elementos na fila
    while queue:
        # Remove o próximo elemento da fila
        current_element= queue.popleft()
        
        # Procura todos os links no elemento atual
        links = current_element.find_all('a')
        
        # Adiciona todos os elementos encontrados na fila
        for link in links[:max_depth]:
            # Obtem o valor do atributo href do link
            href = link.get('href')
            
            # Verifica se o link é diferente de None e começa com "https" ou "http"
            if href and (href.startswith('https') or href.startswith('http')):
                # Se já começar com "https" ou "http", utiliza o link sem modificação
                final_link = href
            else:
                # Se não começar com "https" ou "http", adiciona "https://" antes do link
                final_link = urljoin(url, href)

            if url_regex.match(final_link):
                valid_link = final_link
                #list_link.append(valid_link)
            
            # Faz a requisição do conteúdo da página
            response = requests.get(valid_link)

            # Cria o objeto Beautiful Soup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Obtém o título da página
            title = soup.title.string
            #title = valid_link.replace("https://", "").replace("\\", "").replace("https:\\", "").replace("www", "")

            # Obtém o conteúdo da página
            p_tags = soup.find_all('p')
            for p in p_tags:
                content.append(p.text)
            join_content = ' '.join(content)

            # Cria um dicionário com o título e o conteúdo da página
            data = {"title": title, "content": re.sub(r'\r?\n|\r', '', join_content), "url": valid_link}

            # # Cria um arquivo JSON com o nome do link e o conteúdo do dicionário
            # Nome do diretório a ser criado
            dir_name = str(re.sub(r'\W+', '_', url))

            # Verifica se o diretório já existe
            if not os.path.exists(dir_name):
                # Cria o diretório
                os.makedirs(dir_name)

        
            clean_file_name = re.sub(r'\W+', '_', title.replace("https", ""))
            file_name = os.path.join(dir_name,f"{clean_file_name}.json")
            file_path = os.path.join(dir_name, file_name)
            if not os.path.exists(file_path):
                #os.makedirs(file_path)
                with open(file_name, "w") as f:
                    json.dump(data, f)
    
    content_list = []
    title_list = []
    url_list = []

    for filename in os.listdir(dir_name):
        file_path_ = os.path.join(dir_name, filename)
        with open(file_path_, "r") as file:
            data = json.load(file)
            data_content = str(data['content'])
            content_list.append(data_content)
            title_list.append(data['title'])
            url_list.append([data['url']][0])
    data_dict={'Title':title_list,'Content':content_list,'Url':url_list}
    df = pd.DataFrame(data_dict)

    return df

# %%
# webscrap_df = webscrap('https://solarsystem.nasa.gov/planets/overview/', 2)
# webscrap_df

# %%
def create_index(df):
    doc_content = df['Content']

    # Initialize TfidfVectorizer with custom stopword list
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(doc_content).todense()

    indice_invertido = {}
    for term in tqdm(vectorizer.vocabulary_):
        dic_score = {}
        for i, doc in enumerate(doc_content):
            j = vectorizer.vocabulary_[term] #term frequency
            value_tfidf = tfidf[i,j]
            #print(float(value_tfidf))
            if value_tfidf > 0:
                dic_score[df['Url'][i]] = value_tfidf
        indice_invertido[term] = dic_score
    
    return indice_invertido

# %%
# inv_index = create_index(webscrap_df)

# %%
def buscar_inv(palavras, indice):
    words = palavras.split()
    assert type(words)==list
    resultado = dict()
    for p in words:
        if p in indice.keys():
            for documento in indice[p].keys():
                if documento not in resultado.keys():
                    resultado[documento] = indice[p][documento]
                else:
                    resultado[documento] += indice[p][documento]

    return resultado

# %%
# resultado = buscar_inv('cold',inv_index)

# %%
# if isinstance(resultado, str):
#     print(resultado)

# %%
# max_value_url = max(resultado, key=lambda x: resultado[x])
# title = webscrap_df[webscrap_df['Url'] == max_value_url]['Title'].values[0]
# content = webscrap_df[webscrap_df['Url'] == max_value_url]['Content'].values[0]

# print(title)
# print(content)
# print(max_value_url)
# print("Score:", resultado[max_value_url])

# %%
def get_synonyms(palavra,df):
    words = palavra

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(df['Content']).todense()

    highest_score = 0
    syns1 = wordnet.synsets(words)[0]
    seen_words = set()  # Set to keep track of words already in the list
    
    for term in vectorizer.vocabulary_:
        try:
            syns2 = wordnet.synsets(str(term))
            for syn in syns2:
                syn_name = syn.name().split('.')[0]
                if syn_name in vectorizer.vocabulary_:
                    #print(syn_name)
                    score = syns1.wup_similarity(syns2)
                    if score != 1:  # Exclude perfect matches
                        word = syns2.name().split('.')[0]
                        if word not in seen_words:  # Append only if word is not already in list
                            if score > highest_score:
                                highest_score = score
                                highest_word = word
                                seen_words.add(word)
        except IndexError:
            continue

    return highest_word

# %%
def get_synonyms(palavra,df):
    words = palavra

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(df['Content']).todense()

    highest_score = 0
    syns1 = wordnet.synsets(words)[0]
    seen_words = set()  # Set to keep track of words already in the list
    
    for term in vectorizer.vocabulary_:
        try:
            syns2 = wordnet.synsets(str(term))
            for syn in syns2:
                syn_name = syn.name().split('.')[0]
                if syn_name in vectorizer.vocabulary_:
                    score = syns1.wup_similarity(syn)
                    if score is not None and score != 1:  # Exclude perfect matches
                        word = syn_name
                        if word not in seen_words:  # Append only if word is not already in list
                            if score > highest_score:
                                highest_score = score
                                highest_word = word
                                seen_words.add(word)
        except IndexError:
            continue

    return highest_word


# %%
def multiple_synonyms(palavras,df):
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf = vectorizer.fit_transform(df['Content']).todense()

    words = palavras.split()
    assert type(words)==list

    for i in range(len(words)):
        try:
            if words[i] not in vectorizer.vocabulary_:
                syn = get_synonyms(words[i],df)
                words[i] = syn
        except IndexError:
            continue
    sentence = " ".join(words)

    return sentence

# %%
# multiple_synonyms('big elephant green planet',webscrap_df)

# %%
# buscar_inv('big fox red planet',inv_index)

# %%



