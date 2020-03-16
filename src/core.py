from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

import requests

from conf.settings import BASE_API_URL, TELEGRAM_TOKEN

def brazil(bot, update):

     # Dados da requisição feita na API do coronaanalytic
    dataBrazil = requests.get(BASE_API_URL+"brazil").json()

    values = dataBrazil["values"]

    deaths = 0
    cases = 0
    suspects = 0
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

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message.format(cases, suspects, deaths, date, time)
    )

def world(bot, update):

    req = requests.get(BASE_API_URL).json()

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

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message.format(cases, suspects, deaths, date, time)
    )

def sao_paulo(bot, update):
    dataSaoPaulo = requests.get(BASE_API_URL+"brazil/35").json()

    cases = dataSaoPaulo["cases"]
    suspects = dataSaoPaulo["suspects"]
    deaths = dataSaoPaulo["deaths"]

    response_message = "Informações gerais sobre o corona vírus (COVID-19) em São Paulo\n\n - Casos: {}; \n - Suspeitas: {}; \n - Mortes: {}. \n\n Todas as informações são atualizadas a cada hora com a fonte de dados fornecida pelo governo do Brasil: https://saude.gov.br"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message.format(cases, suspects, deaths)
    )

def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(
        CommandHandler('coronaBrasil', brazil)
    )

    dispatcher.add_handler(
        CommandHandler('coronaMundo', world)
    )

    dispatcher.add_handler(
      CommandHandler('coronaSP', sao_paulo)
    )

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    print("press CTRL + C to cancel.")
    main()
