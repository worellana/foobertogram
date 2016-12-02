import time
import random
import datetime
import re
import telepot
import pywapi
from lxml import html
import requests

saludos = ['gay de farmacia', 'gay de circo', 'gay de playa', 'gay de pueblo', 'gay de finca', 'gay de mezquita',
           'gay de cantina', 'gay de champa', 'gay asolapado', 'gay de ciudad', 'gay de convento', 'gay de hospital',
           'gay de carretera', 'gay de gasolinera']

def handle(msg):
    # print(msg)
    chat_id = msg['chat']['id']
    message = msg['text']
    command = message.split(' ', 1)[0]

    try:
        username = msg['from']['username']
    except:
        username = msg['from']['first_name']

    try:
        argumentos = message.split(' ', 1)[1]
    except IndexError:
        argumentos = ''

    # Sanitizando entradas del usuario
    argumentos = re.sub('[^A-Za-z]+', '', argumentos)

    if command == '/quote':
        bot.sendMessage(chat_id, 'Ya casi.... solo faltan un par de detalles')
    elif command == '/time':
        bot.sendMessage(chat_id, str(datetime.datetime.now()))
    elif command == '/fortune':
        bot.sendMessage(chat_id, 'No se lo que depara la fortuna')
    elif command == '/pipianometro':
        bot.sendMessage(chat_id, 'No les hablen de pipianadas que se emocionan...')
    elif command == '/urbano':
        if argumentos == '':
            # Obtener algo random de urbano
            page = requests.get('http://www.urbandictionary.com/random.php')
        else:
            page = requests.get('http://www.urbandictionary.com/define.php?term=' + argumentos)

        tree = html.fromstring(page.content)
        word = tree.xpath('//a[@class="word"]/text()')
        definicion = tree.xpath('//div[@class="meaning"]/text()')
        if argumentos == '':
            palabra = str(word[0])
            content = str(definicion[0])
            bot.sendMessage(chat_id, palabra + ' : ' + content)                        
        else:
            content = str(definicion[0])
            bot.sendMessage(chat_id, argumentos + ' : ' + content)
    elif command == '/saludar':
        saludo = random.choice(saludos)
        if argumentos == '':
            bot.sendMessage(chat_id, '@' + username + ' ' + saludo)
        else:
            bot.sendMessage(chat_id, argumentos + ' ' + saludo)
    elif command == '/weather':
        if argumentos == '':
            bot.sendMessage(chat_id, 'Despues del comando envia la ciudad de la cual quieres saber el clima.')
        else:
            lookup = pywapi.get_location_ids(argumentos)
            test = pywapi.get_location_ids(argumentos)
            print(test)
            for i in lookup:
                location_id = i

            weather_com_result = pywapi.get_weather_from_weather_com(location_id, 'C')
            condiciones = weather_com_result['current_conditions']['text']
            temp = "Weather.com dice que esta " + condiciones.lower() + " y " + \
                   weather_com_result['current_conditions']['temperature'] + "C ahora en " + \
                   weather_com_result['location']['name']
            bot.sendMessage(chat_id, temp)
    elif command == '/help':
        bot.sendMessage(chat_id,
                        'Comandos disponibles?: \n /quote \n /time \n /fortune \n /pipianometro \n /urbano \n /weather')
    elif command == '/eshta':
        bot.sendMessage(chat_id, '@' + username + ' yo se que te encanta ESHTA, pero trata de controlarte.')

bot = telepot.Bot('317201201:AAHHXyMUVSByqJJO1dBRFT4WGSQ96jjnKm0')
bot.message_loop(handle)
print('Estoy escuchando....')

while 1:
    time.sleep(10)
