import discord
import os
from dotenv import load_dotenv
import re
import requests
from aps3_functions import webscrap, create_index, webscrap, buscar_inv, get_synonyms, multiple_synonyms
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from bs4 import BeautifulSoup
from collections import deque
from urllib.parse import urljoin
import json
import os
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

load_dotenv()

SERVIDOR = os.getenv('SERVIDOR')
CANAL = os.getenv('CANAL')
TOKEN = os.getenv('TOKEN')
NASA_API_KEY = os.getenv('NASA_API_KEY')

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
dir_name = ''
webscrap_df = pd.DataFrame()
inv_index = {}
crawl = False



@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=SERVIDOR)
    channel = discord.utils.get(guild.text_channels, name=CANAL)
    #await channel.send('O bot está online!')

@client.event
async def on_message(message):

    text_message = message.content.lower()
    commands = ['!oi','!author','!source','!help']
    global dir_name

    if message.author == client.user:
        return

    if text_message == '!oi':
        await message.channel.send('Olá!')

    elif text_message == '!author':
        await message.channel.send('Quem me criou foi a Nicole Sarvasi :)')

    elif text_message == '!source':
        await message.channel.send('Aqui está o meu código-fonte: https://github.com/nicolecosta/nlpnicole')

    elif text_message == '!help':
        await message.channel.send('Para utilizar o **Webscrapping + Queries de Busca** temos 3 comandos:\n\n`!crawl` + uma url, por exemplo: \n`!crawl https://solarsystem.nasa.gov/planets/overview/`\n`!search` acompanhado de uma ou mais palavras de busca, por exemplo: \n`!search dwarf planet` \n`!wn_search` acompanhado de uma ou mais palavras de busca, por exemplo: \n`!search little planet`\n\n * _é preciso primeiro fazer o crawl para depois fazer a busca_ \n\n\n Para visualizar a **Astronomy Picture of the Day**, envie uma mensagem com **`!run + data(YYYY-MM-DD)`**\n\nSe quiser a imagem com sua descrição envie **`!run + data(YYYY-MM-DD) + info`** \n\n**Por exemplo:** \n!run 2000-09-24\n!run 2000-09-24 info\n\n * _é importante lembrar que as imagens começaram a partir de 16 de junho de 1995_ ')

    elif text_message.startswith('!run'):
        pattern_date_api =r'^!run\s((?!199[0-4]|1995-0[1-5])\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]))( info)?$'
        match = re.match(pattern_date_api, text_message)
        if match:
            date = match.group(1)
            url = "https://api.nasa.gov/planetary/apod"
            params = {
                "api_key": NASA_API_KEY,
                "date": date
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                apod_info = response.json()

                # extraindo as informações do dicionário
                title = apod_info["title"]
                explanation = apod_info["explanation"]
                image_url = apod_info["url"]
                image_response = requests.get(image_url)

                # salvando a imagem
                with open("apod.jpg", "wb") as f:
                    f.write(image_response.content)

                #enviando as mensagens de título, descrição e a própria imagem
                await message.channel.send(f"**{title}**")
                with open("apod.jpg", "rb") as f:
                    await message.channel.send(file=discord.File(f))
                
                if text_message.endswith('info'):
                    await message.channel.send(f"{explanation}")
                    
            else:
                # se a requisição não for bem sucedida
                await message.channel.send(f"Error: Request returned status code {response.status_code}")

        else:
            await message.channel.send('Oops, algo deu errado :( Verifique a chamada correta com o comando `!help`')

    elif text_message.startswith('!crawl'):
        global webscrap_df
        url_pattern = r"!crawl\s+(https?://\S+)"
        match = re.match(url_pattern, text_message)
        if match:
            try:
                await message.channel.send('Crawling iniciado...')
                webscrap_url = match.group(1)
                webscrap_df = webscrap(webscrap_url, 25)
                pipeline = joblib.load('modelo.joblib')
                webscrap_df['truncated_content'] = webscrap_df['content'].str.split().str[:40].str.join(' ')
                probabilities = pipeline.predict_proba(webscrap_df['truncated_content'])
                polarities = (2 * probabilities[:,1]) - 1
                webscrap_df['threshold'] = polarities
            except Exception as e:
                # Send an error message to the user
                await message.channel.send(f"Ops parece que tivemos um imprevisto :0 \nTente novamente com outro link")
            global inv_index
            inv_index = create_index(webscrap_df)
            global crawl
            crawl = True
            await message.channel.send('Agora você pode utilizar os comandos `!search` e `!wn_search` para fazer buscas')
        else: 
            await message.channel.send('Por favor escreva o comando `!crawl` + uma url, por exemplo: \n`!crawl https://solarsystem.nasa.gov/planets/overview/`')

    elif text_message.startswith('!search'):
        if crawl == True:
            input_pattern = r"!search\s+(\S+)"
            input_pattern_th = r"!search\s+(\S+)\s*(?:th=([\d\.]+))?"
            match = re.match(input_pattern, text_message)
            match_th = re.match(input_pattern_th, text_message)
            if match or match_th:
                palavras = re.sub('!search', '',text_message)
                resultado = buscar_inv(palavras,inv_index)
                if resultado == {}:
                    await message.channel.send(f"Parece que esse assunto não pode ser encontrado aqui :(")
                else:
                    max_value_url = max(resultado, key=lambda x: resultado[x])
                    title = webscrap_df[webscrap_df['Url'] == max_value_url]['Title'].values[0]

                    if match_th:
                        threshold = float(match_th.group(2)) if match_th.group(2) else None
                        threshold_df = webscrap_df.loc[webscrap_df['Url'] == max_value_url, 'threshold'].iloc[0]
                        if threshold >= threshold_df:
                            await message.channel.send(f"**{title}** \n {max_value_url}")
                        else:
                            await message.channel.send('Me desculpe, nenhum resultado atende as suas expectativas de sentimento :(')
                    else:
                        await message.channel.send(f"**{title}** \n {max_value_url}")

            else:
                await message.channel.send('Por favor escreva o comando `!search` acompanhado de uma ou mais palavras de busca, por exemplo: \n`!search dwarf planet`')

        else:
            await message.channel.send('Para fazer o `!search` é preciso primeiro fazer o `!crawl`')
    
    elif text_message.startswith('!wn_search'):
        if crawl == True:
            input_pattern = r"!wn_search\s+(\S+)"
            match = re.match(input_pattern, text_message)
            if match:
                palavras = re.sub('!search', '',text_message)
                synonym = multiple_synonyms(palavras,webscrap_df)
                resultado = buscar_inv(synonym,inv_index)
                if resultado == {}:
                    await message.channel.send(f"Parece que esse assunto não pode ser encontrado aqui :(")
                else:
                    max_value_url = max(resultado, key=lambda x: resultado[x])
                    title = webscrap_df[webscrap_df['Url'] == max_value_url]['Title'].values[0]
                    await message.channel.send(f"**{title}** \n {max_value_url}")
            else:
                await message.channel.send('Por favor escreva o comando `!wn_search` acompanhado de uma ou mais palavras de busca, por exemplo: \n`!search little planet`')
        else:
            await message.channel.send('Para fazer o `!search` é preciso primeiro fazer o `!crawl`')


    # elif text_message not in commands:
    #     await message.channel.send('Parece que não tenho esse comando ainda :O\n\nUma lista de coisas que você pode me mandar: ```!oi\n!author\n!source\n!help```' )

client.run(TOKEN)