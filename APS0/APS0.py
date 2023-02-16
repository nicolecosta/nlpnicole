import discord
import os
from dotenv import load_dotenv

load_dotenv()

SERVIDOR = os.getenv('SERVIDOR')
CANAL = os.getenv('CANAL')
TOKEN = os.getenv('TOKEN')
print(SERVIDOR,CANAL,TOKEN)

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=SERVIDOR)
    channel = discord.utils.get(guild.text_channels, name=CANAL)
    #await channel.send('O bot está online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == '!oi':
        await message.channel.send('Olá!')

    elif message.content.lower() == '!author':
        await message.channel.send('Quem me criou foi a Nicole Sarvasi :)')

    elif message.content.lower() == '!source':
        await message.channel.send('Aqui está o meu código-fonte: https://github.com/nicolecosta/nlpnicole')

client.run(TOKEN)