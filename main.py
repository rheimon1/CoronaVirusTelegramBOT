import os
import requests
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler


def brazil(bot, update: Update):
    # Dados da requisição feita na API do coronaanalytic
    dataBrazil = requests.get("https://api.coronaanalytic.com/brazil").json()

    values = dataBrazil["values"]

    deaths, cases, suspects = 0, 0, 0
    date = str(dataBrazil["date"])
    time = str(dataBrazil["time"])

    for state in values:
        for key, value in state.items():
            if key == 'deaths':
                deaths += value
            if key == 'cases':
                cases += value
            if key == 'suspects':
                suspects += value

    response_message = "Informações gerais sobre o corona vírus (COVID-19) no Brasil\n\n - Casos: {}; \n - Suspeitas: {}; \n - Mortes: {}. \n\n Última atualização: {} às {}. \n\n Todas as informações são atualizadas a cada hora com a fonte de dados fornecida pelo governo do Brasil: https://saude.gov.br"

    update.message.reply_text(response_message.format(cases, suspects, deaths, date, time), quote=False)


def world(bot, update: Update):
    req = requests.get("https://api.coronaanalytic.com/").json()

    dataWorld = req["world"]

    deaths = 0
    cases = 0
    suspects = 0
    date = str(dataWorld["date"])
    time = str(dataWorld["time"])

    valuesWorld = dataWorld["values"]

    for country in valuesWorld:
        for key, value in country.items():
            if key == 'deaths':
                deaths += value
            if key == 'cases':
                cases += value
            if key == 'suspects':
                suspects += value

    response_message = "Informações gerais sobre o corona vírus (COVID-19) no mundo\n\n - Casos: {} \n - Suspeitas: {} \n - Mortes: {}. \n\n Última atualização: {} às {}. \n\n Todas as informações são atualizadas a cada hora com a fonte de dados fornecida pelo governo do Brasil: https://saude.gov.br"

    update.message.reply_text(response_message.format(cases, suspects, deaths, date, time), quote=False)


def sao_paulo(bot, update: Update):
    dataSaoPaulo = requests.get("https://api.coronaanalytic.com/brazil/35").json()

    cases = dataSaoPaulo["cases"]
    suspects = dataSaoPaulo["suspects"]
    deaths = dataSaoPaulo["deaths"]

    response_message = "Informações gerais sobre o corona vírus (COVID-19) em São Paulo\n\n - Casos: {}; \n - Suspeitas: {}; \n - Mortes: {}. \n\n Todas as informações são atualizadas a cada hora com a fonte de dados fornecida pelo governo do Brasil: https://saude.gov.br"

    update.message.reply_text(response_message.format(cases, suspects, deaths), quote=False)


def start(bot, update: Update):
    update.message.reply_text('OIII', quote=False)


def webhook(request):
    bot = Bot(token=os.environ["TELEGRAM_TOKEN"])
    
    dispatcher = Dispatcher(bot, None, 0)
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('coronaMundo', world))
    dispatcher.add_handler(CommandHandler('coronaBrasil', brazil))
    dispatcher.add_handler(CommandHandler('coronaSP', sao_paulo))

    if request.method == 'POST':
        update = Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'
