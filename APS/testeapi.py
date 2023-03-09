import requests

url = 'https://api.nasa.gov/planetary/apod'
headers = {'api_key': 'UbglrrQb1a63BXkBahyfDBxIu6mDb86owxKEwf4X'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print('Erro ao fazer a chamada da API')
