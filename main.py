import os
import requests
import json
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler


def brazil(bot, update: Update):
    # Dados da requisição feita na API
    req = requests.get("https://coronavirus-19-api.herokuapp.com/countries/Brazil")

    dataBrazil = req.content.decode()

    dataBrazil = json.loads(dataBrazil)

    cases = dataBrazil["cases"]
    critical = dataBrazil["critical"]
    todayCases = dataBrazil["todayCases"]
    deaths = dataBrazil["deaths"]
    recovered = dataBrazil["recovered"]

    response_message = "Informações gerais sobre o corona vírus (COVID-19) no Brasil\n\n - Casos: {}; \n - Casos críticos: {};\n - Casos novos: {};\n - Mortes: {};\n - Recuperados: {}. \n\n Fonte: https://www.worldometers.info/coronavirus/"

    update.message.reply_text(response_message.format(cases, critical, todayCases, deaths, recovered), quote=False)


def world(bot, update: Update):
    req = requests.get("https://coronavirus-19-api.herokuapp.com/all")

    # convert from byte to string
    dataWorld = req.content.decode()

    # convert json
    dataWorld = json.loads(dataWorld)

    cases = dataWorld["cases"]
    deaths = dataWorld["deaths"]
    recovered = dataWorld["recovered"]

    response_message = "Informações gerais sobre o corona vírus (COVID-19) no Mundo\n\n - Casos: {};\n - Mortes: {};\n - Recuperados: {}. \n\n Fonte: https://www.worldometers.info/coronavirus/"

    update.message.reply_text(response_message.format(cases, deaths, recovered), quote=False)
    

def webhook(request):
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    
    dispatcher = Dispatcher(bot, None, 0)
    
    dispatcher.add_handler(CommandHandler('coronamundo', world))
    dispatcher.add_handler(CommandHandler('coronabrasil', brazil))

    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'
